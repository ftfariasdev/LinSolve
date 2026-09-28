import { useState, useEffect } from "react";
import { Button } from "@mui/material";
import styles from "./Keyboard.module.css";

function AlphabeticKeyboard() {
  // Estado para rastrear qual tecla física está sendo pressionada
  const [activeKey, setActiveKey] = useState<string | null>(null);

  // Função centralizada para lidar com o clique do número
  const handleStrInput = (str: string) => {
    console.log(str);
  }

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Verifica se a tecla digitada é uma letra do alfabeto
      if (/^[a-zA-Z]$/.test(event.key)) {
        const key = event.key.toLowerCase(); // Converte para minúscula para consistência
        // Ativa o estado visual da tecla correspondente
        setActiveKey(key);
        // Executa a mesma lógica do onClick
        handleStrInput(key);
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

  return(
    <div className={styles.alphabeticKeyboardGrid}>
      { ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'].map((x) => {
        // Verifica se este botão específico é o que deve brilhar/mudar de cor
        const isKeyPressed = activeKey === x;

        return (
          <Button
            key={x}
            value={x}
            onClick={() => handleStrInput(x)}
            variant="contained"
            className={`${styles.keyboardButton} ${isKeyPressed ? styles.activeKey : ""} ${x === 'j' ? styles.lastKey : ""}`}
          >
            {x}
      </Button>
    );
  })}
  </div>
  );
}

export { AlphabeticKeyboard };