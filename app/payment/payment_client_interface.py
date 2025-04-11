from abc import ABC, abstractmethod
from typing import Any, Dict


class PaymentClientInterface(ABC):
    @abstractmethod
    def create_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera um novo pagamento (ex: boleto, pix, cartão)."""
        pass

    @abstractmethod
    def cancel_payment(self, payment_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cancela um pagamento existente."""
        pass

    @abstractmethod
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Consulta o status de um pagamento."""
        pass

    @abstractmethod
    def handle_payment_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um webhook recebido da plataforma de pagamento."""
        pass

    @abstractmethod
    def get_payment_link(self, payment_data: Dict[str, Any]) -> str:
        """Extrai e retorna o link do boleto (caso exista) a partir dos dados da cobrança."""
        pass
