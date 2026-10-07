import json

from services.linear_system import resolver_sistema_linear


def test_resolve_sistema_determinado():
    # x + y = 3
    # 2x + 3y = 8
    resultado = resolver_sistema_linear([[1, 1], [2, 3]], [3, 8])

    assert resultado["classificacao"] == "SPD"
    assert resultado["original"] == [["1", "1", "3"], ["2", "3", "8"]]
    # L2 <- L2 - 2*L1, sem trocar as linhas de lugar
    assert resultado["escalonada"] == [["1", "1", "3"], ["0", "1", "2"]]
    assert resultado["solucao"] == ["1", "2"]


def test_resolve_o_exemplo_da_aula():
    # Exemplo do material de aula (lá resolvido com a matriz inversa):
    # x + 2y = 5
    # 3x - 5y = 4
    resultado = resolver_sistema_linear([[1, 2], [3, -5]], [5, 4])

    assert resultado["classificacao"] == "SPD"
    # L2 <- L2 - 3*L1
    assert resultado["escalonada"] == [["1", "2", "5"], ["0", "-11", "-11"]]
    assert resultado["solucao"] == ["3", "1"]


def test_resolve_o_exercicio_de_quatro_incognitas_da_aula():
    # Exercício do material de aula:
    # 10x + 7y + 8z + 7w = 32
    # 7x + 5y + 6z + 5w = 23
    # 8x + 6y + 10z + 9w = 33
    # 7x + 5y + 9z + 10w = 31
    resultado = resolver_sistema_linear(
        [[10, 7, 8, 7], [7, 5, 6, 5], [8, 6, 10, 9], [7, 5, 9, 10]],
        [32, 23, 33, 31],
    )

    assert resultado["classificacao"] == "SPD"
    assert resultado["solucao"] == ["1", "1", "1", "1"]


def test_classifica_sistema_contraditorio_como_impossivel():
    # x + y = 2
    # x + y = 3
    resultado = resolver_sistema_linear([[1, 1], [1, 1]], [2, 3])

    assert resultado["classificacao"] == "SI"
    # A última linha vira 0 0 | 1, ou seja, 0 = 1
    assert resultado["escalonada"] == [["1", "1", "2"], ["0", "0", "1"]]
    assert resultado["solucao"] is None


def test_classifica_sistema_dependente_como_indeterminado():
    # x + y = 2
    # 2x + 2y = 4
    resultado = resolver_sistema_linear([[1, 1], [2, 2]], [2, 4])

    assert resultado["classificacao"] == "SPI"
    # A segunda equação é o dobro da primeira e some: 0 0 | 0
    assert resultado["escalonada"] == [["1", "1", "2"], ["0", "0", "0"]]
    assert resultado["solucao"] is None


def test_troca_linhas_quando_o_pivo_e_zero():
    # 2y = 4
    # 3x + y = 5
    resultado = resolver_sistema_linear([[0, 2], [3, 1]], [4, 5])

    assert resultado["classificacao"] == "SPD"
    assert resultado["escalonada"] == [["3", "1", "5"], ["0", "2", "4"]]
    assert resultado["solucao"] == ["1", "2"]
    # A troca acontece só na matriz escalonada; a original fica como foi recebida.
    assert resultado["original"] == [["0", "2", "4"], ["3", "1", "5"]]


def test_pula_as_linhas_com_zero_ate_achar_uma_que_serve_de_pivo():
    # y + z = 5
    # 2y + z = 7
    # x + y + z = 6
    resultado = resolver_sistema_linear([[0, 1, 1], [0, 2, 1], [1, 1, 1]], [5, 7, 6])

    assert resultado["classificacao"] == "SPD"
    # L1 <-> L3 (a L2 também começa com zero), depois L3 <- L3 - (1/2)*L2
    assert resultado["escalonada"] == [
        ["1", "1", "1", "6"],
        ["0", "2", "1", "7"],
        ["0", "0", "1/2", "3/2"],
    ]
    assert resultado["solucao"] == ["1", "2", "3"]


def test_troca_com_a_primeira_linha_que_serve_quando_ha_mais_de_uma():
    # y = 1
    # 2x + y = 3
    # 4x + y = 5
    resultado = resolver_sistema_linear([[0, 1], [2, 1], [4, 1]], [1, 3, 5])

    assert resultado["classificacao"] == "SPD"
    # A L2 e a L3 servem de pivô; a troca é com a L2, que vem primeiro.
    # Depois: L3 <- L3 - 2*L1 e L3 <- L3 + L2
    assert resultado["escalonada"] == [
        ["2", "1", "3"],
        ["0", "1", "1"],
        ["0", "0", "0"],
    ]
    assert resultado["solucao"] == ["1", "1"]


def test_troca_linhas_quando_o_zero_aparece_durante_o_escalonamento():
    # x + y + z = 6
    # 2x + 2y + 5z = 21
    # 4x + 6y + 8z = 40
    resultado = resolver_sistema_linear([[1, 1, 1], [2, 2, 5], [4, 6, 8]], [6, 21, 40])

    assert resultado["classificacao"] == "SPD"
    # L2 <- L2 - 2*L1 deixa zero no lugar do segundo pivô, então L2 <-> L3
    assert resultado["escalonada"] == [
        ["1", "1", "1", "6"],
        ["0", "2", "4", "16"],
        ["0", "0", "3", "9"],
    ]
    assert resultado["solucao"] == ["1", "2", "3"]


