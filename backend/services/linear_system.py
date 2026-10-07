# Resolução de sistemas lineares por escalonamento (eliminação de Gauss).
#
# O sistema chega em duas listas, como na forma matricial A·x = b:
#
#      x + 2y = 5        coeficientes         = [[1, 2], [3, -5]]
#     3x - 5y = 4        termos_independentes = [5, 4]
#
# A resolução tem 4 etapas, uma função para cada:
#
#     1. montar_matriz_aumentada   junta as duas listas    [[1, 2, 5], [3, -5, 4]]
#     2. escalonar                 escalona a matriz       [[1, 2, 5], [0, -11, -11]]
#     3. classificar_sistema       diz o tipo do sistema   "SPD"
#     4. retrossubstituir          calcula a solução       [3, 1]
#
# Cada linha da matriz é uma equação: primeiro os coeficientes e, na última
# posição, o termo independente.
#
# Durante as contas os números são frações (Fraction), para o resultado sair
# exato. No fim tudo vira texto, pronto para mostrar na tela: "3", "-11", "1/3".
#
# As funções confiam que o sistema chegou bem montado. Quem chama precisa
# garantir que:
#     - existe pelo menos uma equação e uma incógnita;
#     - todas as equações têm a mesma quantidade de coeficientes;
#     - existe um termo independente para cada equação;
#     - todos os valores são números (inteiros ou decimais).

from fractions import Fraction


def resolver_sistema_linear(coeficientes, termos_independentes):
    aumentada = montar_matriz_aumentada(coeficientes, termos_independentes)
    escalonada = escalonar(aumentada)
    classificacao = classificar_sistema(escalonada)

    # Só existe solução única para calcular quando o sistema é SPD.
    solucao = None
    if classificacao == "SPD":
        solucao = fracoes_para_texto(retrossubstituir(escalonada))

    return {
        "original": matriz_para_texto(aumentada),
        "escalonada": matriz_para_texto(escalonada),
        "classificacao": classificacao,
        "solucao": solucao,
    }


# Etapa 1: monta a matriz aumentada, colocando cada termo independente no
# fim da sua equação. Os números já entram transformados em fração.
def montar_matriz_aumentada(coeficientes, termos_independentes):
    matriz = []

    for i in range(len(coeficientes)):
        equacao = [converter_para_fracao(valor) for valor in coeficientes[i]]
        equacao.append(converter_para_fracao(termos_independentes[i]))
        matriz.append(equacao)

    return matriz


# Transforma o número em fração para as contas saírem exatas.
#
# O float (número com casas decimais do Python) guarda valores como 0.1 com
# um pequeno erro de arredondamento. Depois de algumas contas pode sobrar
# 0.0000000000000002 onde devia dar zero, e um sistema SPI acaba classificado
# como SI. Com fração a conta é exata e o zero sai zero.
#
# O número passa por texto porque Fraction(0.1) copiaria o erro do float,
# enquanto Fraction("0.1") dá exatamente 1/10.
def converter_para_fracao(valor):
    texto = str(valor)
    return Fraction(texto)


# Etapa 2: escalonamento. Em cada coluna, escolhe um pivô e zera todos os
# valores que ficam abaixo dele. A coluna dos termos independentes também
# entra, para as linhas nulas ficarem sempre por último.
# Precisa receber a matriz com frações, como a etapa 1 devolve.
def escalonar(aumentada):
    # Copia a matriz para não alterar a que foi recebida.
    matriz = [[valor for valor in equacao] for equacao in aumentada]
    num_colunas = len(matriz[0])

    linha_pivo = 0
    for coluna in range(num_colunas):
        linha_encontrada = buscar_linha_com_pivo(matriz, linha_pivo, coluna)

        # Se nenhuma linha serve, a coluna fica sem pivô e a mesma linha
        # tenta de novo na próxima coluna.
        if linha_encontrada is not None:
            # O pivô não pode ser zero: quando é, a linha troca de lugar com
            # a que foi encontrada. Quando não é, linha_encontrada é a própria
            # linha_pivo e a troca não muda nada.
            trocar_linhas(matriz, linha_pivo, linha_encontrada)
            zerar_abaixo_do_pivo(matriz, linha_pivo, coluna)
            linha_pivo += 1

    return matriz


