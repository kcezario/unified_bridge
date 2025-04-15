import os
import requests
from typing import Dict, Any

from app.payables.payables_client_interface import PayablesClientInterface
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SuperlogicaPayablesClient(PayablesClientInterface):
    def __init__(self):
        self.base_url = os.getenv("SUPERLOGICA_BASE_URL")
        self.app_token = os.getenv("SUPERLOGICA_APP_TOKEN")
        self.access_token = os.getenv("SUPERLOGICA_ACCESS_TOKEN")

        if not all([self.base_url, self.app_token, self.access_token]):
            raise EnvironmentError("Superlógica: credenciais não configuradas corretamente.")

    def _headers(self):
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "app_token": self.app_token,
            "access_token": self.access_token,
        }

    def create_payable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Superlógica: criando contas a pagar...")

        url = f"{self.base_url}/v2/condor/MovimentacoesDiretas/"
        response = requests.post(url, headers=self._headers(), data=data)

        if response.status_code != 200:
            logger.error(f"Erro ao criar contas a pagar: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()

    def settle_payable(self, payable_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Superlógica: liquidando contas a pagar ID {payable_id}...")

        url = f"{self.base_url}/v2/condor/MovimentacoesDiretas/post"
        response = requests.put(url, headers=self._headers(), params=data)

        if response.status_code != 200:
            logger.error(f"Erro ao liquidar contas a pagar: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()

    def cancel_payable(self, payable_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Superlógica: cancelando contas a pagar ID {payable_id}...")

        url = f"{self.base_url}/v2/condor/MovimentacoesDiretas/post"
        response = requests.put(url, headers=self._headers(), params=data)

        if response.status_code != 200:
            logger.error(f"Erro ao cancelar contas a pagar: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()

    def upload_attachment(self, file_path: str, condominium_id: str, publish: int = 4) -> Dict[str, Any]:
        """
        Envia um anexo (ex: nota fiscal ou boleto) ao Superlógica.

        Args:
            file_path (str): Caminho do arquivo local.
            condominium_id (str): ID do condomínio.
            publish (int): Regra de publicação (1 a 4). Default: 4 (não publicar).

        Returns:
            dict: Resposta da API com ID do documento enviado.
        """
        logger.info(f"Superlógica: enviando anexo para o condomínio {condominium_id}...")

        url = f"{self.base_url}/v2/condor/documentos?idEmpresa={condominium_id}&publicar={publish}"
        headers = {
            "app_token": self.app_token,
            "access_token": self.access_token,
        }

        with open(file_path, "rb") as f:
            files = {"arquivo": (os.path.basename(file_path), f)}
            response = requests.post(url, headers=headers, files=files)

        if response.status_code != 200:
            logger.error(f"Erro ao enviar anexo: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()
