from typing import Dict
from app.utils.logger import get_logger

logger = get_logger(__name__)


REQUIRED_FIELDS_CREATE_PAYABLE = [
    "DT_ENTRADA_MD",         # Data de entrada
    "ST_CONTA_CONT",         # Número da conta categoria no plano de contas
    "VL_VALOR_MD",           # Valor da movimentação
    "ID_CONTABANCO_CB",      # ID da conta bancária
    "ID_CONDOMINIO_COND",    # ID do condomínio
]


def validate_create_payable_payload(data: Dict[str, str]) -> None:
    """
    Valida os campos obrigatórios exigidos pela Superlógica
    para criação de uma nova movimentação bancária (contas a pagar).

    Args:
        data (Dict[str, str]): Dados enviados no corpo da requisição.

    Raises:
        ValueError: Se algum campo obrigatório estiver ausente.
    """
    logger.debug("Validando payload de criação de contas a pagar...")

    for field in REQUIRED_FIELDS_CREATE_PAYABLE:
        if not data.get(field):
            raise ValueError(f"O campo obrigatório '{field}' está ausente.")

    logger.info("Payload de criação de contas a pagar validado com sucesso.")
