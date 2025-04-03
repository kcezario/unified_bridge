from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date


class AccountsReceivableOmieModel(BaseModel):
    codigo_lancamento_integracao: Optional[str] = Field(
        None, description="Código único de controle do integrador"
    )
    codigo_cliente_fornecedor: int = Field(..., description="Código do cliente na Omie")
    data_vencimento: date = Field(..., description="Data de vencimento do título")
    valor_documento: float = Field(..., gt=0, description="Valor do documento (positivo)")
    codigo_categoria: str = Field(..., description="Código da categoria financeira")
    id_conta_corrente: int = Field(..., description="ID da conta corrente bancária")
    observacao: Optional[str] = Field(None, description="Observações gerais")
    data_previsao: Optional[date] = Field(None, description="Data prevista de pagamento")

    @validator("codigo_categoria")
    def categoria_nao_vazia(cls, v):
        if not v.strip():
            raise ValueError("Código da categoria não pode ser vazio.")
        return v

    class Config:
        anystr_strip_whitespace = True
        schema_extra = {
            "example": {
                "codigo_lancamento_integracao": "int-001",
                "codigo_cliente_fornecedor": 4214850,
                "data_vencimento": "2025-04-05",
                "valor_documento": 100.00,
                "codigo_categoria": "1.01.02",
                "id_conta_corrente": 123456,
                "observacao": "Cobrança referente ao serviço XPTO",
                "data_previsao": "2025-04-05"
            }
        }
