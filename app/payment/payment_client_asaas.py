import os
import requests
from typing import Any, Dict

from app.payment.payment_client_interface import PaymentClientInterface
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PaymentClientAsaas(PaymentClientInterface):
    def __init__(self):
        self.base_url = os.getenv("ASAAS_BASE_URL")
        self.api_key = os.getenv("ASAAS_API_KEY")

        if not self.api_key:
            raise EnvironmentError("Asaas: chave de API não configurada.")

    def _headers(self):
        return {
            "Content-Type": "application/json",
            "access_token": self.api_key
        }

    def create_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo pagamento (boleto, pix, cartão) para um cliente."""
        logger.debug("Asaas: criando pagamento com os dados:")
        logger.debug(data)

        url = f"{self.base_url}/payments"
        response = requests.post(url, headers=self._headers(), json=data)

        if response.status_code not in (200, 201):
            logger.error(f"Asaas: erro ao criar pagamento: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()

    def cancel_payment(self, payment_id: str) -> Dict[str, Any]:
        """Cancela uma cobrança existente (altera status para CANCELLED)."""
        logger.debug(f"Asaas: cancelando pagamento {payment_id}...")

        url = f"{self.base_url}/payments/{payment_id}"
        data = {"status": "CANCELLED"}

        response = requests.put(url, headers=self._headers(), json=data)

        if response.status_code != 200:
            logger.error(f"Asaas: erro ao cancelar pagamento: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()

    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Consulta o status de um pagamento."""
        logger.debug(f"Asaas: consultando status do pagamento {payment_id}...")

        url = f"{self.base_url}/payments/{payment_id}"
        response = requests.get(url, headers=self._headers())

        if response.status_code != 200:
            logger.error(f"Asaas: erro ao consultar status: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()
