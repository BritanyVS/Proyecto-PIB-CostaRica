from __future__ import annotations

import numpy as np
import pandas as pd


class RegresionLineal:
    def __init__(self, data: pd.DataFrame, column: str) -> None:
        self.data = data.copy()
        self.column = column

    def calculate(self) -> pd.DataFrame:
        if self.column not in self.data.columns:
            raise ValueError(f"La columna '{self.column}' no existe en el conjunto de datos.")

        result = self.data[["Fecha", self.column]].copy().reset_index(drop=True)
        result = result.dropna(subset=[self.column]).reset_index(drop=True)

        if len(result) < 2:
            raise ValueError("Se necesitan al menos 2 observaciones para ajustar una regresion lineal.")

        x = np.arange(len(result), dtype=float)
        y = result[self.column].astype(float).to_numpy()

        slope, intercept = np.polyfit(x, y, deg=1)
        predicted = slope * x + intercept

        ss_res = float(np.sum((y - predicted) ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        r_squared = 1.0 if ss_tot == 0 else 1 - (ss_res / ss_tot)

        result["Valor_Predicho"] = predicted
        result["Residuo"] = result[self.column] - result["Valor_Predicho"]
        result.attrs["slope"] = float(slope)
        result.attrs["intercept"] = float(intercept)
        result.attrs["r_squared"] = float(r_squared)
        return result