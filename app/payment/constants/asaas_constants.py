class BillingType:
    UNDEFINED = "UNDEFINED"
    BOLETO = "BOLETO"
    PIX = "PIX"
    CREDIT_CARD = "CREDIT_CARD"

    ALL = {UNDEFINED, BOLETO, PIX, CREDIT_CARD}


# Tipos de desconto
class DiscountType:
    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED"


# Exemplo de status possíveis (caso queira tratar depois)
class PaymentStatus:
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    CONFIRMED = "CONFIRMED"
    OVERDUE = "OVERDUE"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"

WEBHOOK_PAYMENT_FIELDS = {
    "event",
    "payment.id",
    "payment.status",
    "payment.paymentDate",
    "payment.value",
    "payment.netValue",
    "payment.billingType",
    "payment.customer",
    "payment.invoiceUrl",
    "payment.bankSlipUrl",
    "payment.transactionReceiptUrl",
}