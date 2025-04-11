import os
from typing import Any, Dict
from app.payment.payment_client_interface import PaymentClientInterface
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PaymentClientMock(PaymentClientInterface):
    def __init__(self):
        self._token = None
        self._payments = {}

    def get_config(self) -> Dict[str, Any]:
        logger.debug("MockPayment: carregando configurações do ambiente.")
        api_key = os.getenv("MOCK_PAYMENT_API_KEY")

        if not api_key:
            logger.error("MockPayment: variável MOCK_PAYMENT_API_KEY ausente.")
            raise EnvironmentError("Variável de ambiente do Payment Mock ausente.")

        return {"api_key": api_key}

    def get_access_token(self) -> str:
        config = self.get_config()
        self._token = f"mock-payment-token-{config['api_key'][-3:]}"
        logger.info(f"MockPayment: token gerado com sucesso: {self._token}")
        return self._token

    def create_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        token = data.get("token")
        if token != self._token:
            logger.error("MockPayment: token inválido ou ausente ao gerar pagamento.")
            raise ValueError("Token inválido.")

        required_fields = ["customer_id", "amount", "due_date"]
        for field in required_fields:
            if field not in data:
                logger.error(f"MockPayment: campo obrigatório '{field}' ausente.")
                raise ValueError(f"Campo obrigatório '{field}' ausente.")

        logger.info(f"MockPayment: token {token} validado com sucesso.")

        payment_id = f"pay-{len(self._payments) + 1}"
        self._payments[payment_id] = {
            "id": payment_id,
            "customer_id": data["customer_id"],
            "amount": data["amount"],
            "due_date": data["due_date"],
            "status": "pending",
            "bank_slip_url": f"https://mock.boleto/{payment_id}.pdf",
        }

        logger.info(f"MockPayment: pagamento criado com ID {payment_id}")
        return {"status": "success", "payment_id": payment_id}

    def cancel_payment(self, payment_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        payment = self._payments.get(payment_id)
        if not payment:
            logger.warning(f"MockPayment: pagamento {payment_id} não encontrado.")
            return {"status": "not_found"}

        payment["status"] = "cancelled"
        logger.info(f"MockPayment: pagamento {payment_id} cancelado.")
        return {"status": "success", "cancelled_id": payment_id}

    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        payment = self._payments.get(payment_id)
        if not payment:
            logger.warning(f"MockPayment: pagamento {payment_id} não encontrado.")
            return {"status": "not_found"}

        logger.info(f"MockPayment: status do pagamento {payment_id} = {payment['status']}")
        return {"status": "success", "payment_status": payment["status"]}

    def handle_payment_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("MockPayment: processando webhook de pagamento...")

        payment_id = payload.get("payment_id")
        event_type = payload.get("event_type")

        if not payment_id or not event_type:
            logger.error("MockPayment: webhook inválido, campos obrigatórios ausentes.")
            return {"status": "error", "message": "Campos obrigatórios ausentes."}

        payment = self._payments.get(payment_id)
        if not payment:
            logger.warning(f"MockPayment: pagamento {payment_id} não encontrado.")
            return {"status": "not_found"}

        if event_type == "payment_confirmed":
            payment["status"] = "paid"
            logger.info(f"MockPayment: pagamento {payment_id} marcado como pago.")
        elif event_type == "payment_failed":
            payment["status"] = "failed"
            logger.info(f"MockPayment: pagamento {payment_id} marcado como falhou.")
        else:
            logger.warning(f"MockPayment: tipo de evento desconhecido: {event_type}")
            return {"status": "ignored", "message": f"Evento não tratado: {event_type}"}

        return {"status": "success", "payment_id": payment_id, "new_status": payment["status"]}

    def get_payment_link(self, payment_data: Dict[str, Any]) -> str:
        """
        Retorna a URL do boleto (simulada).
        """
        link = payment_data.get("bank_slip_url")
        logger.debug(f"MockPayment: link do boleto = {link}")
        return link or ""
