import { BrowserRouter, Route, Routes } from 'react-router-dom'
import HealthPage from './pages/HealthPage.tsx'
import CalculatorPage from './pages/CalculatorPage.tsx'


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CalculatorPage />} />
        <Route path="/health" element={<HealthPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
