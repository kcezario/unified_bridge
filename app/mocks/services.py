from datetime import datetime, timedelta


class MockServices:
    mock_infos = [
        # Mínimo necessário para emissão da NFSE
        {
            "cityServiceCode": "101",
            "description": "Serviço mínimo exigido",
            "servicesAmount": 100.0,
        },
        # Campos recomendados
        {
            "cityServiceCode": "202",
            "description": "Serviço com campos recomendados",
            "servicesAmount": 250.0,
            "taxationType": "None",
            "issRate": 0.05,
            "issuedOn": datetime.utcnow().isoformat() + "Z"
        },

        {
            "cityServiceCode": "303",
            "description": "Serviço completo com todos os campos disponíveis",
            "servicesAmount": 1500.0,
            "federalServiceCode": "1234",
            "cnaeCode": "6201501",
            "rpsSerialNumber": "ABC",
            "issuedOn": datetime.utcnow().isoformat() + "Z",
            "rpsNumber": 1001,
            "taxationType": "WithinCity",
            "issRate": 0.02,
            "issTaxAmount": 75.0,
            "deductionsAmount": 50.0,
            "discountUnconditionedAmount": 10.0,
            "discountConditionedAmount": 5.0,
            "irAmountWithheld": 3.0,
            "pisAmountWithheld": 2.0,
            "cofinsAmountWithheld": 1.5,
            "csllAmountWithheld": 1.0,
            "inssAmountWithheld": 4.0,
            "issAmountWithheld": 0.0,
            "othersAmountWithheld": 0.5,
            "approximateTax": {
                "source": "IBPT",
                "version": "2025.1",
                "totalRate": 15.0
            },
            "additionalInformation": "Informações adicionais sobre o serviço prestado.",
            "location": {
                "state": "SP",
                "country": "BRA",
                "postalCode": "04567-000",
                "street": "Av. Paulista",
                "number": "1000",
                "district": "Bela Vista",
                "AdditionalInformation": "10º andar",
                "city": {
                    "code": "3550308",
                    "name": "São Paulo"
                }
            },
            "activityEvent": {
                "name": "Workshop de tecnologia",
                "startOn": (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z",
                "endOn": datetime.utcnow().isoformat() + "Z",
                "atvEvId": "event-001"
            }
        }
    ]

    @classmethod
    def get(cls, index: int = 0):
        if 0 <= index < len(cls.mock_infos):
            return cls.mock_infos[index]
        return None
