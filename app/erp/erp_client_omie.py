import os
import json
import requests

from typing import Any, Dict

from app.erp.erp_client_interface import ERPClientInterface
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ERPClientOmie(ERPClientInterface):
    """
    Cliente responsável por integração com a API do Omie (Contas a Receber).

    Esta classe encapsula os principais métodos para comunicação com a API REST da Omie
    relacionados à gestão de contas a receber. Permite criar, atualizar e dar baixa
    em lançamentos financeiros.

    Requisitos:
        - Variáveis de ambiente:
            - OMIE_APP_KEY
            - OMIE_APP_SECRET
            - OMIE_BASE_URL
            - OMIE_DEFAULT_ACCOUNT_ID (opcional para baixa)

    Métodos principais:
        - create_accounts_receivable()
        - update_accounts_receivable()
        - settle_accounts_receivable()
    """
    
    def __init__(self):
        config = self._get_config()
        self.base_url = config["base_url"]
        self.app_key = config["app_key"]
        self.app_secret = config["app_secret"]
        self.default_account_id = config["default_account_id"]

    def _get_config(self) -> Dict[str, Any]:
        logger.debug("Omie: carregando configurações do ambiente.")
        config = {
            "app_key": os.getenv("OMIE_APP_KEY"),
            "app_secret": os.getenv("OMIE_APP_SECRET"),
            "base_url": os.getenv("OMIE_BASE_URL"),
            "default_account_id": os.getenv("OMIE_DEFAULT_ACCOUNT_ID")
        }

        if not config["app_key"] or not config["app_secret"]:
            logger.error("Omie: OMIE_APP_KEY ou OMIE_APP_SECRET não configurados.")
            raise EnvironmentError("Credenciais da Omie não configuradas.")

        return config
    
    def _build_payload(self, call: str, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug(f"Omie: construindo payload para chamada {call}.")
        return {
            "call": call,
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "param": [data]
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

    def create_accounts_receivable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo lançamento no Contas a Receber da Omie.

        Args:
            data (Dict[str, Any]): Dados do lançamento, incluindo:
                - codigo_lancamento_integracao (str): Identificador único gerado pelo integrador.
                - codigo_cliente_fornecedor (int/str): Código do cliente ou fornecedor cadastrado no Omie.
                - data_vencimento (str): Data de vencimento no formato "dd/mm/aaaa".
                - valor_documento (float/str): Valor do título.
                - codigo_categoria (str): Código da categoria financeira.
                - data_previsao (str): Data prevista de pagamento/recebimento.
                - id_conta_corrente (int/str): ID da conta corrente a ser associada.
                - observacao (str): Campo opcional para observações.

        Returns:
            Dict[str, Any]: Resposta da API contendo os códigos do lançamento ou erro.
        """
        
        logger.debug("Omie: criando conta a receber com os dados fornecidos.")
        logger.debug(f"Omie: dados recebidos:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
        for field in [
            "codigo_cliente_fornecedor",
            "valor_documento",
            "id_conta_corrente"
        ]:
            if field in data:
                data[field] = str(data[field])

        payload = self._build_payload("IncluirContaReceber", data)
        response = self._post_to_omie("financas/contareceber/", payload)
        return self._handle_response(response)

    def update_accounts_receivable(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza um lançamento existente no Contas a Receber.

        Args:
            id (str): Código do lançamento (`codigo_lancamento_omie`) a ser atualizado.
            data (Dict[str, Any]): Campos a serem atualizados. Exemplo:
                - observacao (str): Nova observação para o título.

        Returns:
            Dict[str, Any]: Resposta da API com a confirmação da atualização.
        """
        
        logger.debug(f"Omie: iniciando atualização da conta a receber {id}.")

        data_with_id = {
            "codigo_lancamento_omie": int(id),
            **data
        }

        payload = self._build_payload(
            call="AlterarContaReceber",
            data=data_with_id
        )

        response = self._post_to_omie("financas/contareceber/", payload)
        return self._handle_response(response)


    def settle_accounts_receivable(
        self,
        id: str,
        valor: str,
        conta_corrente_id: str,
        data: str
    ) -> Dict[str, Any]:
        
        """
        Realiza a baixa de um título em aberto no Contas a Receber da Omie.

        Args:
            id (str): Código do lançamento (`codigo_lancamento`) a ser baixado.
            account_id (str, optional): ID da conta corrente. Caso não informado, será usada a conta padrão definida no ambiente.

        Returns:
            Dict[str, Any]: Resposta da API com os dados da baixa, incluindo valor baixado e status de liquidação.
        """
    
        logger.debug(f"Omie: iniciando baixa da conta a receber {id}.")

        payload_data = {
            "codigo_lancamento": int(id),
            "codigo_conta_corrente": conta_corrente_id,
            "valor": valor,
            "data": data,
            "observacao": "Baixa automática via API"
        }

        payload = self._build_payload(
            call="LancarRecebimento",
            data=payload_data
        )

        response = self._post_to_omie("financas/contareceber/", payload)
        return self._handle_response(response)

