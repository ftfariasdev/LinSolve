// URL base da API. Vazia por padrão: as chamadas vão para "/api/..." no próprio
// servidor do Vite, que repassa para o Django (ver vite.config.ts).
const API_URL = import.meta.env.VITE_API_URL ?? ''

/**
 * Função base para chamar o backend.
 * Retorna o JSON da resposta e lança um erro se o status não for 2xx.
 *
 * Exemplo: const dados = await apiFetch<HealthResponse>('/api/health/')
 */
export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, options)

  if (!response.ok) {
    throw new Error(`Erro ${response.status} ao acessar ${path}`)
  }

  return response.json() as Promise<T>
}
