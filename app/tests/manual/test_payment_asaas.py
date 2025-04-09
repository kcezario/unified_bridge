import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from app.payment.payment_client_asaas import PaymentClientAsaas
from app.utils.logger import get_logger

# Carregar variáveis de ambiente
load_dotenv()
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["LOG_DIR"] = "tests/logs"

logger = get_logger("manual_test")


def test_payment_asaas():
    logger.info("🚀 Iniciando teste manual de pagamento Asaas...")

    client = PaymentClientAsaas()

    payment_data = {
        "customer": "cus_000006622263",
        "billingType": "PIX",
        "value": 25.00,
        "dueDate": (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "description": "Pagamento de teste via API",
    }

    created = client.create_payment(payment_data)
    logger.info(f"✅ Pagamento criado: {created}")

    payment_id = created.get("id")
    if not payment_id:
        logger.error("❌ ID do pagamento não retornado.")
        return

    # --- Consultar status ---
    logger.info("🔍 Consultando status do pagamento...")
    status = client.get_payment_status(payment_id)
    logger.info(f"ℹ️ Status do pagamento: {status}")

    # --- Cancelar pagamento ---
    logger.info("🛑 Cancelando pagamento...")
    cancelled = client.cancel_payment(payment_id)
    logger.info(f"✅ Pagamento cancelado: {cancelled}")


if __name__ == "__main__":
    test_payment_asaas()
