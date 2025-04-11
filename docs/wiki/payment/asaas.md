# 🔗 Integração Payment — Asaas

Este documento descreve a integração real do Unified Bridge com o **Asaas**, provedor de pagamentos utilizado para geração, consulta e cancelamento de cobranças via **PIX**, **boleto bancário** e **cartão de crédito**.

A comunicação com o Asaas é feita via **API REST**, utilizando autenticação via token (`access_token`) no cabeçalho.

---

## ⚙️ Configuração

A integração com o Asaas exige a configuração das seguintes variáveis de ambiente no `.env`:

```env
ASAAS_API_KEY=       # Token de acesso fornecido pelo Asaas
ASAAS_BASE_URL=      # Base da API (ex: https://sandbox.asaas.com/api/v3)
```

---

## 📁 Estrutura do Cliente

Arquivo: `payment_client_asaas.py`  
Classe principal: `PaymentClientAsaas`

Responsável por:

- Montar requisições autenticadas com `access_token`
- Criar cobranças para clientes previamente cadastrados no Asaas
- Cancelar cobranças existentes
- Consultar o status de pagamentos ativos
- Processar webhooks de pagamento
- Tratar falhas HTTP e mensagens de erro da API do Asaas

---

## 📌 Métodos implementados

### 1. `create_payment(data: dict) -> dict`

Cria um novo pagamento (cobrança) no Asaas.

- Endpoint:
  ```
  POST /payments
  ```
- Campos obrigatórios:
  - `customer`: ID do cliente no Asaas (ex: `cus_000001234567`)
  - `value`: Valor da cobrança
  - `dueDate`: Data de vencimento (`YYYY-MM-DD`)
  - `billingType`: Tipo de cobrança (`PIX`, `BOLETO`, `CREDIT_CARD`)  
    > *Se não fornecido, assume-se `BOLETO` por padrão.*
- Campos opcionais: `description`, `externalReference`, `discount`, `interest`, `fine`, `split`, etc.

- Retorna os dados da cobrança criada, incluindo:
  - `id`, `status`, `invoiceUrl`, `bankSlipUrl`, entre outros.

---

### 2. `cancel_payment(payment_id: str, data: dict) -> dict`

Cancela uma cobrança existente, alterando seu status para `"CANCELLED"`.

- Endpoint:
  ```
  PUT /payments/{payment_id}
  ```
- Payload obrigatório:
  - `status`: `"CANCELLED"`
  - Além disso, os seguintes campos são exigidos para compatibilidade com a API:
    - `value`, `dueDate`, `billingType`

- Retorna os dados atualizados da cobrança cancelada.

---

### 3. `get_payment_status(payment_id: str) -> dict`

Consulta os dados e o status atual de uma cobrança.

- Endpoint:
  ```
  GET /payments/{payment_id}/status
  ```
- Retorna os detalhes da cobrança, incluindo status atual, QR Code (PIX), links de boleto, etc.

---

### 4. `handle_payment_webhook(payload: dict) -> dict`

Processa um webhook recebido do Asaas e extrai os campos relevantes.

- Espera receber o payload bruto enviado pelo Asaas
- Os campos relevantes são definidos em `WEBHOOK_PAYMENT_FIELDS`
- Retorna um `dict` com os dados planos extraídos

---

## 🔁 Fluxo de funcionamento

1. O sistema envia uma requisição autenticada com o token da API (`access_token`) no cabeçalho.
2. Os dados da cobrança são enviados no corpo da requisição.
3. O Asaas processa a cobrança e retorna os dados completos da transação.
4. A aplicação pode:
   - Consultar o status da cobrança
   - Cancelar a cobrança
   - Processar o webhook ao receber notificações assíncronas do Asaas

---

## 🔒 Tratamento de erros

A classe `PaymentClientAsaas` realiza o tratamento completo de falhas:

- Verifica presença das variáveis de ambiente obrigatórias
- Lança exceções para status HTTP diferentes de 200/201
- Valida os dados enviados com base no contexto (`create`, `update`)
- Registra todos os erros no log

---

## 🧪 Teste manual

O script `tests/manual/test_payment_asaas.py` permite testar:

- Criação de cobrança com dados reais
- Consulta imediata do status
- Cancelamento da cobrança

> O log completo da operação é salvo conforme configuração do `LOG_DIR` e `LOG_LEVEL`.

---

Para uma visão geral do módulo de pagamentos e da interface, acesse a página [`index.md`](index.md).