def test_passa_para_a_proxima_coluna_quando_nenhuma_linha_tem_pivo():
    # x + y + z = 3
    # x + y + 2z = 4
    # 2x + 2y + 5z = 10
    resultado = resolver_sistema_linear([[1, 1, 1], [1, 1, 2], [2, 2, 5]], [3, 4, 10])

    # Depois da 1ª coluna, nenhuma linha tem pivô em y: o pivô seguinte fica em z.
    assert resultado["escalonada"] == [
        ["1", "1", "1", "3"],
        ["0", "0", "1", "1"],
        ["0", "0", "0", "1"],
    ]
    assert resultado["classificacao"] == "SI"
    assert resultado["solucao"] is None


def test_mais_incognitas_que_equacoes_e_indeterminado():
    # x + y + z = 6
    # 2x + 2y + z = 9
    resultado = resolver_sistema_linear([[1, 1, 1], [2, 2, 1]], [6, 9])

    assert resultado["classificacao"] == "SPI"
    assert resultado["escalonada"] == [["1", "1", "1", "6"], ["0", "0", "-1", "-3"]]
    assert resultado["solucao"] is None


def test_mais_incognitas_que_equacoes_pode_ser_impossivel():
    # x + y + z = 1
    # 2x + 2y + 2z = 3
    resultado = resolver_sistema_linear([[1, 1, 1], [2, 2, 2]], [1, 3])

    assert resultado["classificacao"] == "SI"
    assert resultado["escalonada"] == [["1", "1", "1", "1"], ["0", "0", "0", "1"]]
    assert resultado["solucao"] is None


def test_mais_equacoes_que_incognitas_e_determinado_quando_a_equacao_extra_concorda():
    # x + y = 3
    # x - y = 1
    # 2x + y = 5
    resultado = resolver_sistema_linear([[1, 1], [1, -1], [2, 1]], [3, 1, 5])

    assert resultado["classificacao"] == "SPD"
    # A terceira equação não traz informação nova e vira 0 0 | 0
    assert resultado["escalonada"] == [
        ["1", "1", "3"],
        ["0", "-2", "-2"],
        ["0", "0", "0"],
    ]
    assert resultado["solucao"] == ["2", "1"]


def test_mais_equacoes_que_incognitas_e_impossivel_quando_a_equacao_extra_discorda():
    # x + y = 3
    # x - y = 1
    # 2x + y = 6
    resultado = resolver_sistema_linear([[1, 1], [1, -1], [2, 1]], [3, 1, 6])

    assert resultado["classificacao"] == "SI"
    assert resultado["escalonada"] == [
        ["1", "1", "3"],
        ["0", "-2", "-2"],
        ["0", "0", "1"],
    ]
    assert resultado["solucao"] is None


def test_sistema_impossivel_fica_com_as_linhas_nulas_por_ultimo():
    # x + y = 1
    # x + y = 1
    # x + y = 2
    resultado = resolver_sistema_linear([[1, 1], [1, 1], [1, 1]], [1, 1, 2])

    assert resultado["classificacao"] == "SI"
    # Sem escalonar a coluna dos termos independentes, a linha 0 0 | 0
    # ficaria acima da linha 0 0 | 1.
    assert resultado["escalonada"] == [
        ["1", "1", "1"],
        ["0", "0", "1"],
        ["0", "0", "0"],
    ]


def test_sistema_impossivel_fica_com_uma_unica_linha_de_contradicao():
    # x + y = 1
    # x + y = 2
    # x + y = 3
    resultado = resolver_sistema_linear([[1, 1], [1, 1], [1, 1]], [1, 2, 3])

    assert resultado["classificacao"] == "SI"
    # As linhas 0 0 | 1 e 0 0 | 2 se resolvem entre si: L3 <- L3 - 2*L2
    assert resultado["escalonada"] == [
        ["1", "1", "1"],
        ["0", "0", "1"],
        ["0", "0", "0"],
    ]


def test_mostra_a_solucao_como_fracao_exata():
    # x + 2y = 1
    # 3x + 3y = 2
    resultado = resolver_sistema_linear([[1, 2], [3, 3]], [1, 2])

    assert resultado["solucao"] == ["1/3", "1/3"]


def test_resolve_sistema_com_coeficientes_decimais():
    # 0.5x + 1.5y = 2
    # x - y = 0
    resultado = resolver_sistema_linear([[0.5, 1.5], [1, -1]], [2, 0])

    assert resultado["classificacao"] == "SPD"
    assert resultado["original"] == [["1/2", "3/2", "2"], ["1", "-1", "0"]]
    # L2 <- L2 - 2*L1
    assert resultado["escalonada"] == [["1/2", "3/2", "2"], ["0", "-4", "-4"]]
    assert resultado["solucao"] == ["1", "1"]


def test_le_os_coeficientes_decimais_como_foram_escritos():
    # 0.1x + 0.2y = 0.3
    # 0.3x + 0.6y = 0.9
    resultado = resolver_sistema_linear([[0.1, 0.2], [0.3, 0.6]], [0.3, 0.9])

    # A segunda equação é o triplo da primeira. Com o erro de arredondamento
    # do float, sobraria um resto minúsculo no lugar do zero e o sistema
    # seria classificado como SI.
    assert resultado["classificacao"] == "SPI"
    assert resultado["escalonada"] == [["1/10", "1/5", "3/10"], ["0", "0", "0"]]


def test_resultado_pode_ser_enviado_como_json():
    # x + 2y = 1
    # 3x + 3y = 2
    resultado = resolver_sistema_linear([[1, 2], [3, 3]], [1, 2])

    # É assim que a resposta sai da API; ir e voltar não pode mudar nada.
    assert json.loads(json.dumps(resultado)) == resultado