# Procura, da linha_inicial para baixo, a primeira linha que tem um valor
# diferente de zero na coluna: é esse valor que vai ser o pivô.
# Devolve o número da linha, ou None quando não existe nenhuma.
def buscar_linha_com_pivo(matriz, linha_inicial, coluna):
    for linha in range(linha_inicial, len(matriz)):
        if matriz[linha][coluna] != 0:
            return linha

    return None


def trocar_linhas(matriz, primeira, segunda):
    auxiliar = matriz[primeira]
    matriz[primeira] = matriz[segunda]
    matriz[segunda] = auxiliar


# Zera os valores abaixo do pivô. Cada linha de baixo vira:
#     linha - fator * linha do pivô
# O fator é escolhido para o valor que está embaixo do pivô dar zero.
def zerar_abaixo_do_pivo(matriz, linha_pivo, coluna_pivo):
    pivo = matriz[linha_pivo][coluna_pivo]

    for linha in range(linha_pivo + 1, len(matriz)):
        fator = matriz[linha][coluna_pivo] / pivo

        for coluna in range(len(matriz[linha])):
            matriz[linha][coluna] -= fator * matriz[linha_pivo][coluna]


# Etapa 3: classifica o sistema olhando as equações da matriz escalonada.
#     "SI"  = Sistema Impossível: não tem solução
#     "SPI" = Sistema Possível e Indeterminado: tem infinitas soluções
#     "SPD" = Sistema Possível e Determinado: tem uma única solução
# Precisa receber a matriz já escalonada.
def classificar_sistema(escalonada):
    num_incognitas = len(escalonada[0]) - 1
    num_pivos = 0

    for equacao in escalonada:
        termo_independente = equacao[num_incognitas]

        if tem_incognita(equacao):
            # Na matriz escalonada, cada equação que ainda tem incógnita
            # tem o seu pivô.
            num_pivos += 1
        elif termo_independente != 0:
            # Linha 0 0 ... 0 | c com c diferente de zero: é a equação
            # 0 = c, que nunca é verdadeira.
            return "SI"

    # Menos pivôs que incógnitas: sobram incógnitas livres.
    if num_pivos < num_incognitas:
        return "SPI"

    return "SPD"


# Diz se sobrou alguma incógnita na equação, isto é, se algum coeficiente é
# diferente de zero. O último valor fica de fora: é o termo independente.
def tem_incognita(equacao):
    num_incognitas = len(equacao) - 1

    for coluna in range(num_incognitas):
        if equacao[coluna] != 0:
            return True

    return False


# Etapa 4: retrossubstituição. A linha do último pivô tem uma incógnita só;
# depois de calculá-la, cada linha de cima usa os valores já descobertos.
# Só serve para sistema SPD, em que o pivô da linha i fica na coluna i.
def retrossubstituir(escalonada):
    num_incognitas = len(escalonada[0]) - 1
    solucao = [0 for i in range(num_incognitas)]

    # Começa na última incógnita e vai subindo até a primeira.
    linha = num_incognitas - 1
    while linha >= 0:
        # Soma os termos das incógnitas que já foram calculadas.
        soma_conhecida = 0
        for coluna in range(linha + 1, num_incognitas):
            soma_conhecida += escalonada[linha][coluna] * solucao[coluna]

        termo_independente = escalonada[linha][num_incognitas]
        pivo = escalonada[linha][linha]
        solucao[linha] = (termo_independente - soma_conhecida) / pivo

        linha -= 1

    return solucao


# Transforma uma lista de frações em textos prontos para mostrar na tela:
# [Fraction(1, 3), Fraction(2, 1)] vira ["1/3", "2"].
def fracoes_para_texto(fracoes):
    return [str(fracao) for fracao in fracoes]


def matriz_para_texto(matriz):
    return [fracoes_para_texto(equacao) for equacao in matriz]
