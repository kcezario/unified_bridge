from abc import ABC, abstractmethod
from typing import Any, Dict


class InvoiceClientInterface(ABC):
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
