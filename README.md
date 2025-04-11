# Unified Bridge

Integração modular entre sistemas de pagamento, faturamento e ERP.

Este projeto implementa uma camada unificada para comunicação com diferentes serviços externos, como:

- **Asaas**: pagamentos
- **NFE.io**: emissão de notas fiscais de serviço
- **Omie**: contas a receber (ERP)

## 🔧 Requisitos

- Python 3.11+
- Docker (opcional para ambiente isolado)
- Variáveis de ambiente definidas (ver `.env.example`)

## ▶️ Executando localmente

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure o `.env` a partir do exemplo:
   ```bash
   cp .env.example .env
   ```

3. Rode a aplicação (modo exemplo):
   ```bash
   python -m app.tests.manual.main
   ```

## 🧪 Testes

- Testes manuais:
  ```bash
  python -m app.tests.manual.test_invoice_nfe_io
  ```

- Testes unitários (se aplicável):
  ```bash
  pytest
  ```

## 📚 Documentação técnica

Toda a documentação dos serviços e integrações está disponível na wiki interna do projeto:

👉 [Acesse a documentação técnica completa](docs/wiki/index.md)

---

## 🧱 Estrutura modular

O sistema está dividido em três domínios principais:

- [`payment/`](docs/wiki/payment/index.md)
- [`invoice/`](docs/wiki/invoice/index.md)
- [`erp/`](docs/wiki/erp/index.md)

Cada módulo implementa uma interface padrão, com opção de mocks para testes manuais e integração com provedores reais via client API.

---

## 🛠️ Em desenvolvimento
```