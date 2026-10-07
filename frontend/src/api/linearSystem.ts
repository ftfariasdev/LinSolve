import { apiFetch } from './client.ts'

// Contrato do POST /api/linear-system/solve/ (issue #1).
// Cada linha de "coeficientes" é uma equação e cada coluna, uma incógnita.
export type SolveRequest = {
  coeficientes: number[][]
  termos_independentes: number[]
}

// Os números voltam como texto, em fração exata: "3", "-11", "1/3".
// "original" e "escalonada" são matrizes aumentadas (termo independente na
// última coluna). "solucao" só vem preenchida quando o sistema é SPD.
export type SolveResponse = {
  original: string[][]
  escalonada: string[][]
  classificacao: 'SPD' | 'SPI' | 'SI'
  solucao: string[] | null
}

// O que o campo de input entrega para o componente de resultado: a resposta
// do backend e o nome da incógnita de cada coluna.
export type SolvedSystem = {
  unknowns: string[]
  result: SolveResponse
}

export async function solveLinearSystem(request: SolveRequest): Promise<SolveResponse> {
  const response = await apiFetch<SolveResponse>('/api/linear-system/solve/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  })

  if (typeof response.classificacao !== 'string') {
    throw new Error('O backend não devolveu a resolução do sistema.')
  }

  return response
}
