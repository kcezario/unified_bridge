class MockBorrower:
    mock_infos = [
        {
            "federalTaxNumber": 11111111000191,
            "address": {
                "country": "BRA"
            }
        },
        {
            "type": "LegalEntity",
            "name": "Empresa Recomendável",
            "federalTaxNumber": 22222222000182,
            "taxRegime": "Isento",
            "email": "recomendado@empresa.com",
            "address": {
                "country": "BRA",
                "postalCode": "12345-000",
                "street": "Rua Central",
                "number": "100",
                "district": "Centro",
                "city": {
                    "code": "3550308",
                    "name": "São Paulo"
                },
                "state": "SP"
            }
        },
        {
            "type": "LegalEntity",
            "name": "Empresa Completa",
            "federalTaxNumber": 33333333000173,
            "municipalTaxNumber": "987654",
            "taxRegime": "LucroPresumido",
            "email": "completo@empresa.com",
            "address": {
                "country": "BRA",
                "postalCode": "04567-000",
                "street": "Av. Completa",
                "number": "789",
                "additionalInformation": "Sala 300",
                "district": "Bairro Completo",
                "city": {
                    "code": "3304557",
                    "name": "Rio de Janeiro"
                },
                "state": "RJ"
            }
        },
        {
            "type": "LegalEntity",
            "name": "Empresa Quatro",
            "federalTaxNumber": 44444444000164,
            "municipalTaxNumber": "123456",
            "taxRegime": "SimplesNacional",
            "email": "empresa4@teste.com",
            "address": {
                "country": "BRA",
                "postalCode": "54321-000",
                "street": "Rua Exemplo",
                "number": "456",
                "additionalInformation": "Conjunto B",
                "district": "Bairro Exemplo",
                "city": {
                    "code": "5208707",
                    "name": "Recife"
                },
                "state": "PE"
            }
        }
    ]

    @classmethod
    def get_by_federal_tax_number(cls, federal_tax_number: int) -> dict | None:
        for info in cls.mock_infos:
            if info.get("federalTaxNumber") == federal_tax_number:
                return info
        return None
