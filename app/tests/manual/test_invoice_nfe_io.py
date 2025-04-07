import os
from dotenv import load_dotenv

from app.invoice.invoice_client_nfe_io import InvoiceClientNFEio
from app.utils.logger import get_logger

load_dotenv()
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["LOG_DIR"] = "tests/logs"

logger = get_logger("manual_test")

def test_invoice_nfe_io():
    logger.info("🚀 Iniciando teste manual de emissão de NFSE...")

    client = InvoiceClientNFEio()

    data = client.create_data(
        origem="mock",
        identificador="12345678000100",
        city_service_code="101",
        description="Serviços de consultoria em tecnologia",
        services_amount=1500.00,
        taxation_type="None",
        iss_rate=2.5
    )

    response = client.issue_invoice(data)
    logger.info(f"✅ NFSE emitida com sucesso: {response}")

    invoice_id = response.get("id")
    if invoice_id:
        logger.info(f"🔎 Consultando status da NFSE: {invoice_id}")
        status = client.get_invoice_status(invoice_id)
        logger.info(f"📄 Status da nota: {status}")
    else:
        logger.warning("⚠️ Nenhum ID retornado na emissão.")

if __name__ == "__main__":
    test_invoice_nfe_io()
