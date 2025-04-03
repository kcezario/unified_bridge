from abc import ABC, abstractmethod
from typing import Any, Dict


class PaymentClientInterface(ABC):
    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """Carrega as configurações a partir das variáveis de ambiente."""
        pass

    @abstractmethod
    def get_access_token(self) -> str:
        """Recupera o token de acesso para o sistema de pagamentos."""
        pass

    @abstractmethod
    def create_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera um novo pagamento (ex: boleto, pix, cartão)."""
        pass

    @abstractmethod
    def cancel_payment(self, payment_id: str) -> Dict[str, Any]:
        """Cancela um pagamento existente."""
        pass

    @abstractmethod
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Consulta o status de um pagamento."""
        pass
