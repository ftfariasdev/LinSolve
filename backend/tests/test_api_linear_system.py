from fastapi.testclient import TestClient

from main import app

client = TestClient(app, raise_server_exceptions=False)

URL = "/api/linear-system/solve/"


def test_resolve_sistema_determinado():
    # x + 2y = 5
    # 3x - 5y = 4
    resposta = client.post(
        URL, json={"coeficientes": [[1, 2], [3, -5]], "termos_independentes": [5, 4]}
    )

    assert resposta.status_code == 200
    assert resposta.json() == {
        "original": [["1", "2", "5"], ["3", "-5", "4"]],
        "escalonada": [["1", "2", "5"], ["0", "-11", "-11"]],
        "classificacao": "SPD",
        "solucao": ["3", "1"],
    }


def test_resolve_sistema_indeterminado():
    # x + y = 2
    # 2x + 2y = 4
    resposta = client.post(
        URL, json={"coeficientes": [[1, 1], [2, 2]], "termos_independentes": [2, 4]}
    )

    assert resposta.status_code == 200
    assert resposta.json()["classificacao"] == "SPI"
    assert resposta.json()["solucao"] is None


def test_resolve_sistema_impossivel():
    # x + y = 2
    # x + y = 3
    resposta = client.post(
        URL, json={"coeficientes": [[1, 1], [1, 1]], "termos_independentes": [2, 3]}
    )

    assert resposta.status_code == 200
    assert resposta.json()["classificacao"] == "SI"
    assert resposta.json()["solucao"] is None


def test_aceita_coeficientes_decimais():
    # 0.1x + 0.2y = 0.3
    # 0.3x + 0.6y = 0.9
    resposta = client.post(
        URL,
        json={"coeficientes": [[0.1, 0.2], [0.3, 0.6]], "termos_independentes": [0.3, 0.9]},
    )

    assert resposta.status_code == 200
    assert resposta.json()["original"][0] == ["1/10", "1/5", "3/10"]
    assert resposta.json()["classificacao"] == "SPI"


def test_recusa_sistema_sem_equacoes():
    resposta = client.post(URL, json={"coeficientes": [], "termos_independentes": []})

    assert resposta.status_code == 400
    assert resposta.json() == {"detail": "O sistema precisa ter pelo menos uma equação."}


def test_recusa_equacao_sem_incognitas():
    resposta = client.post(URL, json={"coeficientes": [[]], "termos_independentes": [1]})

    assert resposta.status_code == 400
    assert resposta.json() == {"detail": "O sistema precisa ter pelo menos uma incógnita."}


def test_recusa_equacoes_com_tamanhos_diferentes():
    resposta = client.post(
        URL, json={"coeficientes": [[1, 2], [3]], "termos_independentes": [5, 4]}
    )

    assert resposta.status_code == 400
    assert resposta.json() == {
        "detail": "Todas as equações precisam ter a mesma quantidade de coeficientes."
    }


def test_recusa_termos_independentes_em_quantidade_diferente_das_equacoes():
    resposta = client.post(
        URL, json={"coeficientes": [[1, 2], [3, -5]], "termos_independentes": [5]}
    )

    assert resposta.status_code == 400
    assert resposta.json() == {
        "detail": "A quantidade de termos independentes precisa ser igual à de equações."
    }


def test_recusa_valor_que_nao_e_numero():
    resposta = client.post(
        URL, json={"coeficientes": [[1, "x"]], "termos_independentes": [5]}
    )

    assert resposta.status_code == 400
    assert "detail" in resposta.json()


def test_recusa_requisicao_sem_os_campos():
    resposta = client.post(URL, json={})

    assert resposta.status_code == 400


def test_erro_inesperado_responde_500_sem_detalhes(monkeypatch):
    def falhar(coeficientes, termos_independentes):
        raise RuntimeError("detalhe interno")

    monkeypatch.setattr("api.routes.linear_system.resolver_sistema_linear", falhar)

    resposta = client.post(
        URL, json={"coeficientes": [[1]], "termos_independentes": [1]}
    )

    assert resposta.status_code == 500
    assert resposta.json() == {"detail": "Erro interno. Tente novamente mais tarde."}
    assert "detalhe interno" not in resposta.text
