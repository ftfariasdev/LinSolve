from fractions import Fraction

from services.linear_system import resolver_sistema_linear


def test_resolve_sistema_determinado():
    # x + y = 3
    # 2x + 3y = 8
    resultado = resolver_sistema_linear([[1, 1], [2, 3]], [3, 8])

    assert resultado["classification"] == "SPD"
    assert resultado["original"] == [[1, 1, 3], [2, 3, 8]]
    # L2 <- L2 - 2*L1, sem trocar as linhas de lugar
    assert resultado["echelon"] == [[1, 1, 3], [0, 1, 2]]
    assert resultado["solution"] == [1, 2]


def test_resolve_o_exemplo_da_aula():
    # Exemplo do material de aula (lá resolvido com a matriz inversa):
    # x + 2y = 5
    # 3x - 5y = 4
    resultado = resolver_sistema_linear([[1, 2], [3, -5]], [5, 4])

    assert resultado["classification"] == "SPD"
    # L2 <- L2 - 3*L1
    assert resultado["echelon"] == [[1, 2, 5], [0, -11, -11]]
    assert resultado["solution"] == [3, 1]


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

    assert resultado["classification"] == "SPD"
    assert resultado["solution"] == [1, 1, 1, 1]


def test_classifica_sistema_contraditorio_como_impossivel():
    # x + y = 2
    # x + y = 3
    resultado = resolver_sistema_linear([[1, 1], [1, 1]], [2, 3])

    assert resultado["classification"] == "SI"
    # A última linha vira 0 0 | 1, ou seja, 0 = 1
    assert resultado["echelon"] == [[1, 1, 2], [0, 0, 1]]
    assert resultado["solution"] is None


def test_classifica_sistema_dependente_como_indeterminado():
    # x + y = 2
    # 2x + 2y = 4
    resultado = resolver_sistema_linear([[1, 1], [2, 2]], [2, 4])

    assert resultado["classification"] == "SPI"
    # A segunda equação é o dobro da primeira e some: 0 0 | 0
    assert resultado["echelon"] == [[1, 1, 2], [0, 0, 0]]
    assert resultado["solution"] is None


def test_troca_linhas_quando_o_pivo_e_zero():
    # 2y = 4
    # 3x + y = 5
    resultado = resolver_sistema_linear([[0, 2], [3, 1]], [4, 5])

    assert resultado["classification"] == "SPD"
    assert resultado["echelon"] == [[3, 1, 5], [0, 2, 4]]
    assert resultado["solution"] == [1, 2]
    # A troca acontece só na matriz escalonada; a original fica como foi recebida.
    assert resultado["original"] == [[0, 2, 4], [3, 1, 5]]


def test_troca_com_a_primeira_linha_de_baixo_que_tem_valor_nao_nulo():
    # y + z = 5
    # 2y + z = 7
    # x + y + z = 6
    resultado = resolver_sistema_linear([[0, 1, 1], [0, 2, 1], [1, 1, 1]], [5, 7, 6])

    assert resultado["classification"] == "SPD"
    # L1 <-> L3 (a L2 também começa com zero), depois L3 <- L3 - (1/2)*L2
    assert resultado["echelon"] == [
        [1, 1, 1, 6],
        [0, 2, 1, 7],
        [0, 0, Fraction(1, 2), Fraction(3, 2)],
    ]
    assert resultado["solution"] == [1, 2, 3]


def test_passa_para_a_proxima_coluna_quando_nenhuma_linha_tem_pivo():
    # x + y + z = 3
    # x + y + 2z = 4
    # 2x + 2y + 5z = 10
    resultado = resolver_sistema_linear([[1, 1, 1], [1, 1, 2], [2, 2, 5]], [3, 4, 10])

    # Depois da 1ª coluna, nenhuma linha tem pivô em y: o pivô seguinte fica em z.
    assert resultado["echelon"] == [[1, 1, 1, 3], [0, 0, 1, 1], [0, 0, 0, 1]]
    assert resultado["classification"] == "SI"
    assert resultado["solution"] is None


def test_mais_incognitas_que_equacoes_e_indeterminado():
    # x + y + z = 6
    # 2x + 2y + z = 9
    resultado = resolver_sistema_linear([[1, 1, 1], [2, 2, 1]], [6, 9])

    assert resultado["classification"] == "SPI"
    assert resultado["echelon"] == [[1, 1, 1, 6], [0, 0, -1, -3]]
    assert resultado["solution"] is None


def test_mais_incognitas_que_equacoes_pode_ser_impossivel():
    # x + y + z = 1
    # 2x + 2y + 2z = 3
    resultado = resolver_sistema_linear([[1, 1, 1], [2, 2, 2]], [1, 3])

    assert resultado["classification"] == "SI"
    assert resultado["echelon"] == [[1, 1, 1, 1], [0, 0, 0, 1]]
    assert resultado["solution"] is None


def test_mais_equacoes_que_incognitas_e_determinado_quando_a_equacao_extra_concorda():
    # x + y = 3
    # x - y = 1
    # 2x + y = 5
    resultado = resolver_sistema_linear([[1, 1], [1, -1], [2, 1]], [3, 1, 5])

    assert resultado["classification"] == "SPD"
    # A terceira equação não traz informação nova e vira 0 0 | 0
    assert resultado["echelon"] == [[1, 1, 3], [0, -2, -2], [0, 0, 0]]
    assert resultado["solution"] == [2, 1]


def test_mais_equacoes_que_incognitas_e_impossivel_quando_a_equacao_extra_discorda():
    # x + y = 3
    # x - y = 1
    # 2x + y = 6
    resultado = resolver_sistema_linear([[1, 1], [1, -1], [2, 1]], [3, 1, 6])

    assert resultado["classification"] == "SI"
    assert resultado["echelon"] == [[1, 1, 3], [0, -2, -2], [0, 0, 1]]
    assert resultado["solution"] is None


def test_mantem_as_fracoes_exatas_na_solucao():
    # x + 2y = 1
    # 3x + 3y = 2
    resultado = resolver_sistema_linear([[1, 2], [3, 3]], [1, 2])

    assert resultado["solution"] == [Fraction(1, 3), Fraction(1, 3)]


def test_le_os_coeficientes_decimais_como_foram_escritos():
    # 0.1x + 0.2y = 0.3
    # 0.3x + 0.6y = 0.9
    resultado = resolver_sistema_linear([[0.1, 0.2], [0.3, 0.6]], [0.3, 0.9])

    # A segunda equação é o triplo da primeira. Com o erro de arredondamento
    # do float, sobraria um resto minúsculo no lugar do zero.
    assert resultado["classification"] == "SPI"
    assert resultado["echelon"] == [
        [Fraction(1, 10), Fraction(1, 5), Fraction(3, 10)],
        [0, 0, 0],
    ]
