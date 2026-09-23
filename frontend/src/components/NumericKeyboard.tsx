import { useState, useEffect } from "react";
import { Button } from "@mui/material";
import styles from "./Keyboard.module.css";

function NumericKeyboard() {
  // Estado para rastrear qual tecla física está sendo pressionada
  const [activeKey, setActiveKey] = useState<number | null>(null);

  // Função centralizada para lidar com o clique do número
  const handleNumberInput = (number: number) => {
    console.log(number);
  }

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Verifica se a tecla digitada é um número de 0 a 9
      if (/^[0-9]$/.test(event.key)) {
        const number = Number(event.key);
        // Ativa o estado visual da tecla correspondente
        setActiveKey(number);
        // Executa a mesma lógica do onClick
        handleNumberInput(number);
        setTimeout(() => {
          setActiveKey(null);
        }, 100); // Remove o estado ativo após 100ms
      }
    }

    // Escuta o teclado do PC globalmente
    window.addEventListener("keydown", handleKeyDown);

    // Limpa o listener para não pesar a memória
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  return [1, 2, 3, 4, 5, 6, 7, 8, 9, 0].map((x) => {
    // Verifica se este botão específico é o que deve brilhar/mudar de cor
    const isKeyPressed = activeKey === x;

    return (
      <Button
        key={x}
        value={x}
        onClick={() => handleNumberInput(x)}
        variant="contained"
        className={`${styles.keyboardButton} ${isKeyPressed ? styles.activeKey : ""}`}
      >
        {x}
      </Button>
    );
  });
}

export { NumericKeyboard };