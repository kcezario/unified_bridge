import os
import requests
from typing import Any, Dict

from erp.erp_client_interface import ERPClientInterface
from schemas.accounts_receivable import AccountsReceivableOmieModel
from utils.logger import get_logger

logger = get_logger(__name__)


class ERPClientOmie(ERPClientInterface):
    def __init__(self):
        config = self.get_config()
        self.base_url = config["base_url"]
        self.app_key = config["app_key"]
        self.app_secret = config["app_secret"]

    def get_config(self) -> Dict[str, Any]:
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

    def get_access_token(self) -> str:
        # A Omie utiliza app_key e app_secret em cada requisição, não há token de acesso separado
        logger.debug("Omie: utilizando app_key e app_secret para autenticação.")
        return "(inline auth)"

    def create_accounts_receivable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug("Omie: criando conta a receber com os dados fornecidos.")
        validated_data = self._validate_input(data)
        payload = self._build_payload("IncluirContaReceber", "conta_receber_cadastro", validated_data)
        response = self._post_to_omie("financas/contareceber/", payload)
        return self._handle_response(response)
    
    def _validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug("Omie: validando dados de entrada.")
        try:
            return AccountsReceivableOmieModel(**data).dict()
        except Exception as e:
            logger.error(f"Omie: validação inválida: {str(e)}")
            raise

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

        # Adiciona o ID ao corpo do lançamento (esperado dentro de conta_receber_cadastro)
        data_with_id = {
            "codigo_lancamento_omie": int(id),  # ou 'codigo_lancamento_integracao' se preferir
            **data
        }

        try:
            validated_data = AccountsReceivableOmieModel(**data_with_id).dict()
        except Exception as e:
            logger.error(f"Omie: falha na validação dos dados para update: {str(e)}")
            raise

        payload = self._build_payload(
            call="AlterarContaReceber",
            wrapper_key="conta_receber_cadastro",
            data=validated_data
        )

        response = self._post_to_omie("financas/contareceber/", payload)
        return self._handle_response(response)


    def settle_accounts_receivable(self, id: str) -> Dict[str, Any]:
        logger.debug(f"Omie: iniciando baixa da conta a receber {id}.")

        # Prepara o corpo mínimo exigido pela Omie
        data = {
            "codigo_lancamento_omie": int(id)  # ou "codigo_lancamento_integracao": id
        }

        payload = self._build_payload(
            call="BaixarContaReceber",
            wrapper_key="conta_receber_cadastro",
            data=data
        )

        response = self._post_to_omie("financas/contareceber/", payload)
        return self._handle_response(response)

