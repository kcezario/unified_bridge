import os
import requests
from typing import Any, Dict
from erp.erp_client_interface import ERPClientInterface
from utils.logger import get_logger

logger = get_logger(__name__)


class ERPClientOmie(ERPClientInterface):
    def __init__(self):
        self.base_url = "https://app.omie.com.br/api/v1/financas/"
        self.app_key = os.getenv("OMIE_APP_KEY")
        self.app_secret = os.getenv("OMIE_APP_SECRET")

        if not self.app_key or not self.app_secret:
            logger.error("Omie: OMIE_APP_KEY ou OMIE_APP_SECRET não configurados.")
            raise EnvironmentError("Credenciais da Omie não configuradas.")

    def get_config(self) -> Dict[str, Any]:
        logger.debug("Omie: carregando configurações.")
        return {"app_key": self.app_key, "app_secret": self.app_secret}

    def get_access_token(self) -> str:
        # A Omie utiliza app_key e app_secret em cada requisição, não há token de acesso separado
        logger.debug("Omie: utilizando app_key e app_secret para autenticação.")
        return f"{self.app_key}:{self.app_secret}"

    def create_accounts_receivable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}contareceber/"
        payload = {
            "call": "IncluirContaReceber",
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "param": [data]
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Omie: conta a receber criada com sucesso. ID: {result['codigo_lancamento']}")
            return result
        else:
            logger.error(f"Omie: erro ao criar conta a receber. Status: {response.status_code}, Erro: {response.text}")
            response.raise_for_status()

    def update_accounts_receivable(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}contareceber/"
        payload = {
            "call": "AlterarContaReceber",
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "param": [{"codigo_lancamento": id, **data}]
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Omie: conta a receber {id} atualizada com sucesso.")
            return result
        else:
            logger.error(f"Omie: erro ao atualizar conta a receber {id}. Status: {response.status_code}, Erro: {response.text}")
            response.raise_for_status()

    def settle_accounts_receivable(self, id: str) -> Dict[str, Any]:
        url = f"{self.base_url}contareceber/"
        payload = {
            "call": "BaixarContaReceber",
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "param": [{"codigo_lancamento": id}]
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Omie: conta a receber {id} baixada com sucesso.")
            return result
        else:
            logger.error(f"Omie: erro ao baixar conta a receber {id}. Status: {response.status_code}, Erro: {response.text}")
            response.raise_for_status()
