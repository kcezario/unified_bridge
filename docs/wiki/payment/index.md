# 💰 Módulo Payment — Visão Geral

Este módulo é responsável pela **integração com serviços de pagamento**, permitindo que o Unified Bridge gere, consulte, cancele e valide cobranças de forma padronizada e desacoplada.

Atualmente, o sistema suporta dois tipos de cliente:

- `mock`: utilizado para testes manuais e ambientes de desenvolvimento
- `asaas`: integração real com o provedor de pagamentos **Asaas**

---

## 🧩 Estrutura

- `payment_client_interface.py`: define a interface base que todo cliente de pagamento deve implementar.
- `payment_client_mock.py`: implementação mock que simula o comportamento de pagamentos reais.
- `payment_client_asaas.py`: cliente real que se comunica com a API pública da Asaas.
- `constants/asaas_constants.py`: enums e listas de campos para validação e extração de webhooks.
- `utils/validators.py`: validação de payloads para criação e atualização de cobranças.
- `tests/manual/test_payment_asaas.py`: script para teste manual do fluxo completo com o Asaas.

---

## 🔌 Interface: `PaymentClientInterface`

A interface define os seguintes métodos obrigatórios:

```python
class PaymentClientInterface(ABC):
    def create_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera um novo pagamento (ex: boleto, pix, cartão)."""
        pass

    def cancel_payment(self, payment_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cancela um pagamento existente."""
        pass

    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Consulta o status de um pagamento."""
        pass

    def handle_payment_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Processa um webhook recebido da plataforma de pagamento."""
        pass
```

Essa padronização permite que qualquer cliente de pagamento possa ser intercambiado com segurança e sem alteração na lógica do sistema principal.

---

## 🧪 Implementação Mock

O `PaymentClientMock` simula a criação e cancelamento de pagamentos com as seguintes características:

- Armazena pagamentos em memória (`dict`) com status como `pending`, `cancelled`, `paid` ou `failed`.
- Gera IDs incrementais (`pay-1`, `pay-2`, ...).
- Valida os campos obrigatórios no momento da criação:
  - `customer_id`
  - `amount`
  - `due_date`
- Simula recebimento de webhooks com eventos como `payment_confirmed` e `payment_failed`.

A autenticação é simulada por meio de um token baseado em variável de ambiente:

```env
MOCK_PAYMENT_API_KEY=...
```

Esse mock é ideal para testes manuais e desenvolvimento local sem dependência externa.

---

Para detalhes sobre a integração real com o provedor Asaas, acesse [`asaas.md`](asaas.md).