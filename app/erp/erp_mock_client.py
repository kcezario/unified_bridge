import os
from typing import Any, Dict
from erp.erp_client_interface import ERPClientInterface
from utils.logger import get_logger

logger = get_logger(__name__)


class ERPClientMock(ERPClientInterface):
    def __init__(self):
        self._token = None
        self._receivables = {}  # simula uma "tabela" na memória

    def get_config(self) -> Dict[str, Any]:
        logger.debug("MockERP: carregando configurações do ambiente.")
        config = {
            "app_key": os.getenv("MOCK_ERP_APP_KEY"),
            "app_secret": os.getenv("MOCK_ERP_APP_SECRET")
        }

        if not config["app_key"] or not config["app_secret"]:
            logger.error("MockERP: chaves MOCK_ERP_APP_KEY ou MOCK_ERP_APP_SECRET ausentes.")
            raise EnvironmentError("Variáveis de ambiente do ERP Mock ausentes.")

        return config

    def get_access_token(self) -> str:
        config = self.get_config()
        # Geração fake de token
        self._token = f"mock-token-{config['app_key'][-4:]}"
        logger.info(f"MockERP: token gerado com sucesso: {self._token}")
        return self._token

    def create_accounts_receivable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        token = data.get("token")
        if token != self._token:
            logger.error("MockERP: token inválido ou ausente ao criar conta a receber.")
            raise ValueError("Token inválido.")

        required_fields = ["customer_id", "amount", "due_date"]
        for field in required_fields:
            if field not in data:
                logger.error(f"MockERP: campo obrigatório '{field}' ausente.")
                raise ValueError(f"Campo obrigatório '{field}' ausente.")

        logger.info(f"MockERP: token {token} validado com sucesso.")

        ar_id = f"ar-{len(self._receivables) + 1}"
        self._receivables[ar_id] = {
            "id": ar_id,
            "customer_id": data["customer_id"],
            "amount": data["amount"],
            "due_date": data["due_date"],
            "status": "open"
        }

        logger.info(f"MockERP: conta a receber criada com ID {ar_id}")
        return {"status": "success", "accounts_receivable_id": ar_id}

    def update_accounts_receivable(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if id not in self._receivables:
            logger.warning(f"MockERP: conta a receber {id} não encontrada.")
            return {"status": "not_found"}

        self._receivables[id].update(data)
        logger.info(f"MockERP: conta a receber {id} atualizada.")
        return {"status": "success", "updated_id": id}

    def settle_accounts_receivable(self, id: str) -> Dict[str, Any]:
        if id not in self._receivables:
            logger.warning(f"MockERP: conta a receber {id} não encontrada.")
            return {"status": "not_found"}

        self._receivables[id]["status"] = "settled"
        logger.info(f"MockERP: conta a receber {id} marcada como paga.")
        return {"status": "success", "settled_id": id}
