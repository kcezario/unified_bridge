# 🔗 Integração Invoice — NFE.io

Este documento descreve a integração real do Unified Bridge com a **NFE.io**, provedor de emissão de **Notas Fiscais de Serviço Eletrônicas (NFSE)**.

A comunicação com a NFE.io é feita via **API REST** autenticada por chave de API (`Authorization`) e associada a uma `company_id`.

---

## ⚙️ Configuração

A integração exige a definição das seguintes variáveis de ambiente no `.env`:

```env
NFE_IO_API_KEY=         # Chave da API da NFE.io
NFE_IO_COMPANY_ID=      # ID da empresa emissora configurada na plataforma NFE.io
NFE_IO_BASE_URL=        # Base da API, normalmente https://api.nfse.io/v1
```

---

## 📁 Estrutura do Cliente

Arquivo: `invoice_client_nfe_io.py`  
Classe principal: `InvoiceClientNFEio`

Responsável por:

- Montar payloads de emissão de NFSE com campos obrigatórios e opcionais
- Realizar chamadas autenticadas à API REST da NFE.io
- Validar dados do tomador de serviço (borrower)
- Tratar respostas HTTP e erros lógicos
- Realizar cancelamento, consulta de status e download em PDF das notas fiscais emitidas

---

## 📌 Métodos implementados

### 1. `create_data(...) -> dict`

Método auxiliar que prepara o dicionário com os dados para a emissão da NFSE.

- Obtém e valida os dados do tomador de serviço (`borrower`)
- Verifica presença dos campos obrigatórios:
  - `cityServiceCode`
  - `description`
  - `servicesAmount`
  - `taxationType`
- Processa e inclui campos opcionais válidos automaticamente (ex: `issuedOn`, `externalId`)

Este método deve ser utilizado **antes** de chamar `issue_invoice`.

---

### 2. `issue_invoice(data: dict) -> dict`

Envia o payload gerado para a API da NFE.io e realiza a emissão da nota fiscal.

- Endpoint:  
  ```
  POST /companies/{company_id}/serviceinvoices
  ```
- Requer o dicionário completo com tomador, serviço, código da cidade, valores e impostos.
- Retorna o corpo da resposta da API, incluindo o `id` da nota emitida.
- Lança exceções caso a emissão falhe (status diferente de 202).

---

### 3. `cancel_invoice(invoice_id: str) -> dict`

Solicita o **cancelamento** de uma NFSE emitida.

- Endpoint:
  ```
  DELETE /companies/{company_id}/serviceinvoices/{invoice_id}
  ```
- Retorna os dados da nota cancelada ou erro, caso o ID não exista ou não possa ser cancelado.

---

### 4. `get_invoice_status(invoice_id: str) -> dict`

Consulta os **detalhes e status atual** de uma NFSE.

- Endpoint:
  ```
  GET /companies/{company_id}/serviceinvoices/{invoice_id}
  ```
- Retorna os dados da nota, incluindo status atual, data de emissão, tomador, valores e impostos.

---

### 5. `download_invoice(invoice_id: str) -> dict`

Obtém o **PDF da nota fiscal de serviço (NFSE)** emitida.

- Endpoint:
  ```
  GET /companies/{company_id}/serviceinvoices/{invoice_id}/pdf
  ```
- Requer apenas o `invoice_id` válido e retorna o conteúdo em base64 ou link para download.
- Em caso de sucesso, retorna:
  ```json
  {
    "pdf": "<base64_encoded_content>"
  }
  ```
- Em caso de falha, a API pode retornar códigos `401`, `404`, `500`, entre outros.

---

## 📐 Validações

As validações de entrada são feitas por funções auxiliares localizadas em `utils/validators.py`, garantindo que os campos obrigatórios e os enumeradores estejam corretos:

- Validação do `borrower`:
  - Tipo (`type`)
  - Regime tributário (`taxRegime`)
  - Endereço (`address.country`, `address.city.code`, `state`, etc.)

- Validação do serviço:
  - `cityServiceCode`, `description`, `servicesAmount`, `taxationType`
  - Verificação de estrutura dos campos opcionais via `OPTIONAL_FIELDS`

---

## 🌍 Mocks e Testes Combinatórios

A pasta `mocks/` contém:

- `borrowers.py`: tomadores de serviço simulados com diferentes níveis de preenchimento de dados.
- `services.py`: serviços simulados com conjuntos mínimos, recomendados e completos.

Estes mocks são utilizados no script de teste manual:

- `tests/manual/test_invoice_nfe_io.py`

Esse script realiza **testes combinatórios** entre tomadores e serviços simulados, para garantir cobertura em múltiplos cenários.

---

## 🔒 Tratamento de erros

A classe `InvoiceClientNFEio` realiza tratamento completo de falhas:

- Verifica presença de variáveis de ambiente obrigatórias
- Lança exceções claras para:
  - Erros de estrutura dos dados (`ValueError`)
  - Erros de autenticação e rede (`requests.HTTPError`)
  - Falhas lógicas retornadas pela NFE.io

Todos os erros são registrados no sistema de logs, com nível `ERROR` ou `WARNING`.

---

Para uma visão geral do módulo `invoice` e sua interface, consulte a página [`index.md`](index.md).