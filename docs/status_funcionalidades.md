# ✅ Status das Funcionalidades — Unified Bridge

Este documento consolida as funcionalidades requisitadas por stakeholders e o status atual da sua implementação **a nível de interface**. O objetivo é garantir que todas as integrações externas possuam suporte padronizado e completo via `ClientInterface`.

---

## 💰 PaymentClientInterface (Asaas)

| Funcionalidade                                     | Método esperado na interface             | Status         |
|---------------------------------------------------|------------------------------------------|----------------|
| ✅ Gerar cobrança (PIX, boleto, cartão)           | `create_payment(data: dict)`             | ✅ Implementado |
| ⚠️ Expor link ou PDF do boleto                    | 🔸 Dentro da resposta de `create_payment` | ⚠️ Parcial (*implícito via response*) |
| ⚠️ Webhook: validação de pagamento automático     | `handle_payment_webhook(payload: dict)`  | ❌ Não implementado |
| ✅ Cancelar cobrança                              | `cancel_payment(payment_id: str)`        | ✅ Implementado |
| ✅ Consultar status do pagamento                  | `get_payment_status(payment_id: str)`    | ✅ Implementado |

🟡 **Ações pendentes**:
- Adicionar o método `handle_payment_webhook()` na `PaymentClientInterface`.
- Criar lógica para expor ou extrair o link do boleto via método dedicado (opcional).

---

## 🧾 InvoiceClientInterface (NFE.io)

| Funcionalidade                                   | Método esperado na interface             | Status         |
|--------------------------------------------------|------------------------------------------|----------------|
| ✅ Emissão de nota fiscal de serviço (NFSE)      | `issue_invoice(data: dict)`              | ✅ Implementado |
| ✅ Cancelamento de nota fiscal                   | `cancel_invoice(invoice_id: str)`        | ✅ Implementado |
| ✅ Consulta de status da nota fiscal             | `get_invoice_status(invoice_id: str)`    | ✅ Implementado |
| ✅ Download da nota em PDF                       | `download_invoice(invoice_id: str)`      | ✅ implementado |

🟡 **Ações pendentes**:
- Adicionar `download_invoice()` na `InvoiceClientInterface`.
- Implementar chamada à API NFE.io para obtenção de PDF da nota fiscal (se suportado).

---

## 📊 ERPClientInterface (Omie)

| Funcionalidade                                 | Método esperado na interface                      | Status         |
|------------------------------------------------|-------------------------------------------------- |----------------|
| ✅ Criação de conta a receber                  | `create_accounts_receivable(data: dict)`          | ✅ Implementado |
| ✅ Baixa (liquidação) da conta                 | `settle_accounts_receivable(...)`                 | ✅ Implementado |
| ✅ Atualização de conta                        | `update_accounts_receivable(id: str, data: dict)` | ✅ Implementado |
| ✅ Cancelamento da conta a receber             | `cancel_accounts_receivable(id: str)`             | ✅ Implementado |
---

## 📌 Resumo Geral

| Provedor | Funcionalidade pendente a nível de interface |
|----------|-----------------------------------------------|
| **Asaas** | `handle_payment_webhook(payload: dict)` (*novo método*) |
| **NFE.io** | `download_invoice(invoice_id: str)` |
| **Omie** | `cancel_accounts_receivable(id: str)` |

---

✅ Interfaces padronizadas garantem flexibilidade e intercambialidade.  
⚠️ Funcionalidades pendentes devem ser priorizadas para completar a cobertura solicitada.

