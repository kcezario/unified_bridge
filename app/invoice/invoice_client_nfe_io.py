import os
import json
import requests
from datetime import datetime
from uuid import uuid4
from typing import Any, Dict

from app.invoice.invoice_client_interface import InvoiceClientInterface
from app.utils.logger import get_logger
from app.mocks.borrowers import MockBorrower
from app.invoice.constants.nfe_io_constants import (
    OPTIONAL_FIELDS,
    VALID_BORROWER_TYPES,
    VALID_TAX_REGIMES,
    VALID_COUNTRIES_ISO_ALPHA3,
)


logger = get_logger(__name__)


class InvoiceClientNFEio(InvoiceClientInterface):
    def __init__(self):
        self.base_url = os.getenv("NFE_IO_BASE_URL", "https://api.nfse.io/v1")
        self.api_key = os.getenv("NFE_IO_API_KEY")
        self.company_id = os.getenv("NFE_IO_COMPANY_ID")

        if not self.api_key or not self.company_id:
            raise EnvironmentError(
                "NFE.io: API Key ou Company ID não configurados corretamente."
            )

    def _headers(self):
        return {"Content-Type": "application/json", "Authorization": f"{self.api_key}"}

    def get_borrower_info(self, origem: str, identificador: str) -> Dict[str, Any]:
        logger.debug(
            f"Obtendo dados do tomador: origem={origem}, identificador={identificador}"
        )

        if origem == "mock":
            return MockBorrower.get_by_federal_tax_number(identificador)

        raise NotImplementedError(f"Origem '{origem}' não implementada.")

    def _borrower_validator(self, borrower: Dict[str, Any]) -> None:
        """
        Valida a estrutura mínima exigida pela API da Nfe.io para o campo 'borrower'.

        - borrower.address.country é obrigatório (formato ISO 3166-1 alpha-3).
        - Se 'type' estiver presente, deve estar em VALID_BORROWER_TYPES.
        - Se 'taxRegime' estiver presente, deve estar em VALID_TAX_REGIMES.
        """
        if not isinstance(borrower, dict):
            raise ValueError("'borrower' deve ser um dicionário.")

        address = borrower.get("address")
        if not isinstance(address, dict):
            raise ValueError("'borrower.address' deve ser um dicionário.")

        country = address.get("country")
        if not country or not isinstance(country, str):
            raise ValueError(
                "O campo obrigatório 'borrower.address.country' está ausente ou inválido."
            )

        if country.upper() not in VALID_COUNTRIES_ISO_ALPHA3:
            raise ValueError(
                f"Sigla de país inválida: '{country}'. Esperado formato ISO 3166-1 alpha-3, ex: 'BRA', 'USA'."
            )

        borrower_type = borrower.get("type")
        if borrower_type and borrower_type not in VALID_BORROWER_TYPES:
            raise ValueError(
                f"'type' inválido em borrower: '{borrower_type}'. Valores válidos: {VALID_BORROWER_TYPES}"
            )

        tax_regime = borrower.get("taxRegime")
        if tax_regime and tax_regime not in VALID_TAX_REGIMES:
            raise ValueError(
                f"'taxRegime' inválido em borrower: '{tax_regime}'. Valores válidos: {VALID_TAX_REGIMES}"
            )

    def issue_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Emite uma nova nota fiscal de serviço (NFSE)."""
        logger.debug("NFE.io: Emitindo NFSE com os dados:")
        logger.debug(data)

        url = f"{self.base_url}/companies/{self.company_id}/serviceinvoices"
        response = requests.post(url, headers=self._headers(), json=data)

        if response.status_code != 202:
            logger.error(
                f"Erro ao emitir NFSE: {response.status_code} - {response.text}"
            )
            response.raise_for_status()

        return response.json()

    def _process_optional_fields(
        self, data: Dict[str, Any], kwargs: Dict[str, Any]
    ) -> None:
        """
        Processa os campos opcionais e os adiciona ao dicionário de dados, se válidos.
        """
        for key, value in kwargs.items():
            if key in OPTIONAL_FIELDS:
                data[key] = value
                logger.debug(f"Campo opcional incluído: {key} = {value}")
            else:
                logger.warning(f"Campo opcional inválido ignorado: {key}")

    def create_data(
        self,
        origem: str,
        identificador: str,
        city_service_code: str,
        description: str,
        services_amount: float,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Monta o corpo da requisição para emissão de NFSE com os campos obrigatórios,
        e aceita campos adicionais válidos via kwargs.
        """
        borrower = self.get_borrower_info(origem, identificador)
        if not borrower:
            raise ValueError("Tomador de serviços não encontrado.")

        data = {
            "borrower": borrower,
            "cityServiceCode": city_service_code,
            "description": description,
            "servicesAmount": services_amount,
        }

        for key in ["externalId", "issuedOn"]:
            if key not in kwargs:
                kwargs[key] = (
                    str(uuid4())
                    if key == "externalId"
                    else datetime.utcnow().isoformat() + "Z"
                )

        self._process_optional_fields(data, kwargs)

        return data

    def cancel_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Cancela uma NFSE existente."""
        logger.debug(f"NFE.io: Cancelando NFSE {invoice_id}...")

        url = (
            f"{self.base_url}/companies/{self.company_id}/serviceinvoices/{invoice_id}"
        )
        response = requests.delete(url, headers=self._headers())

        if response.status_code != 200:
            logger.error(
                f"Erro ao cancelar NFSE: {response.status_code} - {response.text}"
            )
            response.raise_for_status()

        return response.json()

    def get_invoice_status(self, invoice_id: str) -> Dict[str, Any]:
        """Consulta o status/detalhes de uma NFSE."""
        logger.debug(f"NFE.io: Consultando NFSE {invoice_id}...")

        url = (
            f"{self.base_url}/companies/{self.company_id}/serviceinvoices/{invoice_id}"
        )
        response = requests.get(url, headers=self._headers())

        if response.status_code != 200:
            logger.error(
                f"Erro ao consultar NFSE: {response.status_code} - {response.text}"
            )
            response.raise_for_status()

        return response.json()
