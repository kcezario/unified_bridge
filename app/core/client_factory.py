import os
from app.erp.erp_client_interface import ERPClientInterface
from app.invoice.invoice_client_interface import InvoiceClientInterface
from app.payment.payment_client_interface import PaymentClientInterface

# Mocks
from app.erp.erp_client_mock import ERPClientMock
from app.invoice.invoice_client_mock import InvoiceClientMock
from app.payment.payment_client_mock import PaymentClientMock

# Futuras implementações reais (ex: Omie)
from app.erp.erp_client_omie import ERPClientOmie

# from app.invoice.nfeio_client import NFeIOClient
# from app.payment.asaas_client import AsaasClient


class ClientFactory:
    @staticmethod
    def get_erp_client() -> ERPClientInterface:
        client_type = os.getenv("ERP_CLIENT", "mock").lower()
        if client_type == "mock":
            return ERPClientMock()
        elif client_type == "omie":
            return ERPClientOmie()
        else:
            raise ValueError(f"ERP client '{client_type}' is not supported.")

    @staticmethod
    def get_invoice_client() -> InvoiceClientInterface:
        client_type = os.getenv("INVOICE_CLIENT", "mock").lower()
        if client_type == "mock":
            return InvoiceClientMock()
        # elif client_type == "nfe_io":
        #     return NFeIOClient()
        else:
            raise ValueError(f"Invoice client '{client_type}' is not supported.")

    @staticmethod
    def get_payment_client() -> PaymentClientInterface:
        client_type = os.getenv("PAYMENT_CLIENT", "mock").lower()
        if client_type == "mock":
            return PaymentClientMock()
        # elif client_type == "asaas":
        #     return AsaasClient()
        else:
            raise ValueError(f"Payment client '{client_type}' is not supported.")
