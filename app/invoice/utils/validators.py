from typing import Optional, Any
from app.invoice.constants.nfe_io_constants import (
    VALID_COUNTRIES_ISO_ALPHA3,
    VALID_BORROWER_TYPES,
    VALID_TAX_REGIMES,
    VALID_TAXATION_TYPES,
) 

def normalize_country_code(country: Optional[str]) -> str:
    """
    Normaliza e valida o código de país no padrão ISO 3166-1 alpha-3.

    - Se None ou vazio, retorna "BRA"
    - Se "Brasil" ou "Brazil", retorna "BRA"
    - Se código válido (ex: BRA, USA), retorna em caixa alta
    - Caso contrário, levanta ValueError
    """
    if not country:
        return "BRA"

    country = country.strip().upper()
    aliases = {
        "BRASIL": "BRA",
        "BRAZIL": "BRA"
    }

    normalized = aliases.get(country, country)

    if normalized not in VALID_COUNTRIES_ISO_ALPHA3:
        raise ValueError(
            f"Sigla de país inválida: '{country}'. Esperado formato ISO 3166-1 alpha-3, ex: 'BRA', 'USA'."
        )

    return normalized

def validate_borrower_type(b_type: Optional[str]) -> None:
    """
    Valida se o borrower.type está entre os valores permitidos.
    """
    if b_type and b_type not in VALID_BORROWER_TYPES:
        raise ValueError(
            f"'type' inválido em borrower: '{b_type}'. Valores válidos: {VALID_BORROWER_TYPES}"
        )


def validate_tax_regime(tax_regime: Optional[str]) -> None:
    """
    Valida se o borrower.taxRegime está entre os valores permitidos.
    """
    if tax_regime and tax_regime not in VALID_TAX_REGIMES:
        raise ValueError(
            f"'taxRegime' inválido em borrower: '{tax_regime}'. Valores válidos: {VALID_TAX_REGIMES}"
        )
        
def validate_taxation_type(value: str) -> None:
    if value and value not in VALID_TAXATION_TYPES:
        raise ValueError(
            f"'taxationType' inválido: '{value}'. Valores válidos: {VALID_TAXATION_TYPES}"
        )


def validate_services_amount(value: Any) -> None:
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValueError("O campo 'servicesAmount' deve ser numérico e maior que zero.")


def validate_required_string(field_name: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"O campo obrigatório '{field_name}' está ausente ou inválido.")