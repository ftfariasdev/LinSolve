import { useEffect, useState } from "react";
import { Button } from "@mui/material";
import styles from "./Keyboard.module.css";

type SymbolKeyboardProps = {
  // Chamada a cada símbolo digitado (na tela ou no teclado físico)
  onKey: (key: string) => void;
};

function SymbolKeyboard({ onKey }: SymbolKeyboardProps) {
  const [activeKey, setActiveKey] = useState<string | null>(null);

  useEffect(() => {
    const handleKeyPress = (key: string) => {
      setActiveKey(key);
      onKey(key);

      setTimeout(() => {
        setActiveKey(null);
      }, 100);
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      // Atalhos como Ctrl+- (zoom) não são entrada de texto
      if (event.ctrlKey || event.metaKey || event.altKey) return;

      const keyMap: Record<string, string> = {
        Backspace: "⌫",
        Enter: "↵",
        Escape: "C",
        "+": "+",
        "-": "-",
        "=": "=",
        ".": ".",
        ",": ".",
      };

      const key = keyMap[event.key];

      if (key) {
        event.preventDefault();
        handleKeyPress(key);
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [onKey]);

  const keys = ['+', '⌫', '-', 'C', '.', '↵', '='];

  return (
    <div className={styles.operatorKeyboardGrid}>
      {keys.map((key) => {
        const isKeyPressed = activeKey === key;

        return (
          <Button
            key={key}
            value={key}
            onClick={() => onKey(key)}
            variant="contained"
            className={`${styles.keyboardButton} ${
              isKeyPressed ? styles.activeKey : ""
            }`}
          >
            {key}
          </Button>
        );
      })}
    </div>
  );
}

export { SymbolKeyboard };