import os
from dotenv import load_dotenv

from core.client_factory import ClientFactory

load_dotenv()  # Carrega o .env para os testes locais

def test_create_erp():
    erp_client = ClientFactory.get_erp_client()
    
    # Gera token se for necessário
    token = erp_client.get_access_token()
    print(f"Token: {token}")

    # Dados mínimos para teste (mock ou reais com a Omie)
    data = {
        "codigo_lancamento_integracao": "test-erp-001",
        "codigo_cliente_fornecedor": 123456,
        "data_vencimento": "2025-04-10",
        "valor_documento": 150.0,
        "codigo_categoria": "1.01.02",
        "id_conta_corrente": 7890,
        "observacao": "Teste de criação de contas a receber",
        "data_previsao": "2025-04-10"
    }

    # Cria
    result = erp_client.create_accounts_receivable(data)
    print("Resultado da criação:", result)

    # Pega o ID do lançamento criado
    lancamento_id = (
        result.get("codigo_lancamento_omie") or
        result.get("codigo_lancamento_integracao") or
        "mock-ar-1"
    )

    # Atualiza
    updated = erp_client.update_accounts_receivable(
        id=str(lancamento_id),
        data={"observacao": "Observação atualizada via teste"}
    )
    print("Resultado da atualização:", updated)

    # Dá baixa
    settled = erp_client.settle_accounts_receivable(str(lancamento_id))
    print("Resultado da baixa:", settled)


if __name__ == "__main__":
    test_create_erp()
