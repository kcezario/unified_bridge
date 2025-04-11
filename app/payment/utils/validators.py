from typing import Dict
from app.payment.constants.asaas_constants import BillingType
from app.utils.logger import get_logger

logger = get_logger(__name__)


def validate_payment_payload(data: Dict[str, any], context: str = "create") -> None:
    """
    Valida os campos obrigatórios para criação ou atualização de cobranças.

    Args:
        data (Dict): Dados da cobrança.
        context (str): "create" ou "update".

    Raises:
        ValueError: se qualquer campo obrigatório estiver ausente ou inválido.
    """
    required_fields_base = ["value", "dueDate"]

    if context == "create":
        required_fields = required_fields_base + ["customer"]
        if "billingType" not in data:
            data["billingType"] = "BOLETO"
            logger.info("Asaas: 'billingType' não fornecido. Usando valor padrão: 'BOLETO'.")
    elif context == "update":
        required_fields = required_fields_base + ["billingType"]
    else:
        raise ValueError(f"Contexto desconhecido para validação: {context}")

    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"O campo obrigatório '{field}' está ausente.")

    billing_type = data.get("billingType")
    if billing_type not in BillingType.ALL:
        raise ValueError(
            f"Tipo de pagamento inválido: {billing_type}. Use um dos: {BillingType.ALL}"
        )
