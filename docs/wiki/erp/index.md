# 🧾 Módulo ERP — Visão Geral

Este módulo é responsável pela integração com sistemas de **ERP**, permitindo o controle de **contas a receber** dentro da arquitetura do Unified Bridge.

Atualmente, o sistema suporta dois tipos de cliente ERP:

- `mock`: usado para testes e validação local
- `omie`: integração real com a API do Omie

---

## 🧩 Estrutura

- `erp_client_interface.py`: define a interface padrão para qualquer cliente ERP.
- `erp_client_mock.py`: implementação mock para simular comportamento do ERP sem dependência externa.
- `erp_client_omie.py`: cliente real que se comunica com a API REST da Omie.
- `tests/manual/test_erp_omie.py`: script manual para testar criação, atualização e baixa de contas a receber.

---

## 🔌 Interface: `ERPClientInterface`

A interface define os seguintes métodos obrigatórios:

```python
class ERPClientInterface(ABC):
    def create_accounts_receivable(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo lançamento de contas a receber."""
        pass

    def update_accounts_receivable(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um lançamento de contas a receber existente."""
        pass

    def settle_accounts_receivable(self, id: str) -> Dict[str, Any]:
        """Dá baixa (marca como pago) em um lançamento de contas a receber."""
        pass
```

Essa padronização permite alternar facilmente entre implementações reais e simuladas, sem alterar a lógica de negócio.

---

## 🧪 Implementação Mock

O `ERPClientMock` simula um ambiente de ERP com as seguintes características:

- Armazena lançamentos de contas a receber em memória (`dict`).
- Gera IDs incrementais (`ar-1`, `ar-2`, ...).
- Permite criar, atualizar e baixar lançamentos.
- Valida presença de campos obrigatórios como:
  - `codigo_cliente_fornecedor`
  - `data_vencimento`
  - `valor_documento`
  - `codigo_categoria`
  - `id_conta_corrente`

A autenticação é simulada via token gerado a partir de variáveis de ambiente:

```env
MOCK_ERP_APP_KEY=...
MOCK_ERP_APP_SECRET=...
```

Este mock é utilizado nos testes manuais e em ambientes locais ou de desenvolvimento para garantir independência da API externa.

---

Para detalhes sobre a integração real com o Omie, acesse [`omie.md`](omie.md).