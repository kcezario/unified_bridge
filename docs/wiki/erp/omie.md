# 🔗 Integração ERP — Omie

Este documento descreve a integração real do Unified Bridge com o **Omie**, provedor ERP utilizado para controle de **Contas a Receber**.

A comunicação com o Omie é feita através da **API REST** pública, com autenticação por `app_key` e `app_secret`. Todas as chamadas são feitas via POST e seguem o modelo de payload estabelecido pelo Omie, com os campos agrupados dentro da chave `param`.

---

## ⚙️ Configuração

A integração exige a configuração das seguintes variáveis de ambiente no `.env`:

```env
OMIE_APP_KEY=           # Chave da aplicação fornecida pelo Omie
OMIE_APP_SECRET=        # Segredo da aplicação fornecido pelo Omie
OMIE_BASE_URL=          # Base da API (ex: https://app.omie.com.br/api/v1/)
OMIE_DEFAULT_ACCOUNT_ID=# ID da conta corrente padrão (opcional, usada na baixa)
```

---

## 📁 Estrutura do Cliente

Arquivo: `erp_client_omie.py`  
Classe principal: `ERPClientOmie`

Responsável por:

- Montar payloads conforme especificações do Omie
- Executar chamadas HTTP POST com dados autenticados
- Tratar erros lógicos e HTTP retornados pela API
- Encapsular a lógica de negócio relacionada a **contas a receber**

---

## 📌 Métodos implementados

### 1. `create_accounts_receivable(data: dict) -> dict`

Cria um novo lançamento de conta a receber no sistema do Omie.

- Requer campos obrigatórios como:
  - `codigo_lancamento_integracao`
  - `codigo_cliente_fornecedor`
  - `valor_documento`
  - `data_vencimento`
  - `codigo_categoria`
  - `id_conta_corrente`

- Faz a chamada com o método `IncluirContaReceber` para o endpoint:
  ```
  {OMIE_BASE_URL}/financas/contareceber/
  ```

- Retorna os dados da criação, incluindo o `codigo_lancamento_omie` atribuído pela Omie.

---

### 2. `update_accounts_receivable(id: str, data: dict) -> dict`

Atualiza dados de um lançamento de conta a receber já existente.

- O campo `id` representa o `codigo_lancamento_omie`.
- O campo `data` contém os valores a serem atualizados (ex: `observacao`).
- Usa o método `AlterarContaReceber` da API Omie.

---

### 3. `settle_accounts_receivable(id: str, valor: str, conta_corrente_id: str, data: str) -> dict`

Efetua a **baixa** (liquidação) de um título aberto no contas a receber.

- Requer os seguintes dados:
  - `id`: `codigo_lancamento` do título
  - `valor`: valor da baixa
  - `conta_corrente_id`: ID da conta corrente (pode usar `OMIE_DEFAULT_ACCOUNT_ID`)
  - `data`: data da baixa no formato `dd/mm/aaaa`

- Faz a chamada com o método `LancarRecebimento`.

---

## 🔄 Fluxo de funcionamento

1. **Autenticação**: todas as chamadas usam `app_key` e `app_secret`, enviados diretamente no corpo do payload.
2. **Encapsulamento do método**:
   - O método da API (ex: `IncluirContaReceber`) é informado na chave `call`.
   - Os dados são passados como um dicionário dentro da lista `param`.
3. **Resposta**:
   - Em caso de sucesso, a resposta retorna dados como `codigo_lancamento_omie`, `codigo_lancamento_integracao`, entre outros.
   - Em caso de erro, pode haver:
     - Código HTTP diferente de 200 (erro de rede ou autenticação)
     - Chave `faultstring` no corpo (erro lógico de negócio)

---

## 🔒 Tratamento de erros

A classe `ERPClientOmie` verifica e trata:

- Erros de configuração (chaves ausentes no ambiente)
- Respostas HTTP inválidas (como 401 ou 500)
- Erros retornados via `faultstring` pela própria API do Omie

Todas as falhas são registradas no logger com nível `ERROR` ou `WARNING`, conforme o tipo.

---

Para a visão geral do módulo ERP e do mock, consulte a página [`index.md`](index.md).