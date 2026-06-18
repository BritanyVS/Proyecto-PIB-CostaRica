from __future__ import annotations

import pandas as pd


class CadenaMarkov:

    ESTADOS = [
        "Crecimiento",
        "Estancamiento",
        "Recesion"
    ]

    def __init__(self, data: pd.DataFrame, column: str) -> None:
        self.data = data.copy()
        self.column = column

    def _clasificar_estado(self, variacion: float) -> str:

        if variacion > 2:
            return "Crecimiento"

        if variacion < -2:
            return "Recesion"

        return "Estancamiento"

    def calculate(self):

        result = self.data[["Fecha", self.column]].copy()

        result = result.dropna()

        result["Variacion"] = (
            result[self.column]
            .pct_change()
            * 100
        )

        result = result.dropna().reset_index(drop=True)

        result["Estado"] = (
            result["Variacion"]
            .apply(self._clasificar_estado)
        )

        matriz = pd.DataFrame(
            0,
            index=self.ESTADOS,
            columns=self.ESTADOS
        )

        estados = result["Estado"].tolist()

        for i in range(len(estados) - 1):

            actual = estados[i]
            siguiente = estados[i + 1]

            matriz.loc[actual, siguiente] += 1

        matriz_prob = matriz.div(
            matriz.sum(axis=1),
            axis=0
        ).fillna(0)

        result.attrs["matriz"] = matriz_prob

        return result