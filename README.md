# 🧠 Unified Bridge

**Unified Bridge** é uma aplicação modular que unifica a comunicação com provedores externos de **pagamentos**, **emissão de notas fiscais** e **ERPs**, abstraindo a complexidade de cada serviço em uma arquitetura extensível e desacoplada.

---

## 📌 Visão Geral

Este projeto foi desenvolvido com o objetivo de centralizar integrações críticas de negócio em uma única ponte unificadora. Através de interfaces padronizadas e clientes intercambiáveis (mock ou real), é possível alternar entre provedores sem alterar a lógica de negócio.

---

## 🔧 Funcionalidades

- Integração com múltiplos provedores:
  - 📄 Notas Fiscais: [NFE.io](https://nfe.io/)
  - 💰 Pagamentos: [Asaas](https://asaas.com/)
  - 📊 ERP: [Omie](https://omie.com.br/)

- Arquitetura orientada a interfaces, com suporte a:
  - Mocks para ambientes de desenvolvimento
  - Testes manuais independentes por domínio
  - Validação automática de dados de entrada

---

## 🗂 Estrutura de pastas

```bash
app/
├── core/           # Fábrica de clientes e lógica central
├── erp/            # Integração com sistemas ERP (Omie, Mock)
├── invoice/        # Emissão de NFSE (NFE.io, Mock)
├── payment/        # Geração e consulta de pagamentos (Asaas, Mock)
├── mocks/          # Dados simulados para testes
├── tests/manual/   # Scripts de teste manuais
├── utils/          # Logger, validações e handlers
└── config/         # Configurações e arquivos auxiliares
```

---

## 📖 Documentação

A documentação técnica completa está disponível em:

📚 [`docs/wiki/index.md`](docs/wiki/index.md)

Ela está organizada por módulo:

- [`docs/wiki/erp/`](docs/wiki/erp/index.md)
- [`docs/wiki/invoice/`](docs/wiki/invoice/index.md)
- [`docs/wiki/payment/`](docs/wiki/payment/index.md)

Cada seção cobre:
- Visão geral
- Interface implementada
- Cliente mock
- Integrações reais com provedores

---

## 🚀 Requisitos

- Python 3.10+
- `pip install -r requirements.txt`
- Configurar variáveis de ambiente (veja `.env.example`)

---

## 🧪 Testes manuais

Todos os módulos possuem testes manuais organizados em `app/tests/manual/`, permitindo validação sem necessidade de interface gráfica ou front-end.

---

## 🛠 Desenvolvimento

Ambientes de desenvolvimento podem usar os **clientes mock** via `.env`:

```env
ERP_CLIENT=mock
INVOICE_CLIENT=mock
PAYMENT_CLIENT=mock
```