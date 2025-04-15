from abc import ABC, abstractmethod
from typing import Any, Dict

class PayablesClientInterface(ABC):
    @abstractmethod
    def create_payable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova conta a pagar, incluindo informações básicas e links ou anexos."""
        pass

    @abstractmethod
    def settle_payable(self, payable_id: str) -> Dict[str, Any]:
        """Dá baixa (marca como paga) uma conta a pagar já cadastrada."""
        pass

    @abstractmethod
    def cancel_payable(self, payable_id: str) -> Dict[str, Any]:
        """Cancela uma conta a pagar pendente."""
        pass
