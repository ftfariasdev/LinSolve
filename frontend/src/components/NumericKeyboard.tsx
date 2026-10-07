import { useState, useEffect } from "react";
import { Button } from "@mui/material";
import styles from "./Keyboard.module.css";

type NumericKeyboardProps = {
  // Chamada a cada dígito digitado (na tela ou no teclado físico)
  onKey: (key: string) => void;
};

function NumericKeyboard({ onKey }: NumericKeyboardProps) {
  // Estado para rastrear qual tecla física está sendo pressionada
  const [activeKey, setActiveKey] = useState<number | null>(null);

  // Função centralizada para lidar com o clique do número
  const handleNumberInput = (number: number) => {
    onKey(String(number));
  }

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Verifica se a tecla digitada é um número de 0 a 9
      if (/^[0-9]$/.test(event.key)) {
        const number = Number(event.key);
        // Ativa o estado visual da tecla correspondente
        setActiveKey(number);
        // Executa a mesma lógica do onClick
        onKey(String(number));
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
  }, [onKey]);

  return(
    <div className={styles.numericKeyboardGrid}>
      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 0].map((x) => {
      // Verifica se este botão específico é o que deve brilhar/mudar de cor
      const isKeyPressed = activeKey === x;

      return (
        <Button
          key={x}
          value={x}
          onClick={() => handleNumberInput(x)}
          variant="contained"
          className={`${styles.keyboardButton} ${isKeyPressed ? styles.activeKey : ""} ${x === 0 ? styles.zeroKey : ""}`}
        >
          {x}
        </Button>
      );
    })}
    </div>
  );
}

export { NumericKeyboard };