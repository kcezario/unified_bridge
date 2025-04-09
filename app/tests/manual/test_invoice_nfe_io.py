import itertools
import os
from dotenv import load_dotenv

from app.invoice.invoice_client_nfe_io import InvoiceClientNFEio
from app.mocks.borrowers import MockBorrower
from app.mocks.services import MockServices
from app.utils.logger import get_logger

# Carregar variáveis de ambiente
dotenv_loaded = load_dotenv()
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["LOG_DIR"] = "tests/logs"

logger = get_logger("manual_test")


def test_invoice_nfe_io():
    logger.info("🚀 Iniciando teste combinatória de emissão de NFSE...")

    client = InvoiceClientNFEio()

    # Coletar mocks
    borrower_mocks = [b["federalTaxNumber"] for b in MockBorrower.mock_infos]
    service_mocks = MockServices.mock_infos

    combinations = list(itertools.product(borrower_mocks, enumerate(service_mocks)))

    for i, (borrower_cnpj, (service_idx, service_data)) in enumerate(combinations):
        logger.info(f"\n=== Teste {i+1}/{len(combinations)} ===")
        logger.info(f"📌 Tomador: {borrower_cnpj} | Serviço mock #{service_idx}")

        try:
            data = client.create_data(
                origem="mock",
                identificador=borrower_cnpj,
                city_service_code=service_data["cityServiceCode"],
                description=service_data["description"],
                services_amount=service_data["servicesAmount"],
                **{k: v for k, v in service_data.items() if k not in ["cityServiceCode", "description", "servicesAmount"]}
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

        except Exception as e:
            logger.error(f"❌ Erro no teste {i+1}: {e}")


if __name__ == "__main__":
    test_invoice_nfe_io()
