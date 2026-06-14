from pathlib import Path
from typing import Any

import pandas as pd

from .config import COLUMNS, get_excel_path


def _load_dataframe(source: Any) -> pd.DataFrame:
    data = pd.read_excel(source, skiprows=4, header=None, names=COLUMNS)
    data = data[data["Fecha"] != "Fecha"].copy()
    data["Fecha"] = pd.to_datetime(data["Fecha"], errors="coerce")
    data = data.dropna(subset=["Fecha"]).reset_index(drop=True)

    for column in data.columns:
        if column != "Fecha":
            data[column] = pd.to_numeric(data[column], errors="coerce")

    return data


def load_data_from_excel(source: Any) -> pd.DataFrame:
    if isinstance(source, (str, Path)):
        return _load_dataframe(source)

    if hasattr(source, "seek"):
        try:
            source.seek(0)
        except Exception:
            pass

    return _load_dataframe(source)


def load_default_data() -> pd.DataFrame | None:
    try:
        return load_data_from_excel(get_excel_path())
    except FileNotFoundError:
        return None