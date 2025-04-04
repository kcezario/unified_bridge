import os
from uuid import uuid4
from dotenv import load_dotenv
from datetime import datetime

from app.core.client_factory import ClientFactory
from app.utils.logger import get_logger

# Forçar ambiente de teste com logs isolados
load_dotenv()
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["LOG_DIR"] = "tests/logs"

logger = get_logger("manual_test")

# Variáveis globais para reuso entre etapas
codigo_integracao = str(uuid4())
lancamento_id = None


def create_accounts_receivable(data: dict):
    logger.info("🧪 Iniciando teste manual de criação de conta a receber...")

    erp_client = ClientFactory.get_erp_client()
    logger.debug(f"Instância do ERP client: {type(erp_client).__name__}")

    result = erp_client.create_accounts_receivable(data)
    logger.info(f"✅ Resultado da criação: {result}")

    global lancamento_id
    lancamento_id = result.get("codigo_lancamento_omie") or result.get("codigo_lancamento_integracao")
    logger.debug(f"ID do lançamento obtido: {lancamento_id}")
    return lancamento_id


def update_accounts_receivable(id: str, update_data: dict):
    logger.info("🛠️ Testando atualização da conta a receber...")

    erp_client = ClientFactory.get_erp_client()
    result = erp_client.update_accounts_receivable(id=id, data=update_data)
    logger.info(f"✅ Resultado da atualização: {result}")
    return result


def settle_accounts_receivable(id: str, valor: float, conta_corrente_id: str, data: str = None):
    logger.info("💰 Testando baixa da conta a receber...")

    erp_client = ClientFactory.get_erp_client()

    result = erp_client.settle_accounts_receivable(
        id=id,
        valor=str(valor),
        conta_corrente_id=conta_corrente_id,
        data=data or datetime.today().strftime("%d/%m/%Y")
    )
    logger.info(f"✅ Resultado da baixa: {result}")
    return result


if __name__ == "__main__":
    data_criacao = {
        "codigo_lancamento_integracao": codigo_integracao,
        "codigo_cliente_fornecedor": 6823222813,
        "data_vencimento": "04/04/2025",
        "valor_documento": 1234.00,
        "codigo_categoria": "1.01.02",
        "data_previsao": "04/04/2025",
        "id_conta_corrente": 6823222790,
        "observacao": "Teste via API Omie"
    }

    lancamento_id = create_accounts_receivable(data_criacao)

    update_accounts_receivable(
        id=str(lancamento_id),
        update_data={"observacao": "Observação atualizada via teste"}
    )

    settle_accounts_receivable(
        id=str(lancamento_id),
        valor=1234.00,
        conta_corrente_id="6823222790",
        data="04/04/2025"
    )