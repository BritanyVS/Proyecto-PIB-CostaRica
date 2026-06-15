from __future__ import annotations

import pandas as pd


class PromedioMovil:
    def __init__(self, data: pd.DataFrame, column: str, window: int) -> None:
        self.data = data.copy()
        self.column = column
        self.window = window

    def calculate(self) -> pd.DataFrame:
        if self.column not in self.data.columns:
            raise ValueError(f"La columna '{self.column}' no existe en el conjunto de datos.")

        if self.window < 2:
            raise ValueError("La ventana del promedio movil debe ser mayor o igual a 2.")

        result = self.data[["Fecha", self.column]].copy()
        result["Promedio_Movil"] = result[self.column].rolling(window=self.window).mean()
        result = result.dropna(subset=["Promedio_Movil"]).reset_index(drop=True)
        return result