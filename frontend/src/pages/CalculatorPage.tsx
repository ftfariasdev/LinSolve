import { useCallback, useState } from 'react'
import { NumericKeyboard } from '../components/NumericKeyboard.jsx'
import { AlphabeticKeyboard } from '../components/AlphabeticKeyboard.tsx'
import { SymbolKeyboard } from '../components/SymbolKeyboard.tsx'
import { SystemInput } from '../components/SystemInput.tsx'
import { SystemResult } from '../components/SystemResult.tsx'
import type { SolvedSystem } from '../api/linearSystem.ts'
import { applyKey } from '../utils/systemParser.ts'
import styles from '../components/Keyboard.module.css'

function CalculatorPage() {
  // Texto do sistema: uma equação por linha
  const [text, setText] = useState('')
  const [solved, setSolved] = useState<SolvedSystem | null>(null)

  // Os três teclados (e o teclado físico, que eles escutam) chegam aqui
  const handleKey = useCallback((key: string) => {
    setText((current) => applyKey(current, key))
    // O resultado na tela era do sistema anterior
    setSolved(null)
  }, [])

  return (
    <main>
      <h1 className={styles.pageTitle}>Calculadora de Sistemas Lineares</h1>

      <SystemInput text={text} onSolved={setSolved} />

      <div className={styles.keyboardContainer}>
        
        <NumericKeyboard onKey={handleKey} />

        <AlphabeticKeyboard onKey={handleKey} />

        <SymbolKeyboard onKey={handleKey} />

      </div>

      {solved && <SystemResult solved={solved} />}
    </main>
  )
}

export default CalculatorPage
