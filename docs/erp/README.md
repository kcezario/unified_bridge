
## 🧩 `ERPClientInterface`

Interface que define o contrato para qualquer cliente ERP que deseje implementar integração com o sistema de contas a receber.

Esta interface permite desacoplar a aplicação do provedor específico de ERP, garantindo testabilidade e extensibilidade.

### Métodos obrigatórios

```python
def create_accounts_receivable(self, data: Dict[str, Any]) -> Dict[str, Any]: ...
def update_accounts_receivable(self, id: str, data: Dict[str, Any]) -> Dict[str, Any]: ...
def settle_accounts_receivable(self, id: str, account_id: Optional[str] = None) -> Dict[str, Any]: ...
```

Todos os métodos devem receber/retornar dicionários, de forma a manter compatibilidade com qualquer ERP.

---

## 🧪 `ERPClientMock`

Classe de mock utilizada exclusivamente para testes locais ou ambientes de desenvolvimento offline.

Implementa a interface `ERPClientInterface`, simulando chamadas reais, mas sem efetuar nenhuma operação externa.

### Exemplos de retorno

#### `create_accounts_receivable(...)`

```json
{
  "codigo_lancamento_omie": 123456,
  "codigo_lancamento_integracao": "mock-uuid",
  "codigo_status": "0",
  "descricao_status": "Mock: lançamento criado"
}
```

#### `update_accounts_receivable(...)`

```json
{
  "codigo_lancamento_omie": 123456,
  "codigo_status": "0",
  "descricao_status": "Mock: lançamento atualizado"
}
```

#### `settle_accounts_receivable(...)`

```json
{
  "codigo_lancamento": 123456,
  "codigo_baixa": 999999,
  "valor_baixado": 4321.0,
  "codigo_status": "0",
  "descricao_status": "Mock: baixa registrada"
}
```

## `ERPClientOmie`

Classe responsável pela integração com a [API de Contas a Receber da Omie](https://app.omie.com.br/api/v1/financas/contareceber/).

Esta classe encapsula os métodos necessários para **criar**, **atualizar** e **baixar** lançamentos financeiros na plataforma Omie via REST API.

### 🔧 Requisitos de Ambiente

As seguintes variáveis de ambiente devem estar configuradas:

- `OMIE_APP_KEY`: Chave de acesso fornecida pela Omie.
- `OMIE_APP_SECRET`: Segredo da aplicação.
- `OMIE_BASE_URL`: Normalmente `https://app.omie.com.br/api/v1/`.
- `OMIE_DEFAULT_ACCOUNT_ID`: (opcional) ID da conta corrente padrão para baixas.

---

### 📘 Métodos

#### `create_accounts_receivable(data: Dict[str, Any]) -> Dict[str, Any>`

Cria um novo lançamento no Contas a Receber.

**Parâmetros:**

| Campo                      | Tipo        | Obrigatório | Descrição                                            |
|---------------------------|-------------|-------------|------------------------------------------------------|
| `codigo_lancamento_integracao` | `str`     | ✅           | Identificador único do integrador (UUID recomendado). |
| `codigo_cliente_fornecedor`    | `int/str` | ✅           | Código do cliente/fornecedor no Omie.                |
| `data_vencimento`              | `str`     | ✅           | Data no formato `"dd/mm/aaaa"`.                      |
| `valor_documento`             | `float/str` | ✅         | Valor total do lançamento.                           |
| `codigo_categoria`            | `str`     | ✅           | Categoria financeira cadastrada no Omie.             |
| `data_previsao`               | `str`     | ✅           | Data prevista de recebimento.                        |
| `id_conta_corrente`           | `int/str` | ✅           | ID da conta corrente para crédito.                   |
| `observacao`                  | `str`     | Opcional     | Comentário sobre o lançamento.                       |

**Retorno:**

Dicionário com os dados do lançamento criado, incluindo `codigo_lancamento_omie`.

---

#### `update_accounts_receivable(id: str, data: Dict[str, Any]) -> Dict[str, Any>`

Atualiza campos de um lançamento existente.

**Parâmetros:**

- `id`: Código do lançamento (`codigo_lancamento_omie`).
- `data`: Dicionário com os campos a serem atualizados (ex: `{"observacao": "Texto atualizado"}`).

**Retorno:**

Dicionário com status da operação.

---

#### `settle_accounts_receivable(id: str, account_id: Optional[str] = None) -> Dict[str, Any>`

Realiza a **baixa de um título** financeiro.

**Parâmetros:**

- `id`: Código do lançamento (`codigo_lancamento`).
- `account_id`: ID da conta corrente. Se não fornecido, usa `OMIE_DEFAULT_ACCOUNT_ID`.

> **Importante:** o valor da baixa deve ser igual ou inferior ao valor em aberto.

**Retorno:**

Dicionário com o status da baixa, incluindo `valor_baixado`, `codigo_baixa` e se foi `liquidado`.