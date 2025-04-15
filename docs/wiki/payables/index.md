# 🧾 Módulo Payables — Visão Geral

Este módulo gerencia a **criação e controle de contas a pagar** para integrações com sistemas externos, como o Superlógica.

---

## 🧩 Estrutura

- `payables_client_interface.py`: define a interface que todas as integrações devem seguir.
- `payables_client_mock.py`: simula lançamentos de contas a pagar para testes.
- `superlogica.md`: documentação da integração real (em desenvolvimento).

---

## 🔌 Interface: `PayablesClientInterface`

```python
class PayablesClientInterface(ABC):
    def create_payable(self, data: Dict[str, Any]) -> Dict[str, Any]: ...
    def settle_payable(self, payable_id: str) -> Dict[str, Any]: ...
    def cancel_payable(self, payable_id: str) -> Dict[str, Any]: ...
```

Essa padronização garante que diferentes integrações possam ser intercambiadas sem alterar a lógica central do sistema.

---

Para detalhes sobre a integração com o Superlógica, acesse [`superlogica.md`](superlogica.md).