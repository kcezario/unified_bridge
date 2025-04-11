# 🧠 Documentação Técnica — Unified Bridge

Bem-vindo à documentação técnica do Unified Bridge. Este sistema foi projetado para integrar, de forma modular e transparente, diferentes serviços de pagamentos, emissão de notas fiscais e ERPs.

## 📂 Módulos

### [`payment`](payment/index.md)
Módulo responsável pela integração com serviços de **pagamento**. Atualmente, utiliza o provedor **Asaas**.

- Geração de cobranças (PIX, boleto, cartão)
- Cancelamento de cobranças
- Consulta de status de pagamento
- Interfaces e testes com mocks

### [`invoice`](invoice/index.md)
Módulo responsável pela emissão de **notas fiscais de serviço (NFSE)**. Atualmente, utiliza o provedor **NFE.io**.

- Emissão e cancelamento de NFSE
- Consulta de status da nota fiscal
- Validação dos dados do tomador de serviço
- Interfaces e testes com mocks
- Testes combinatórios com mocks de tomadores e serviços

### [`erp`](erp/index.md)
Módulo de integração com sistemas de **ERP** para controle de contas a receber. Atualmente, utiliza o provedor **Omie**.

- Criação de contas a receber
- Atualização de lançamentos
- Baixa de liquidação (recebimento)
- Interfaces e testes com mocks

---

## 📐 Padrão de implementação

Cada módulo segue uma estrutura comum:

- `interface/`: definição da interface esperada
- `client/`: implementação real da integração com a API externa
- `mock/`: simulação de comportamento para testes
- `tests/manual/`: scripts de testes manuais
- `utils/`: funções auxiliares e validações

---

## 📄 Observações

- As credenciais e configurações dos serviços são carregadas via variáveis de ambiente no `.env`.
- Cada integração real segue a documentação oficial do provedor, referenciada na respectiva página do módulo.
- Os logs são gerados com base no nível definido por `LOG_LEVEL` e armazenados em `LOG_DIR`, conforme definido no ambiente.

Para detalhes específicos de cada serviço, acesse as páginas dedicadas.