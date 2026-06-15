from __future__ import annotations

import pandas as pd


class SuavizamientoExponencial:
    def __init__(self, data: pd.DataFrame, column: str, alpha: float) -> None:
        self.data = data.copy()
        self.column = column
        self.alpha = alpha

    def calculate(self) -> pd.DataFrame:
        if self.column not in self.data.columns:
            raise ValueError(f"La columna '{self.column}' no existe en el conjunto de datos.")

        if not 0 < self.alpha <= 1:
            raise ValueError("El valor de alpha debe estar entre 0 y 1.")

        result = self.data[["Fecha", self.column]].copy().reset_index(drop=True)
        result["Suavizamiento_Exponencial"] = result[self.column].ewm(alpha=self.alpha, adjust=False).mean()
        return result