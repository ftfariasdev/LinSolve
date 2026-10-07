// Regras de montagem do sistema linear digitado pelo usuário.
//
// Cada linha do campo é uma equação na forma:
//
//     2x + 3y - z = 5
//
//   - antes do "=": termos na ordem coeficiente → incógnita → operador;
//   - depois do "=": só o termo independente (um número, com sinal opcional);
//   - incógnita sem coeficiente vale 1 (x é o mesmo que 1x);
//   - o coeficiente não pode ser 0;
//   - uma incógnita não pode aparecer duas vezes na mesma equação.
//
// O resultado final segue o contrato da issue #1: a matriz de coeficientes e
// a lista de termos independentes, com as colunas em ordem alfabética das
// incógnitas usadas no sistema.

export type LineCheck =
  | { status: 'ok'; coefficients: Record<string, number>; constant: number }
  // "incomplete": ainda dá para consertar continuando a digitar.
  // "error": só apagando.
  | { status: 'incomplete' | 'error'; message: string }

export type LinearSystem = {
  unknowns: string[]
  coefficients: number[][]
  constants: number[]
}

// Caracteres que o campo aceita, além da quebra de linha.
const ALLOWED_CHARACTER = /^[0-9a-z+\-=.]$/

const TOKEN = /\d+(?:\.\d*)?|[a-z]|[+\-=.]/g

function incomplete(message: string): LineCheck {
  return { status: 'incomplete', message }
}

function error(message: string): LineCheck {
  return { status: 'error', message }
}

function isNumber(token: string) {
  return /^\d/.test(token)
}

function isLetter(token: string) {
  return /^[a-z]$/.test(token)
}

function isOperator(token: string) {
  return token === '+' || token === '-'
}

/** Valida uma equação e devolve os coeficientes e o termo independente. */
export function checkLine(line: string): LineCheck {
  const tokens = line.match(TOKEN) ?? []

  const coefficients: Record<string, number> = {}
  let constant: number | null = null

  let side: 'left' | 'right' = 'left'
  // O que acabou de ser lido: nada (início do lado), um operador, um número
  // ainda sem incógnita ou um termo completo.
  let last: 'start' | 'operator' | 'number' | 'term' = 'start'
  let sign = 1
  let number = ''

  for (const token of tokens) {
    if (token === '.') {
      return last === 'number'
        ? error(`O número ${number} já tem ponto decimal.`)
        : error('Digite um número antes do ponto.')
    }

    if (last === 'number' && number.endsWith('.')) {
      return error(`Faltam as casas decimais de ${number}`)
    }

    if (isNumber(token)) {
      if (last === 'term') {
        return error(`Falta um operador (+ ou -) antes de ${token}.`)
      }
      number = token
      last = 'number'
      if (side === 'right') {
        constant = sign * Number(token)
      }
    } else if (isLetter(token)) {
      if (side === 'right') {
        return error('Depois do "=" só entra o termo independente (um número).')
      }
      if (last === 'term') {
        return error(`Falta um operador (+ ou -) antes de "${token}".`)
      }
      // Sem número antes, o coeficiente é 1: "x" vale "1x" e "-x" vale "-1x".
      const coefficient = last === 'number' ? Number(number) : 1
      if (coefficient === 0) {
        return error(`O coeficiente de "${token}" não pode ser 0.`)
      }
      if (token in coefficients) {
        return error(`A incógnita "${token}" aparece mais de uma vez na equação.`)
      }
      coefficients[token] = sign * coefficient
      sign = 1
      last = 'term'
    } else if (isOperator(token)) {
      if (last === 'operator') {
        return error('Dois operadores seguidos.')
      }
      if (last === 'number') {
        return side === 'left'
          ? error(`Falta a incógnita depois de ${number}.`)
          : error('Depois do "=" só entra o termo independente (um número).')
      }
      sign = token === '-' ? -1 : 1
      last = 'operator'
    } else {
      // token === '='
      if (side === 'right') {
        return error('A equação só pode ter um "=".')
      }
      if (last === 'number') {
        return error(`Falta a incógnita depois de ${number}.`)
      }
      if (last !== 'term') {
        return error('Falta um termo antes do "=".')
      }
      side = 'right'
      last = 'start'
    }
  }

  if (last === 'number' && number.endsWith('.')) {
    return incomplete(`Faltam as casas decimais de ${number}`)
  }
  if (side === 'left') {
    if (last === 'number') {
      return incomplete(`Falta a incógnita depois de ${number}.`)
    }
    if (last === 'term') {
      return incomplete('Falta o "=" e o termo independente.')
    }
    return incomplete('Falta um termo, por exemplo 2x.')
  }
  if (constant === null) {
    return incomplete('Falta o termo independente depois do "=".')
  }

  return { status: 'ok', coefficients, constant }
}

/** Aplica uma tecla (dos teclados da tela ou do teclado físico) ao texto. */
export function applyKey(text: string, key: string): string {
  if (key === 'C') {
    return ''
  }
  if (key === '⌫') {
    return text.slice(0, -1)
  }
  if (key === '↵') {
    // Só abre uma equação nova quando a atual já tem alguma coisa.
    return text === '' || text.endsWith('\n') ? text : text + '\n'
  }
  return ALLOWED_CHARACTER.test(key) ? text + key : text
}

/**
 * Valida cada linha do texto digitado. A última linha é a que está sendo
 * digitada, então pode ficar "incomplete"; nas anteriores, o que falta já
 * conta como erro.
 */
export function checkLines(text: string): LineCheck[] {
  const lines = text.split('\n')

  // Depois do Enter sobra uma linha nova ainda vazia: ela não é uma equação,
  // e as de cima já foram todas encerradas.
  const hasEmptyNewLine = lines.length > 1 && lines[lines.length - 1] === ''
  if (hasEmptyNewLine) {
    lines.pop()
  }

  return lines.map((line, index) => {
    const check = checkLine(line)
    const isBeingTyped = !hasEmptyNewLine && index === lines.length - 1

    if (check.status === 'incomplete' && !isBeingTyped) {
      return { status: 'error', message: check.message }
    }
    return check
  })
}

/**
 * Monta a matriz de coeficientes e os termos independentes. Devolve null
 * enquanto alguma equação não estiver válida.
 */
export function buildSystem(checks: LineCheck[]): LinearSystem | null {
  const equations = []
  for (const check of checks) {
    if (check.status !== 'ok') {
      return null
    }
    equations.push(check)
  }

  const unknowns = [
    ...new Set(equations.flatMap((equation) => Object.keys(equation.coefficients))),
  ].sort()

  return {
    unknowns,
    // Incógnita que não aparece na equação entra com coeficiente 0.
    coefficients: equations.map((equation) =>
      unknowns.map((unknown) => equation.coefficients[unknown] ?? 0),
    ),
    constants: equations.map((equation) => equation.constant),
  }
}
