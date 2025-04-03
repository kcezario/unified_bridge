from abc import ABC, abstractmethod
from typing import Any, Dict


class InvoiceClientInterface(ABC):
    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """Carrega as configurações a partir das variáveis de ambiente."""
        pass

    @abstractmethod
    def get_access_token(self) -> str:
        """Recupera o token de acesso para o sistema de emissão de notas fiscais."""
        pass

    @abstractmethod
    def issue_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Emite uma nova nota fiscal."""
        pass

    @abstractmethod
    def cancel_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Cancela uma nota fiscal existente."""
        pass

    @abstractmethod
    def get_invoice_status(self, invoice_id: str) -> Dict[str, Any]:
        """Consulta o status de uma nota fiscal."""
        pass
