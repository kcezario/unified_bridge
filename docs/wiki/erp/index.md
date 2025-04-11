# 🏢 Módulo de ERP (`erp`)

Este módulo é responsável pela integração com sistemas de gestão financeira (ERP), realizando controle de contas a receber.

## 🔗 Provedor atual: [Omie](https://developer.omie.com.br/)

---

## ✅ Funcionalidades Suportadas

- **Criação de contas a receber** (`/financas/contareceber/incluir`)
- **Cancelamento de contas a receber** (`/financas/contareceber/excluir`)
- **Baixa (liquidação) de contas a receber** (`/financas/contareceber/baixar`)

---

## 🧩 Estrutura do Módulo

```
erp/
├── interfaces/                # Contrato da integração
│   └── erp_interface.py
├── erp_client_omie.py         # Integração com a API da Omie
├── erp_service.py             # Lógica de criação, baixa e cancelamento
├── mock/                      # Dados simulados para testes
│   ├── mock_customer.py       # Mocks de clientes
│   ├── mock_receivable.py     # Mocks de contas a receber
│   └── mock_erp_client.py     # Mock do client principal
└── tests/manual/
    └── test_erp_omie.py       # Testes manuais com criação, baixa e exclusão
```

---

## 🧪 Testes Manuais

O script `test_erp_omie.py` executa testes com as três principais ações:

- `criar_conta_receber()`
- `baixar_conta_receber()`
- `cancelar_conta_receber()`

---

## 🔌 Interface Implementada

Arquivo: `erp/interfaces/erp_interface.py`

### Métodos esperados:

- `criar_conta_receber(data: dict) -> dict`
- `baixar_conta_receber(identificador: str, data: dict) -> dict`
- `cancelar_conta_receber(identificador: str) -> dict`

---

## 🧪 Mock para Testes

O mock `mock_erp_client.py` simula todas as chamadas principais com dados dos módulos:

- `mock_customer.py` (clientes)
- `mock_receivable.py` (contas a receber)

---

## 📌 Observações

- O código Omie da conta (`codigo_lancamento_omie`) é persistido após a criação.
- A chave de API e app_key são lidas do `.env`:
  - `OMIE_APP_KEY`
  - `OMIE_APP_SECRET`
- O método `baixar_conta_receber()` exige a data da liquidação e valor.

---

## 📚 Referência Oficial

- [Documentação da API Omie](https://developer.omie.com.br/)