from __future__ import annotations

import pandas as pd
from scipy.optimize import linprog


class ProgramacionLineal:

    def __init__(
        self,
        data: pd.DataFrame,
        sectores: list[str],
        presupuesto: float,
    ) -> None:

        self.data = data.copy()
        self.sectores = sectores
        self.presupuesto = presupuesto

    def calculate(self):

        if len(self.sectores) < 2:
            raise ValueError(
                "Debe seleccionar al menos dos sectores."
            )

        coeficientes = []

        for sector in self.sectores:

            promedio = (
                self.data[sector]
                .dropna()
                .mean()
            )

            coeficientes.append(promedio)

        c = [-x for x in coeficientes]

        A_ub = [
            [1] * len(self.sectores)
        ]

        b_ub = [
            self.presupuesto
        ]

        bounds = [
            (5, 40)
            for _ in self.sectores
        ]

        resultado = linprog(
            c=c,
            A_ub=A_ub,
            b_ub=b_ub,
            bounds=bounds,
            method="highs"
        )

        asignacion = pd.DataFrame(
            {
                "Sector": self.sectores,
                "Asignacion": resultado.x.round(2)
            }
        )

        asignacion.attrs["valor_optimo"] = (
            -resultado.fun
        )

        return asignacion