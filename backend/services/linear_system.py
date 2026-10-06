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

from fractions import Fraction


def resolver_sistema_linear(coeficientes, termos_independentes):
    original = montar_matriz_aumentada(coeficientes, termos_independentes)
    escalonada = escalonar(original)
    classificacao = classificar_sistema(escalonada)

    # Só existe solução única para calcular quando o sistema é SPD.
    solucao = None
    if classificacao == "SPD":
        solucao = retrossubstituir(escalonada)

    # As chaves ficam em inglês porque são o formato da resposta da API
    # combinado com o frontend.
    return {
        "original": original,
        "echelon": escalonada,
        "classification": classificacao,
        "solution": solucao,
    }


# Etapa 1: monta a matriz aumentada, colocando cada termo independente
# no fim da linha da sua equação.
def montar_matriz_aumentada(coeficientes, termos_independentes):
    matriz = []

    for i in range(len(coeficientes)):
        linha = [converter_para_fracao(valor) for valor in coeficientes[i]]
        linha.append(converter_para_fracao(termos_independentes[i]))
        matriz.append(linha)

    return matriz


# Transforma o número em fração, para as contas darem o resultado exato
# (1/3, e não 0.3333...).
# O número vira texto antes porque o float guarda 0.1 com um pequeno erro
# de arredondamento: Fraction(0.1) carregaria esse erro, Fraction("0.1") é 1/10.
def converter_para_fracao(valor):
    return Fraction(str(valor))


# Etapa 2: escalonamento. Em cada coluna, escolhe um pivô e zera todos
# os valores que ficam abaixo dele.
def escalonar(aumentada):
    # Copia a matriz para não alterar a original.
    matriz = [[valor for valor in linha] for linha in aumentada]
    num_incognitas = len(matriz[0]) - 1

    linha_pivo = 0
    for coluna in range(num_incognitas):
        linha_nao_nula = buscar_linha_nao_nula(matriz, linha_pivo, coluna)

        # Se nenhuma linha serve, a coluna fica sem pivô e a mesma linha
        # tenta de novo na próxima coluna.
        if linha_nao_nula is not None:
            # O pivô não pode ser zero: quando é, a linha troca de lugar com
            # a que foi encontrada. Quando não é, linha_nao_nula é a própria
            # linha_pivo e a troca não muda nada.
            trocar_linhas(matriz, linha_pivo, linha_nao_nula)
            zerar_abaixo_do_pivo(matriz, linha_pivo, coluna)
            linha_pivo += 1

    return matriz


# Procura, da linha_inicial para baixo, a primeira linha que tem um valor
# diferente de zero na coluna. Devolve None quando não existe nenhuma.
def buscar_linha_nao_nula(matriz, linha_inicial, coluna):
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


# Etapa 3: classifica o sistema olhando as linhas da matriz escalonada.
#     "SI"  = Sistema Impossível: não tem solução
#     "SPI" = Sistema Possível e Indeterminado: tem infinitas soluções
#     "SPD" = Sistema Possível e Determinado: tem uma única solução
def classificar_sistema(escalonada):
    num_incognitas = len(escalonada[0]) - 1
    num_pivos = 0

    for linha in escalonada:
        termo_independente = linha[-1]

        if tem_pivo(linha):
            num_pivos += 1
        elif termo_independente != 0:
            # Linha 0 0 ... 0 | c com c diferente de zero: é a equação
            # 0 = c, que nunca é verdadeira.
            return "SI"

    # Menos pivôs que incógnitas: sobram incógnitas livres.
    if num_pivos < num_incognitas:
        return "SPI"

    return "SPD"


# Diz se a linha tem pivô, isto é, algum coeficiente diferente de zero.
# O último valor fica de fora porque é o termo independente.
def tem_pivo(linha):
    for coluna in range(len(linha) - 1):
        if linha[coluna] != 0:
            return True

    return False


# Etapa 4: retrossubstituição. A última linha tem uma incógnita só; depois
# de calculá-la, cada linha de cima usa os valores que já foram descobertos.
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

        termo_independente = escalonada[linha][-1]
        pivo = escalonada[linha][linha]
        solucao[linha] = (termo_independente - soma_conhecida) / pivo

        linha -= 1

    return solucao
