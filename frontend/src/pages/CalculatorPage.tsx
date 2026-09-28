import { useEffect, useState } from 'react'
import { apiFetch } from '../api/client.ts'
import { NumericKeyboard } from '../components/NumericKeyboard.jsx'
import { AlphabeticKeyboard } from '../components/AlphabeticKeyboard.tsx'

type HealthResponse = {
  status: string
  message: string
}

function CalculatorPage() {
  return (
    <main>
      <h1>Calculadora de Sistemas Lineares</h1>

      <NumericKeyboard />
      <AlphabeticKeyboard />
    </main>
  )
}

export default CalculatorPage
