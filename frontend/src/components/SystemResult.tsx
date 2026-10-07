import type { SolvedSystem } from "../api/linearSystem.ts";
import styles from "./SystemResult.module.css";

type SystemResultProps = {
  solved: SolvedSystem;
};

// Título, explicação e cor de cada classificação
const CLASSIFICATIONS = {
  SPD: {
    title: "Sistema Possível e Determinado (SPD)",
    description: "O sistema tem uma única solução.",
    className: styles.spd,
  },
  SPI: {
    title: "Sistema Possível e Indeterminado (SPI)",
    description:
      "O sistema tem infinitas soluções: depois do escalonamento sobram menos equações do que incógnitas.",
    className: styles.spi,
  },
  SI: {
    title: "Sistema Impossível (SI)",
    description:
      "O sistema não tem solução: o escalonamento chegou a uma equação que nunca é verdadeira, como 0 = 1.",
    className: styles.si,
  },
};

type MatrixTableProps = {
  unknowns: string[];
  // Matriz aumentada: o termo independente é a última coluna de cada linha
  matrix: string[][];
};

function MatrixTable({ unknowns, matrix }: MatrixTableProps) {
  return (
    <div className={styles.matrixScroll}>
      <table className={styles.matrix}>
        <thead>
          <tr>
            {unknowns.map((unknown) => (
              <th key={unknown} scope="col">{unknown}</th>
            ))}
            <th scope="col">=</th>
          </tr>
        </thead>
        <tbody>
          {matrix.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((value, columnIndex) => (
                <td key={columnIndex}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SystemResult({ solved }: SystemResultProps) {
  const { unknowns, result } = solved;
  const classification = CLASSIFICATIONS[result.classificacao];

  return (
    <section className={styles.result} aria-live="polite">
      <div className={`${styles.classification} ${classification.className}`}>
        <h2>{classification.title}</h2>
        <p>{classification.description}</p>
      </div>

      <div className={styles.blocks}>
        <div>
          <h3>Sistema original</h3>
          <MatrixTable unknowns={unknowns} matrix={result.original} />
        </div>

        <div>
          <h3>Sistema escalonado</h3>
          <MatrixTable unknowns={unknowns} matrix={result.escalonada} />
        </div>

        <div>
          <h3>Solução</h3>
          {result.solucao ? (
            <ul className={styles.solution}>
              {unknowns.map((unknown, index) => (
                <li key={unknown}>
                  {unknown} = {result.solucao?.[index]}
                </li>
              ))}
            </ul>
          ) : (
            <p className={styles.noSolution}>
              {result.classificacao === "SPI"
                ? "Não há uma solução única para mostrar."
                : "Não há solução."}
            </p>
          )}
        </div>
      </div>
    </section>
  );
}

export { SystemResult };
