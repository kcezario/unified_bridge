from abc import ABC, abstractmethod
from typing import Any, Dict


class ERPClientInterface(ABC):
    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """Carrega as configurações a partir das variáveis de ambiente."""
        pass

    @abstractmethod
    def get_access_token(self) -> str:
        """Recupera o token de acesso para o sistema ERP."""
        pass

    @abstractmethod
    def create_accounts_receivable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo lançamento de contas a receber."""
        pass

    @abstractmethod
    def update_accounts_receivable(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um lançamento de contas a receber existente."""
        pass

    @abstractmethod
    def settle_accounts_receivable(self, id: str) -> Dict[str, Any]:
        """Dá baixa (marca como pago) em um lançamento de contas a receber."""
        pass
