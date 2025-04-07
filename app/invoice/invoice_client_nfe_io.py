import os
import requests
from typing import Any, Dict
from app.invoice.invoice_client_interface import InvoiceClientInterface
from app.utils.logger import get_logger

logger = get_logger(__name__)


class InvoiceClientNFEio(InvoiceClientInterface):
    def __init__(self):
        self.base_url = os.getenv("NFEIO_BASE_URL", "https://api.nfse.io/v2")
        self.api_key = os.getenv("NFEIO_API_KEY")

        if not self.api_key:
            logger.error("NFE.io: Chave de API (NFEIO_API_KEY) não configurada.")
            raise EnvironmentError("Chave de API da NFE.io não configurada.")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def issue_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Emite uma nova nota fiscal de produto."""
        company_id = data.pop("company_id")
        url = f"{self.base_url}/companies/{company_id}/productinvoices"
        logger.debug(f"Emitindo NFe via POST {url} com dados: {data}")
        response = requests.post(url, json=data, headers=self.headers)
        return self._handle_response(response)

    def cancel_invoice(self, invoice_id: str, company_id: str) -> Dict[str, Any]:
        """Cancela uma nota fiscal emitida."""
        url = f"{self.base_url}/companies/{company_id}/productinvoices/{invoice_id}"
        logger.debug(f"Cancelando NFe via DELETE {url}")
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)

    def get_invoice_status(self, invoice_id: str, company_id: str) -> Dict[str, Any]:
        """Consulta os detalhes de uma nota fiscal."""
        url = f"{self.base_url}/companies/{company_id}/productinvoices/{invoice_id}"
        logger.debug(f"Consultando NFe via GET {url}")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_invoice_pdf(self, invoice_id: str, company_id: str) -> bytes:
        """Obtém o PDF da nota fiscal emitida."""
        url = f"{self.base_url}/companies/{company_id}/productinvoices/{invoice_id}/pdf"
        logger.debug(f"Baixando PDF da NFe via GET {url}")
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.content

    def get_invoice_xml(self, invoice_id: str, company_id: str) -> str:
        """Obtém o XML da nota fiscal emitida."""
        url = f"{self.base_url}/companies/{company_id}/productinvoices/{invoice_id}/xml"
        logger.debug(f"Baixando XML da NFe via GET {url}")
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code >= 400:
            logger.error(f"NFE.io: Erro HTTP {response.status_code} - {response.text}")
            response.raise_for_status()

        logger.info("NFE.io: Requisição concluída com sucesso.")
        return response.json()
