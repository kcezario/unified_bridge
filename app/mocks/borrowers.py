class MockBorrower:
    mock_infos = [
        {
            "type": "PessoaJuridica",
            "name": "Empresa A",
            "federalTaxNumber": 12345678000100,
            "municipalTaxNumber": "123456",
            "taxRegime": "Isento",
            "email": "contato@empresaA.com",
            "address": {
                "country": "Brasil",
                "postalCode": "04567-000",
                "street": "Rua Fictícia A",
                "number": "123",
                "additionalInformation": "Sala 1",
                "district": "Bairro Exemplo A",
                "city": {"code": "3550308", "name": "São Paulo"},
                "state": "SP",
            },
        },
        {
            "type": "PessoaJuridica",
            "name": "Empresa B",
            "federalTaxNumber": 98765432000100,
            "municipalTaxNumber": "654321",
            "taxRegime": "Normal",
            "email": "contato@empresaB.com",
            "address": {
                "country": "Brasil",
                "postalCode": "12345-678",
                "street": "Rua Fictícia B",
                "number": "456",
                "additionalInformation": "Sala 2",
                "district": "Bairro Exemplo B",
                "city": {"code": "3304557", "name": "Rio de Janeiro"},
                "state": "RJ",
            },
        },
        {
            "type": "PessoaJuridica",
            "name": "Empresa C",
            "federalTaxNumber": 11223344000155,
            "municipalTaxNumber": "789012",
            "taxRegime": "Isento",
            "email": "contato@empresaC.com",
            "address": {
                "country": "Brasil",
                "postalCode": "98765-432",
                "street": "Rua Fictícia C",
                "number": "789",
                "additionalInformation": "Sala 3",
                "district": "Bairro Exemplo C",
                "city": {"code": "4106902", "name": "Curitiba"},
                "state": "PR",
            },
        },
        {
            "type": "PessoaJuridica",
            "name": "Empresa D",
            "federalTaxNumber": 55667788000199,
            "municipalTaxNumber": "345678",
            "taxRegime": "Normal",
            "email": "contato@empresaD.com",
            "address": {
                "country": "Brasil",
                "postalCode": "54321-098",
                "street": "Rua Fictícia D",
                "number": "101",
                "additionalInformation": "Sala 4",
                "district": "Bairro Exemplo D",
                "city": {"code": "5208707", "name": "Recife"},
                "state": "PE",
            },
        },
    ]

    @classmethod
    def get_by_federal_tax_number(cls, federal_tax_number: int = 12345678000100):
        for info in cls.mock_infos:
            if info["federalTaxNumber"] == federal_tax_number:
                return info
        return None
