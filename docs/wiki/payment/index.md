# 💳 Módulo de Pagamento (`payment`)

Este módulo é responsável pela integração com provedores de pagamento, atualmente utilizando a API do **Asaas** para geração e controle de cobranças via boleto bancário.

## 🔗 Provador atual: [Asaas](https://docs.asaas.com/)

---

## ✅ Funcionalidades Suportadas

- **Geração de cobrança** (`POST /payments`)
- **Cancelamento de cobrança** (`DELETE /payments/{id}`)
- **Download de boleto** (`GET /payments/{id}/identificationField`)
- **Validação de pagamento via Webhook** (`POST /payments/webhook`)

---

## 🧩 Estrutura do Módulo

```
payment/
├── interfaces/                 # Contratos base de integração
│   └── payment_interface.py
├── payment_client_asaas.py    # Integração real com a API do Asaas
├── payment_service.py         # Lógica de negócio de pagamento
├── mock/                      # Mocks para testes
│   └── mock_payment_client.py
└── tests/manual/              # Scripts para testes manuais
    └── test_payment_asaas.py
```

---

## 🧪 Testes Manuais

O script `test_payment_asaas.py` permite:

- Criar cobrança de teste
- Cancelar cobrança
- Testar download de boleto
- Simular recebimento de webhook

---

## 🧾 Interface Implementada

Arquivo: `payment/interfaces/payment_interface.py`

### Métodos esperados:

- `create_charge(data: dict) -> dict`
- `cancel_charge(charge_id: str) -> None`
- `get_boleto_link(charge_id: str) -> str`
- `handle_webhook(payload: dict) -> None`

---

## 🧪 Mock para Testes

O mock implementado em `mock/mock_payment_client.py` simula todos os métodos da interface principal com dados estáticos ou randomizados.

---

## 📌 Observações

- O client real (`payment_client_asaas.py`) utiliza a variável `ASAAS_API_KEY` do `.env`.
- O webhook é validado apenas com base no `event` recebido.

---

## 📚 Referência Oficial

- [Documentação da API Asaas](https://docs.asaas.com/)
