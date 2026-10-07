# Formato de entrada e saída do POST /api/linear-system/solve/.
#
# Aqui fica só a validação do formato: se chegou uma matriz de números, com
# as dimensões batendo. A resolução do sistema fica em services/.

from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator

# Número inteiro ou decimal. NaN e infinito não entram: não são coeficientes.
Numero = Annotated[int | float, Field(allow_inf_nan=False)]


class SolveRequest(BaseModel):
    # Uma linha por equação, uma coluna por incógnita.
    coeficientes: list[list[Numero]]
    # Um valor por equação, na mesma ordem das linhas de "coeficientes".
    termos_independentes: list[Numero]

    @model_validator(mode="after")
    def validar_dimensoes(self):
        if len(self.coeficientes) == 0:
            raise ValueError("O sistema precisa ter pelo menos uma equação.")

        num_incognitas = len(self.coeficientes[0])
        if num_incognitas == 0:
            raise ValueError("O sistema precisa ter pelo menos uma incógnita.")

        for equacao in self.coeficientes:
            if len(equacao) != num_incognitas:
                raise ValueError(
                    "Todas as equações precisam ter a mesma quantidade de coeficientes."
                )

        if len(self.termos_independentes) != len(self.coeficientes):
            raise ValueError(
                "A quantidade de termos independentes precisa ser igual à de equações."
            )

        return self


class SolveResponse(BaseModel):
    # Matrizes aumentadas: em cada linha, os coeficientes e, por último, o
    # termo independente. Os números vêm como texto: "3", "-11", "1/3".
    original: list[list[str]]
    escalonada: list[list[str]]
    # SPD = possível e determinado, SPI = possível e indeterminado, SI = impossível.
    classificacao: Literal["SPD", "SPI", "SI"]
    # Um valor por incógnita, na ordem das colunas. Só existe quando é SPD.
    solucao: list[str] | None
