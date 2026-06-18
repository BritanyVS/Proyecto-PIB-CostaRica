from __future__ import annotations

import pandas as pd


class ControlEstadistico:
    def __init__(self, data: pd.DataFrame, column: str) -> None:
        self.data = data.copy()
        self.column = column

    def calculate(self) -> pd.DataFrame:
        if self.column not in self.data.columns:
            raise ValueError(
                f"La columna '{self.column}' no existe en el conjunto de datos."
            )

        result = self.data[["Fecha", self.column]].copy()
        result = result.dropna(subset=[self.column]).reset_index(drop=True)

        media = result[self.column].mean()
        desviacion = result[self.column].std()

        ucl = media + (3 * desviacion)
        lcl = media - (3 * desviacion)

        result["Media"] = media
        result["UCL"] = ucl
        result["LCL"] = lcl

        result["Estado"] = result[self.column].apply(
            lambda x: "Fuera de control"
            if x > ucl or x < lcl
            else "Normal"
        )

        result.attrs["media"] = float(media)
        result.attrs["desviacion"] = float(desviacion)
        result.attrs["ucl"] = float(ucl)
        result.attrs["lcl"] = float(lcl)
        result.attrs["fuera_control"] = int(
            (result["Estado"] == "Fuera de control").sum()
        )

        return result