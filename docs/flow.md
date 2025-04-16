* * *

## 📄 **Fluxo da Nota Fiscal (NFE.io) — por CNPJ**

* * *

### 1. `issue_invoice(data: dict) -> dict`

**Local:** `InvoiceClientNFEio`**Descrição:** Emite a nota fiscal de serviço via API da NFE.io.

**Parâmetros:**

    data = {
        "borrower": {
            "federalTaxNumber": "12345678000199",         # CNPJ da filial
            "address": {
                "country": "BRA",                         # País (sempre "BRA")
            }
        },
        "description": "Gestão de benefícios",            # Descrição do serviço prestado
        "servicesAmount": 200.00,                         # Valor total da nota
        "cityServiceCode": "101"                          # Código de serviço municipal (prefeitura)
    }

**Retorno:**

    {
        "invoice_id": "inv-123",                          # ID gerado pela NFE.io
        "external_id": "uuid-ex-123",                     # ID interno (se usado)
        "nfe_io_response": {...}                          # Resposta bruta da NFE.io
    }

* * *

### 2. `download_invoice(invoice_id: str) -> dict`

**Local:** `InvoiceClientNFEio`**Descrição:** Baixa o PDF da nota fiscal emitida.

**Parâmetros:**

    invoice_id = "inv-123"                               # ID retornado na emissão

**Retorno:**

    {
        "status": "success",
        "invoice_id": "inv-123",
        "pdf_url": "https://nfe.io/api/pdf/inv-123"       # Link direto do PDF
    }

* * *

### 3. `upload_pdf_to_s3(file_bytes: bytes, s3_key: str) -> str`

**Local:** a ser implementado (ex: `utils/storage.py`)**Descrição:** Envia o PDF da nota para o S3 e retorna a URL final.

**Parâmetros:**

    file_bytes = b"%PDF-1.4 ..."                         # Conteúdo bruto do arquivo PDF
    s3_key = "invoices/cliente-001/inv-123.pdf"          # Caminho no bucket

**Retorno:**

    s3_url = "https://s3.amazonaws.com/bucket/invoices/cliente-001/inv-123.pdf"  # Link final no S3

* * *

### 4. `save_invoice_record(invoice_id: str, external_id: str, client_id: str, branch_cnpj: str, raw_data: dict) -> None`

**Local:** a ser implementado (ex: `repository/invoice.py`)**Descrição:** Persiste o registro da nota fiscal no banco de dados.

**Parâmetros:**

    invoice_id = "inv-123"                               # ID da NFE.io
    external_id = "uuid-ex-123"                          # ID interno (chave de rastreio)
    client_id = "cliente-001"                            # ID do cliente Brasil Life
    branch_cnpj = "12345678000199"                       # CNPJ da filial
    raw_data = {...}                                     # Resposta bruta da NFE.io

**Retorno:** `None`

* * *

### 5. `save_invoice_pdf_url(invoice_id: str, s3_url: str) -> None`

**Local:** a ser implementado**Descrição:** Atualiza o registro da nota com o link do PDF hospedado no S3.

**Parâmetros:**

    invoice_id = "inv-123"
    s3_url = "https://s3.amazonaws.com/bucket/invoices/cliente-001/inv-123.pdf"

**Retorno:** `None`

* * *

## 💰 **Fluxo de Pagamento (Asaas) — por CNPJ**

* * *

### 1. `create_payment(data: dict) -> dict`

**Local:** `PaymentClientAsaas`**Descrição:** Cria uma cobrança (boleto, PIX ou cartão) via API do Asaas.

**Parâmetros:**

    data = {
        "customer": "cus_000006622263",                  # ID do cliente no Asaas (já cadastrado)
        "billingType": "BOLETO",                         # Tipo de cobrança (BOLETO, PIX ou CREDIT_CARD)
        "value": 200.00,                                 # Valor da cobrança
        "dueDate": "2025-04-20",                         # Data de vencimento (formato YYYY-MM-DD)
        "description": "Gestão de benefícios"            # Descrição da cobrança
    }

**Retorno:**

    {
        "payment_id": "pay_abc123",                      # ID da cobrança gerado pelo Asaas
        "asaas_response": {...}                          # Resposta completa da API do Asaas
    }

* * *

### 2. `get_payment_link(payment_data: dict) -> str`

**Local:** `PaymentClientAsaas`**Descrição:** Extrai o link do boleto bancário da resposta da API.

**Parâmetros:**

    payment_data = {
        "bankSlipUrl": "https://asaas.com/boleto/xyz",   # Campo presente na resposta da criação
        ...
    }

**Retorno:**

    "https://asaas.com/boleto/xyz"                      # Link do boleto

* * *

### 3. `download_payment_pdf(payment_id: str) -> bytes`

**Local:** a ser implementado (ex: `utils/asaas.py`)**Descrição:** Faz o download do PDF do boleto usando o `bankSlipUrl`.

**Parâmetros:**

    payment_id = "pay_abc123"                           # ID da cobrança

> ⚠️ Obs.: o PDF deve ser baixado diretamente via link (`bankSlipUrl`) com `requests.get(...).content`

**Retorno:**

    pdf_bytes = b"%PDF-1.4 ..."                         # Conteúdo bruto do boleto em PDF

* * *

### 4. `upload_pdf_to_s3(file_bytes: bytes, s3_key: str) -> str`

**Local:** reutilização da mesma função do fluxo da nota**Descrição:** Envia o PDF do boleto para o S3 e retorna o link.

**Parâmetros:**

    file_bytes = b"%PDF-1.4 ..."                        # Conteúdo do boleto
    s3_key = "payments/cliente-001/pay_abc123.pdf"      # Caminho no bucket

**Retorno:**

    "https://s3.amazonaws.com/bucket/payments/cliente-001/pay_abc123.pdf"

* * *

### 5. `save_payment_record(payment_id: str, client_id: str, branch_cnpj: str, raw_data: dict) -> None`

**Local:** a ser implementado**Descrição:** Salva os dados da cobrança gerada no banco, com vínculo à filial.

**Parâmetros:**

    payment_id = "pay_abc123"
    client_id = "cliente-001"
    branch_cnpj = "12345678000199"
    raw_data = {...}                                    # Resposta completa da API do Asaas

**Retorno:** `None`

* * *

### 6. `save_payment_pdf_url(payment_id: str, s3_url: str) -> None`

**Local:** a ser implementado**Descrição:** Atualiza o registro da cobrança com o link do boleto PDF hospedado no S3.

**Parâmetros:**

    payment_id = "pay_abc123"
    s3_url = "https://s3.amazonaws.com/bucket/payments/cliente-001/pay_abc123.pdf"

**Retorno:** `None`