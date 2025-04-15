import os
from typing import Any, Dict
from app.payables.payables_client_interface import PayablesClientInterface
from app.utils.logger import get_logger

logger = get_logger(__name__)

class PayablesClientMock(PayablesClientInterface):
    def __init__(self):
        self._payables = {}

    def create_payable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("MockPayables: criando conta a pagar.")
        payable_id = f"payable-{len(self._payables) + 1}"
        self._payables[payable_id] = {**data, "status": "open", "id": payable_id}
        return {"status": "success", "payable_id": payable_id}

    def settle_payable(self, payable_id: str) -> Dict[str, Any]:
        if payable_id not in self._payables:
            return {"status": "not_found"}
        self._payables[payable_id]["status"] = "settled"
        return {"status": "success", "payable_id": payable_id}

    def cancel_payable(self, payable_id: str) -> Dict[str, Any]:
        if payable_id not in self._payables:
            return {"status": "not_found"}
        self._payables[payable_id]["status"] = "cancelled"
        return {"status": "success", "payable_id": payable_id}
