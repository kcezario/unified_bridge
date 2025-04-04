import os
from datetime import datetime
from dotenv import load_dotenv
from uuid import uuid4

from app.core.client_factory import ClientFactory
from app.utils.logger import get_logger

# Força ambiente de teste com log isolado e nível máximo de detalhe
load_dotenv()

os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["LOG_DIR"] = "tests/logs"

logger = get_logger("manual_test")

def test_create_erp():
    logger.info("Iniciando teste manual de ERP...")

    erp_client = ClientFactory.get_erp_client()
    logger.debug(f"Instância do ERP client: {type(erp_client).__name__}")

    codigo_integracao = str(uuid4())
    
    data = {
        "codigo_lancamento_integracao": codigo_integracao,
        "codigo_cliente_fornecedor": 6823222813,  # Pegue um cliente válido do seu ambiente de teste
        "data_vencimento": "04/04/2025",
        "valor_documento": 1234.00,
        "codigo_categoria": "1.01.02",  # Categoria cadastrada no Omie
        "data_previsao": "04/04/2025",
        "id_conta_corrente": 6823222790,  # Conta corrente válida do ambiente de teste
        "observacao": "Teste via API Omie"
    }

    logger.info("Chamando create_accounts_receivable()...")
    result = erp_client.create_accounts_receivable(data)
    logger.info(f"Resultado da criação: {result}")

    lancamento_id = (
        result.get("codigo_lancamento_omie") or
        result.get("codigo_lancamento_integracao") or
        result.get("accounts_receivable_id")
    )
    logger.debug(f"ID do lançamento obtido: {lancamento_id}")

    logger.info("Chamando update_accounts_receivable()...")
    updated = erp_client.update_accounts_receivable(
        id=str(lancamento_id),
        data={"observacao": "Observação atualizada via teste"}
    )
    logger.info(f"Resultado da atualização: {updated}")

    logger.info("Chamando settle_accounts_receivable()...")
    settled = erp_client.settle_accounts_receivable(str(lancamento_id))
    logger.info(f"Resultado da baixa: {settled}")


if __name__ == "__main__":
    test_create_erp()
