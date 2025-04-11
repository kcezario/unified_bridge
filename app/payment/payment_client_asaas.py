import json
import os
import requests
from typing import Any, Dict

from app.payment.constants.asaas_constants import WEBHOOK_PAYMENT_FIELDS
from app.payment.payment_client_interface import PaymentClientInterface
from app.payment.utils.validators import validate_payment_payload
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PaymentClientAsaas(PaymentClientInterface):
    def __init__(self):
        self.base_url = os.getenv("ASAAS_BASE_URL")
        self.api_key = os.getenv("ASAAS_API_KEY")

        if not self.api_key:
            raise EnvironmentError("Asaas: chave de API não configurada.")

    def _headers(self):
        return {"Content-Type": "application/json", "access_token": self.api_key}

    def create_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug("Asaas: criando pagamento com os dados:")
        logger.debug(data)

        validate_payment_payload(data, context="create")

        url = f"{self.base_url}/payments"
        response = requests.post(url, headers=self._headers(), json=data)

        if response.status_code not in (200, 201):
            logger.error(
                f"Asaas: erro ao criar pagamento: {response.status_code} - {response.text}"
            )
            response.raise_for_status()

        return response.json()

    def cancel_payment(self, payment_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cancela uma cobrança existente (altera status para CANCELLED)."""
        logger.debug(f"Asaas: cancelando pagamento {payment_id}...")
        
        data["status"] = "CANCELLED"          
        validate_payment_payload(data, context="update")

        url = f"{self.base_url}/payments/{payment_id}"
        response = requests.put(url, headers=self._headers(), json=data)

        if response.status_code != 200:
            logger.error(
                f"Asaas: erro ao cancelar pagamento: {response.status_code} - {response.text}"
            )
            response.raise_for_status()

        return response.json()

    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Consulta o status de um pagamento."""
        logger.debug(f"Asaas: consultando status do pagamento {payment_id}...")

        url = f"{self.base_url}/payments/{payment_id}/status"
        response = requests.get(url, headers=self._headers())

        if response.status_code != 200:
            logger.error(
                f"Asaas: erro ao consultar status: {response.status_code} - {response.text}"
            )
            response.raise_for_status()

        return response.json()


    def handle_payment_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa o webhook de pagamento recebido da Asaas,
        extraindo apenas os campos relevantes definidos em WEBHOOK_PAYMENT_FIELDS.

        Args:
            payload (dict): Payload completo enviado pela Asaas.

        Returns:
            dict: Dados filtrados com os campos mais relevantes para processamento interno.
        """
        logger.info("Asaas: processando payload do webhook de pagamento...")

        flat_data = {}
        for field in WEBHOOK_PAYMENT_FIELDS:
            value = self._extract_nested_field(payload, field)
            flat_data[field] = value
            logger.debug(f"Asaas Webhook: {field} = {value}")

        logger.info("Asaas: extração do webhook concluída com sucesso.")
        return flat_data

    def _extract_nested_field(self, payload: Dict[str, Any], field: str) -> Any:
        """
        Extrai o valor de um campo aninhado do payload, como 'payment.id'.

        Args:
            payload (dict): Dicionário de origem.
            field (str): Caminho no formato 'a.b.c'.

        Returns:
            Any: Valor extraído ou None se não encontrado.
        """
        parts = field.split(".")
        value = payload
        for part in parts:
            if not isinstance(value, dict) or part not in value:
                return None
            value = value[part]
        return value
    
    def get_payment_link(self, payment_data: Dict[str, Any]) -> str:
        """
        Retorna o link do boleto bancário, se disponível.

        Args:
            payment_data (dict): Resposta completa da API após criação ou consulta do pagamento.

        Returns:
            str: URL do boleto (`bankSlipUrl`), ou uma string vazia se não encontrado.
        """
        link = payment_data.get("bankSlipUrl")
        if link:
            logger.info(f"Asaas: link do boleto encontrado: {link}")
        else:
            logger.warning("Asaas: link do boleto não disponível no response.")
        return link or ""
