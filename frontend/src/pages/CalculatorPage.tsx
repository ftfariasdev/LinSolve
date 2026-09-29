import { NumericKeyboard } from '../components/NumericKeyboard.jsx'
import { AlphabeticKeyboard } from '../components/AlphabeticKeyboard.tsx'
import { SymbolKeyboard } from '../components/SymbolKeyboard.tsx'
import styles from '../components/Keyboard.module.css'

function CalculatorPage() {
  return (
    <main>
      <h1 className={styles.pageTitle}>Calculadora de Sistemas Lineares</h1>

      <div className={styles.keyboardContainer}>
        
        <NumericKeyboard />

        <AlphabeticKeyboard />

        <SymbolKeyboard />

      </div>
    </main>
  )
}

export default CalculatorPage