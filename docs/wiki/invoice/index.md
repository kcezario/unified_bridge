# 🧾 Módulo de Nota Fiscal (`invoice`)

Este módulo é responsável pela emissão de Notas Fiscais de Serviço (NFSE), utilizando a API da **NFE.io**.

## 🔗 Provedor atual: [NFE.io](https://nfe.io/docs/api/)

---

## ✅ Funcionalidades Suportadas

- **Emissão de NFSE** (`POST /v1/companies/{companyId}/serviceinvoices`)
- **Consulta de NFSE** (`GET /v1/companies/{companyId}/serviceinvoices/{invoiceId}`)
- **Cancelamento de NFSE** (`POST /v1/companies/{companyId}/serviceinvoices/{invoiceId}/cancel`)
- **Download da NFSE** (`GET /v1/companies/{companyId}/serviceinvoices/{invoiceId}/pdf`)

---

## 🧩 Estrutura do Módulo

```
invoice/
├── interfaces/                   # Contrato da integração
│   └── invoice_interface.py
├── invoice_client_nfe_io.py     # Integração com a API da NFE.io
├── invoice_service.py           # Lógica de emissão e cancelamento
├── mock/                        # Dados simulados para testes
│   ├── mock_borrower.py         # Mocks de tomadores de serviço
│   ├── mock_service.py          # Mocks de serviços prestados
│   └── mock_invoice_client.py   # Mock do client principal
└── tests/manual/
    └── test_invoice_nfe_io.py   # Testes combinatórios e manuais
```

---

## 🧪 Testes Manuais

O script `test_invoice_nfe_io.py` executa testes combinatórios com:

- Três perfis de tomadores (mínimo, recomendado, completo)
- Três tipos de serviços (mínimo, recomendado, completo)

---

## 🔌 Interface Implementada

Arquivo: `invoice/interfaces/invoice_interface.py`

### Métodos esperados:

- `emitir_nfse(data: dict) -> dict`
- `consultar_nfse(nfse_id: str) -> dict`
- `cancelar_nfse(nfse_id: str, reason: str) -> None`
- `download_nfse(nfse_id: str) -> bytes`

---

## 🧪 Mock para Testes

O mock `mock_invoice_client.py` simula todas as chamadas de emissão, consulta, cancelamento e download de notas com base nos dados fornecidos por:

- `mock_borrower.py` (dados dos tomadores)
- `mock_service.py` (dados dos serviços)

---

## 📌 Observações

- O client usa a variável `NFEIO_API_KEY` do `.env`.
- O campo `externalId` é obrigatório e usado como referência de rastreabilidade.
- Os erros 400 e 204 da API real são tratados com logs detalhados.

---

## 📚 Referência Oficial

- [Documentação da API NFE.io](https://nfe.io/docs/api/)