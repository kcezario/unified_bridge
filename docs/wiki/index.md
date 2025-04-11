# 🧠 Documentação Técnica — Unified Bridge

Bem-vindo à documentação técnica do Unified Bridge. Este sistema foi projetado para integrar, de forma modular e transparente, diferentes serviços de pagamentos, emissão de notas fiscais e ERPs.

## 📂 Módulos

### [`payment`](payment/index.md)
Módulo responsável por integração com serviços de **pagamentos**. Atualmente, utiliza o provedor Asaas.

- Geração de cobranças
- Cancelamento
- Webhook de pagamento
- Download de boleto
- Interfaces e testes com mocks

### [`invoice`](invoice/index.md)
Módulo responsável por emissão de **notas fiscais de serviço**. Atualmente, utiliza o provedor NFE.io.

- Emissão e cancelamento de NFSE
- Consulta e download da nota
- Validação de dados do tomador
- Interfaces e testes com mocks

### [`erp`](erp/index.md)
Módulo de integração com **ERP** para controle de contas a receber. Atualmente, utiliza o provedor Omie.

- Criação de contas a receber
- Baixa de liquidação
- Cancelamento de lançamentos
- Interfaces e testes com mocks

---

## 📐 Padrão de implementação

Cada módulo segue uma estrutura comum:

- `interfaces/`: definição das funções esperadas
- `clients/`: integração real com a API externa
- `mock/`: simulação de comportamento para testes
- `services/`: lógica de negócio intermediária
- `tests/manual/`: scripts de testes manuais

---

## 📄 Observações

- As credenciais e configurações dos serviços são injetadas via `.env`.
- Cada integração real possui documentação oficial referenciada na página interna do módulo.

Para detalhes específicos de cada serviço, acesse as páginas dedicadas.
