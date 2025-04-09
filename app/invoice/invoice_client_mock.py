import os
from typing import Any, Dict
from app.invoice.invoice_client_interface import InvoiceClientInterface
from app.utils.logger import get_logger

logger = get_logger(__name__)


class InvoiceClientMock(InvoiceClientInterface):
    def __init__(self):
        self._token = None
        self._invoices = {}

    def get_config(self) -> Dict[str, Any]:
        logger.debug("MockInvoice: carregando configurações do ambiente.")
        api_key = os.getenv("MOCK_INVOICE_API_KEY")

        if not api_key:
            logger.error("MockInvoice: variável MOCK_INVOICE_API_KEY ausente.")
            raise EnvironmentError("Variável de ambiente do Invoice Mock ausente.")

        return {"api_key": api_key}

    def get_access_token(self) -> str:
        config = self.get_config()
        self._token = f"mock-invoice-token-{config['api_key'][-3:]}"
        logger.info(f"MockInvoice: token gerado com sucesso: {self._token}")
        return self._token

    def issue_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        token = data.get("token")
        if token != self._token:
            logger.error("MockInvoice: token inválido ou ausente ao emitir nota.")
            raise ValueError("Token inválido.")

        required_fields = ["customer_id", "amount", "service_description"]
        for field in required_fields:
            if field not in data:
                logger.error(f"MockInvoice: campo obrigatório '{field}' ausente.")
                raise ValueError(f"Campo obrigatório '{field}' ausente.")

        logger.info(f"MockInvoice: token {token} validado com sucesso.")

        invoice_id = f"inv-{len(self._invoices) + 1}"
        self._invoices[invoice_id] = {
            "id": invoice_id,
            "customer_id": data["customer_id"],
            "amount": data["amount"],
            "description": data["service_description"],
            "status": "issued",
        }

        logger.info(f"MockInvoice: nota fiscal emitida com ID {invoice_id}")
        return {"status": "success", "invoice_id": invoice_id}

    def cancel_invoice(self, invoice_id: str) -> Dict[str, Any]:
        invoice = self._invoices.get(invoice_id)
        if not invoice:
            logger.warning(f"MockInvoice: nota fiscal {invoice_id} não encontrada.")
            return {"status": "not_found"}

        invoice["status"] = "cancelled"
        logger.info(f"MockInvoice: nota fiscal {invoice_id} cancelada.")
        return {"status": "success", "cancelled_id": invoice_id}

    def get_invoice_status(self, invoice_id: str) -> Dict[str, Any]:
        invoice = self._invoices.get(invoice_id)
        if not invoice:
            logger.warning(f"MockInvoice: nota fiscal {invoice_id} não encontrada.")
            return {"status": "not_found"}

        logger.info(f"MockInvoice: status da nota {invoice_id} = {invoice['status']}")
        return {"status": "success", "invoice_status": invoice["status"]}
