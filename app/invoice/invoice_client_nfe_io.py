import os
import json
import requests
from datetime import datetime
from uuid import uuid4
from typing import Any, Dict

from app.invoice.invoice_client_interface import InvoiceClientInterface
from app.utils.logger import get_logger
from app.mocks.borrowers import MockBorrower


logger = get_logger(__name__)


class InvoiceClientNFEio(InvoiceClientInterface):
    def __init__(self):
        self.base_url = os.getenv("NFE_IO_BASE_URL", "https://api.nfse.io/v1")
        self.api_key = os.getenv("NFE_IO_API_KEY")
        self.company_id = os.getenv("NFE_IO_COMPANY_ID")

        if not self.api_key or not self.company_id:
            raise EnvironmentError("NFE.io: API Key ou Company ID não configurados corretamente.")

    def _headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"{self.api_key}"
        }

    def get_borrower_info(self, origem: str, identificador: str) -> Dict[str, Any]:
        logger.debug(f"Obtendo dados do tomador: origem={origem}, identificador={identificador}")

        if origem == "mock":
            return MockBorrower.get_by_federal_tax_number(identificador)

        raise NotImplementedError(f"Origem '{origem}' não implementada.")
    
    def issue_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Emite uma nova nota fiscal de serviço (NFSE)."""
        logger.debug("NFE.io: Emitindo NFSE com os dados:")
        logger.debug(data)

        url = f"{self.base_url}/companies/{self.company_id}/serviceinvoices"
        response = requests.post(url, headers=self._headers(), json=data)

        if response.status_code != 202:
            logger.error(f"Erro ao emitir NFSE: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()
    
    def create_data(
        self,
        origem: str,
        identificador: str,
        city_service_code: str,
        description: str,
        services_amount: float,
        taxation_type: str,
        iss_rate: float
    ) -> Dict[str, Any]:
        """Monta o corpo da requisição para emissão de NFSE."""
        borrower = self.get_borrower_info(origem, identificador)
        if not borrower:
            raise ValueError("Tomador de serviços não encontrado.")
        
        external_id = str(uuid4())
        logger.debug(f"externalId gerado: {external_id}")

        data = {
            "borrower": borrower,
            "externalId": external_id,
            "cityServiceCode": city_service_code,
            "description": description,
            "servicesAmount": services_amount,
            "taxationType": taxation_type,
            "issRate": iss_rate,
            "issuedOn": datetime.utcnow().isoformat() + "Z"
        }
        return data

    def cancel_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Cancela uma NFSE existente."""
        logger.debug(f"NFE.io: Cancelando NFSE {invoice_id}...")

        url = f"{self.base_url}/companies/{self.company_id}/serviceinvoices/{invoice_id}"
        response = requests.delete(url, headers=self._headers())

        if response.status_code != 200:
            logger.error(f"Erro ao cancelar NFSE: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()

    def get_invoice_status(self, invoice_id: str) -> Dict[str, Any]:
        """Consulta o status/detalhes de uma NFSE."""
        logger.debug(f"NFE.io: Consultando NFSE {invoice_id}...")

        url = f"{self.base_url}/companies/{self.company_id}/serviceinvoices/{invoice_id}"
        response = requests.get(url, headers=self._headers())

        if response.status_code != 200:
            logger.error(f"Erro ao consultar NFSE: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()


