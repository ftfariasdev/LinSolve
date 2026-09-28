import { useEffect, useState } from 'react'
import { apiFetch } from '../api/client.ts'
import { NumericKeyboard } from '../components/NumericKeyboard.jsx'
import { SymbolKeyboard } from '../components/SymbolKeyboard.tsx'

type HealthResponse = {
  status: string
  message: string
}

function CalculatorPage() {
  return (
    <main>
      <h1>Calculadora de Sistemas Lineares</h1>

      <NumericKeyboard />
      <SymbolKeyboard />
    </main>
  )
}

export default CalculatorPage