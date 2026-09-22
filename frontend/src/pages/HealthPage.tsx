import { useEffect, useState } from 'react'
import { apiFetch } from '../api/client.ts'

type HealthResponse = {
  status: string
  message: string
}

function HealthPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    apiFetch<HealthResponse>('/api/health/')
      .then((data) => setHealth(data))
      .catch(() => setError(true))
  }, [])

  return (
    <main>
      <h1>Calculadora de Sistemas Lineares</h1>

      {error ? (
        <p className="error">
          Não foi possível conectar ao backend. Verifique se ele está rodando em
          http://localhost:8000.
        </p>
      ) : health ? (
        <p className="success">
          {health.message} (status: {health.status})
        </p>
      ) : (
        <p>Carregando...</p>
      )}
    </main>
  )
}

export default HealthPage
