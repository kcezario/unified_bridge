# 🧾 Módulo Invoice — Visão Geral

Este módulo é responsável pela **emissão de Notas Fiscais de Serviço Eletrônicas (NFSE)**, permitindo que o Unified Bridge se comunique com provedores fiscais de forma padronizada.

Atualmente, o sistema suporta dois tipos de cliente:

- `mock`: usado para simulação de emissão e testes manuais
- `nfe_io`: integração real com a API pública da NFE.io

---

## 🧩 Estrutura

- `invoice_client_interface.py`: define a interface padrão para qualquer cliente de emissão de nota.
- `invoice_client_mock.py`: implementação mock para simular comportamento de emissão sem dependência externa.
- `invoice_client_nfe_io.py`: cliente real que se comunica com a API REST da NFE.io.
- `utils/validators.py`: funções auxiliares para validação de campos obrigatórios e enums.
- `tests/manual/test_invoice_nfe_io.py`: script manual para testar emissão, consulta e download de notas com dados simulados.
- `mocks/`: contém tomadores (`borrowers.py`) e serviços (`services.py`) para testes combinatórios.

---

## 🔌 Interface: `InvoiceClientInterface`

A interface define os seguintes métodos obrigatórios:

```python
class InvoiceClientInterface(ABC):
    def issue_invoice(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Emite uma nova nota fiscal."""
        pass

    def cancel_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Cancela uma nota fiscal existente."""
        pass

    def get_invoice_status(self, invoice_id: str) -> Dict[str, Any]:
        """Consulta o status de uma nota fiscal."""
        pass

    def download_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Obtém o link ou conteúdo em PDF da nota fiscal emitida."""
        pass
```

Essa padronização permite alternar facilmente entre diferentes provedores de nota fiscal, sem alterar a lógica principal do sistema.

---

## 🧪 Implementação Mock

O `InvoiceClientMock` simula a emissão, cancelamento e download de notas fiscais com as seguintes características:

- Armazena notas fiscais em memória (`dict`) com status como `issued` ou `cancelled`.
- Gera IDs incrementais (`inv-1`, `inv-2`, ...).
- Valida presença de campos obrigatórios:
  - `customer_id`
  - `amount`
  - `service_description`
- Simula o download da nota com um link fictício:

```python
{
  "status": "success",
  "invoice_id": "inv-1",
  "pdf_url": "https://mock-invoice.local/pdf/inv-1.pdf"
}
```

A autenticação é simulada por um token gerado a partir de uma variável de ambiente:

```env
MOCK_INVOICE_API_KEY=...
```

Esse mock é usado em ambientes de desenvolvimento e para testes locais, garantindo independência da API real.

---

Para detalhes sobre a integração real com o provedor NFE.io, acesse [`nfe_io.md`](nfe_io.md).