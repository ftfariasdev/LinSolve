import { useEffect, useState } from "react";
import { Button } from "@mui/material";
import styles from "./Keyboard.module.css";

function SymbolKeyboard() {
  const [activeKey, setActiveKey] = useState<string | null>(null);

  const handleStrInput = (str: string) => {
    console.log(str);
  };

  const handleKeyPress = (key: string) => {
    setActiveKey(key);
    handleStrInput(key);

    setTimeout(() => {
      setActiveKey(null);
    }, 100);
  };

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      const keyMap: Record<string, string> = {
        Backspace: "⌫",
        Enter: "↵",
        "+": "+",
        "-": "-",
        "=": "=",
        ".": ".",
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
  }, []);

  const keys = ['+', '⌫', '-', 'C', '.', '↵', '='];

  return (
    <div className={styles.operatorKeyboardGrid}>
      {keys.map((key) => {
        const isKeyPressed = activeKey === key;

        return (
          <Button
            key={key}
            value={key}
            onClick={() => handleKeyPress(key)}
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