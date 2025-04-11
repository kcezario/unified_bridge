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
- Tratar falhas HTTP e mensagens de erro da API do Asaas

---

## 📌 Métodos implementados

### 1. `create_payment(data: dict) -> dict`

Cria um novo pagamento (cobrança) no Asaas.

- Endpoint:
  ```
  POST /payments
  ```
- Campos esperados no `data`:
  - `customer`: ID do cliente no Asaas (ex: `cus_000001234567`)
  - `billingType`: Tipo de cobrança (`PIX`, `BOLETO`, `CREDIT_CARD`, etc.)
  - `value`: Valor da cobrança (float)
  - `dueDate`: Data de vencimento (formato `YYYY-MM-DD`)
  - `description`: Descrição da cobrança

- Retorna os dados da cobrança criada, incluindo:
  - `id`: Identificador da cobrança
  - `status`, `invoiceUrl`, entre outros

- Lança exceções se a criação falhar (ex: dados incorretos, cliente inválido, autenticação ausente).

---

### 2. `cancel_payment(payment_id: str) -> dict`

Cancela uma cobrança existente, alterando seu status para `"CANCELLED"`.

- Endpoint:
  ```
  PUT /payments/{payment_id}
  ```
- Payload enviado:
  ```json
  { "status": "CANCELLED" }
  ```

- Retorna os dados atualizados da cobrança cancelada.

---

### 3. `get_payment_status(payment_id: str) -> dict`

Consulta os dados e o status atual de uma cobrança.

- Endpoint:
  ```
  GET /payments/{payment_id}
  ```
- Retorna os detalhes completos do pagamento, incluindo status, valor, vencimento, QR Code (se for PIX), e links de boleto.

---

## 🔁 Fluxo de funcionamento

1. O sistema envia uma requisição autenticada com o token da API (`access_token`) no cabeçalho.
2. Os dados da cobrança são enviados no corpo da requisição.
3. O Asaas processa a cobrança e retorna os dados completos da transação.
4. A aplicação pode posteriormente:
   - Consultar o status da cobrança
   - Cancelar a cobrança, se necessário

---

## 🔒 Tratamento de erros

A classe `PaymentClientAsaas` realiza o tratamento completo de falhas:

- Verifica presença da variável `ASAAS_API_KEY` no ambiente
- Verifica status da resposta HTTP (`200` ou `201`)
- Em caso de erro, registra a falha no logger e lança uma exceção com os detalhes do erro retornado pela API

---

## 🧪 Teste manual

O script `tests/manual/test_payment_asaas.py` permite testar:

- Criação de cobrança com dados reais
- Consulta imediata do status
- Cancelamento da cobrança

O log completo da operação é salvo conforme configuração do `LOG_DIR` e `LOG_LEVEL`.

---

Para uma visão geral do módulo de pagamentos e da interface, acesse a página [`index.md`](index.md).