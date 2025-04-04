import os
import requests
from typing import Any, Dict

from app.erp.erp_client_interface import ERPClientInterface
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ERPClientOmie(ERPClientInterface):
    def __init__(self):
        config = self._get_config()
        self.base_url = config["base_url"]
        self.app_key = config["app_key"]
        self.app_secret = config["app_secret"]

    def _get_config(self) -> Dict[str, Any]:
        logger.debug("Omie: carregando configurações do ambiente.")
        config = {
            "app_key": os.getenv("OMIE_APP_KEY"),
            "app_secret": os.getenv("OMIE_APP_SECRET"),
            "base_url": os.getenv("OMIE_BASE_URL", "https://app.omie.com.br/api/v1/")
        }

        if not config["app_key"] or not config["app_secret"]:
            logger.error("Omie: OMIE_APP_KEY ou OMIE_APP_SECRET não configurados.")
            raise EnvironmentError("Credenciais da Omie não configuradas.")

        return config
    
    def create_accounts_receivable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug("Omie: criando conta a receber com os dados fornecidos.")
        payload = self._build_payload("IncluirContaReceber", "conta_receber_cadastro", data)
        response = self._post_to_omie("financas/contareceber/", payload)
        return self._handle_response(response)
    
    def _build_payload(self, call: str, wrapper_key: str, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug(f"Omie: construindo payload para chamada {call}.")
        return {
            "call": call,
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "param": [{wrapper_key: data}]
        }

    def _post_to_omie(self, path: str, payload: Dict[str, Any]) -> requests.Response:
        url = f"{self.base_url}{path}"
        logger.debug(f"Omie: POST para {url} com payload: {payload}")
        return requests.post(url, json=payload)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code != 200:
            logger.error(f"Omie: erro HTTP {response.status_code} - {response.text}")
            response.raise_for_status()

        result = response.json()
        if "faultstring" in result:
            logger.error(f"Omie: erro lógico da API: {result['faultstring']}")
            raise ValueError(result["faultstring"])

        logger.info(f"Omie: operação concluída com sucesso. Resposta: {result}")
        return result

    def update_accounts_receivable(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug(f"Omie: iniciando atualização da conta a receber {id}.")

        data_with_id = {
            "codigo_lancamento_omie": int(id),
            **data
        }

        payload = self._build_payload(
            call="AlterarContaReceber",
            wrapper_key="conta_receber_cadastro",
            data=data_with_id
        )

        response = self._post_to_omie("financas/contareceber/", payload)
        return self._handle_response(response)


    def settle_accounts_receivable(self, id: str) -> Dict[str, Any]:
        logger.debug(f"Omie: iniciando baixa da conta a receber {id}.")

        data = {
            "codigo_lancamento_omie": int(id)
        }

        payload = self._build_payload(
            call="BaixarContaReceber",
            wrapper_key="conta_receber_cadastro",
            data=data
        )

        response = self._post_to_omie("financas/contareceber/", payload)
        return self._handle_response(response)

