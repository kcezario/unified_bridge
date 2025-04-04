import os
from typing import Any, Dict
from app.erp.erp_client_interface import ERPClientInterface
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ERPClientMock(ERPClientInterface):
    def __init__(self):
        self._token = None
        self._receivables = {}

    def _get_config(self) -> Dict[str, Any]:
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
        if self._token is None:
            config = self._get_config()
            self._token = f"mock-token-{config['app_key'][-4:]}"
            logger.info(f"MockERP: token gerado com sucesso: {self._token}")
        return self._token

    def _validate_token(self, token: str):
        logger.debug(f"MockERP: token recebido: {token}")
        logger.debug(f"MockERP: token armazenado: {self._token}")
        if token != self._token:
            logger.error("MockERP: token inválido ou ausente.")
            raise ValueError("Token inválido.")

    def create_accounts_receivable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        token = data.pop("token", None)
        self._validate_token(token)

        required_fields = [
            "codigo_cliente_fornecedor",
            "data_vencimento",
            "valor_documento",
            "codigo_categoria",
            "id_conta_corrente"
        ]
        for field in required_fields:
            if field not in data:
                logger.error(f"MockERP: campo obrigatório '{field}' ausente.")
                raise ValueError(f"Campo obrigatório '{field}' ausente.")

        logger.info("MockERP: token validado com sucesso.")

        ar_id = f"ar-{len(self._receivables) + 1}"
        self._receivables[ar_id] = {
            "id": ar_id,
            **data,
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
