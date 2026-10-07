import { useEffect, useRef, useState } from "react";
import { Button } from "@mui/material";
import { solveLinearSystem } from "../api/linearSystem.ts";
import type { SolvedSystem } from "../api/linearSystem.ts";
import { buildSystem, checkLines } from "../utils/systemParser.ts";
import styles from "./SystemInput.module.css";

type SystemInputProps = {
  // Texto montado pelos teclados: uma equação por linha
  text: string;
  // Chamada com a resposta do backend, para o componente de resultado
  onSolved: (solved: SolvedSystem) => void;
};

function SystemInput({ text, onSolved }: SystemInputProps) {
  const [isSolving, setIsSolving] = useState(false);
  // Texto do sistema cuja chamada falhou: o erro some assim que o texto muda
  const [failedText, setFailedText] = useState<string | null>(null);

  // Guarda o texto atual para descartar a resposta de um sistema que já foi editado
  const currentText = useRef(text);
  useEffect(() => {
    currentText.current = text;
  }, [text]);

  // A validação roda a cada tecla: o texto muda, o componente renderiza de novo
  const lines = text.split("\n");
  const checks = checkLines(text);
  const system = buildSystem(checks);

  const handleSolve = async () => {
    if (!system) return;

    setIsSolving(true);
    setFailedText(null);

    try {
      const result = await solveLinearSystem({
        coeficientes: system.coefficients,
        termos_independentes: system.constants,
      });

      if (currentText.current === text) {
        onSolved({ unknowns: system.unknowns, result });
      }
    } catch {
      setFailedText(text);
    } finally {
      setIsSolving(false);
    }
  };

  return (
    <section>
      <div className={styles.field} role="textbox" aria-multiline="true" aria-readonly="true" aria-label="Sistema linear">
        {text === "" && (
          <p className={styles.placeholder}>Digite uma equação por linha, por exemplo 2x+3y=5</p>
        )}

        {text !== "" && lines.map((line, index) => {
          // A linha nova, ainda vazia depois do Enter, não tem validação
          const check = checks[index];
          const isLastLine = index === lines.length - 1;
          const isError = check?.status === "error";
          const showMessage = check && check.status !== "ok" && line !== "";

          return (
            <div key={index} className={`${styles.line} ${isError ? styles.lineError : ""}`}>
              <div className={styles.equation}>
                {line}
                {isLastLine && <span className={styles.caret} />}
              </div>

              {showMessage && (
                <p
                  className={`${styles.message} ${isError ? styles.messageError : styles.messageHint}`}
                  role={isError ? "alert" : undefined}
                >
                  {check.message}
                </p>
              )}
            </div>
          );
        })}
      </div>

      <div className={styles.actions}>
        <Button variant="contained" onClick={handleSolve} disabled={!system || isSolving}>
          {isSolving ? "Resolvendo..." : "Resolver"}
        </Button>

        {failedText === text && (
          <p className={styles.requestError} role="alert">
            Não foi possível resolver o sistema. Verifique se o backend está rodando.
          </p>
        )}
      </div>
    </section>
  );
}

export { SystemInput };
