# Contrato de dados (RFC — issue #1)

Decisões que valem para o frontend e para o backend. Elas descrevem o que já
está implementado no motor de escalonamento (`backend/services/linear_system.py`)
e no campo de input (`frontend/src/utils/systemParser.ts`).

## 1. Incógnitas

- Cada incógnita é **uma letra minúscula** (`a` a `z`). O teclado da tela oferece
  de `a` a `j`; as outras letras entram pelo teclado físico.
- A quantidade é **dinâmica**: as incógnitas do sistema são as letras que
  aparecem em pelo menos uma equação.
- As colunas da matriz seguem a **ordem alfabética** das incógnitas. Quando uma
  incógnita não aparece em uma equação, o coeficiente dela é `0`.
- O backend não recebe os nomes das incógnitas, só a matriz. O frontend guarda
  a lista de nomes para rotular o resultado (a coluna `i` é a incógnita `i`).

## 2. Formato enviado ao backend

O frontend faz o parsing das equações e manda a matriz pronta; o backend não
interpreta texto de equação.

`POST /api/linear-system/solve/`

```
2x + 3y - z = 5
x - y + 2z = 3
```

```json
{
  "coeficientes": [[2, 3, -1], [1, -1, 2]],
  "termos_independentes": [5, 3]
}
```

- `coeficientes`: uma linha por equação, uma coluna por incógnita.
- `termos_independentes`: um valor por equação, na mesma ordem.
- Os valores são números JSON, inteiros ou decimais (`0.5`).
- O sistema não precisa ser quadrado.

Resposta:

```json
{
  "original": [["2", "3", "-1", "5"], ["1", "-1", "2", "3"]],
  "escalonada": [["2", "3", "-1", "5"], ["0", "-5/2", "5/2", "1/2"]],
  "classificacao": "SPI",
  "solucao": null
}
```

- `original` e `escalonada`: matrizes aumentadas (o termo independente é a
  última coluna de cada linha).
- Os números voltam como **texto em fração exata** (`"3"`, `"-11"`, `"1/3"`),
  prontos para mostrar na tela.
- `classificacao`: `"SPD"`, `"SPI"` ou `"SI"`.
- `solucao`: um valor por incógnita, na ordem das colunas, quando o sistema é
  SPD; `null` nos outros casos.

## 3. Estratégia de escalonamento

- Eliminação de Gauss **sem troca de linhas**, exceto quando o pivô da linha
  atual é zero: aí a linha troca com a **primeira linha abaixo** que tem valor
  diferente de zero naquela coluna.
- Se nenhuma linha abaixo serve, a coluna fica sem pivô e a mesma linha tenta
  de novo na coluna seguinte.
- As contas usam frações, então o resultado é exato e determinístico (é isso
  que torna os testes da issue #5 verificáveis).

## Regras do campo de input (issue #8)

Cada linha do campo é uma equação:

- antes do `=`: termos na ordem coeficiente → incógnita → operador (`2x+3y-z`);
- depois do `=`: só o termo independente, um número com sinal opcional;
- incógnita sem coeficiente vale 1 (`x` é o mesmo que `1x`);
- o coeficiente não pode ser `0` (`0x` é erro);
- uma incógnita não pode aparecer duas vezes na mesma equação;
- decimais usam ponto (`0.5`).
