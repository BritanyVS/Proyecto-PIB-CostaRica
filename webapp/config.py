from pathlib import Path


APP_TITLE = "PIB Costa Rica"

COLUMNS = [
    "Fecha",
    "PIB_Precios_Mercado",
    "Impuestos",
    "Valor_Agregado",
    "Agricultura",
    "Minas",
    "Manufactura",
    "Electricidad_Agua",
    "Construccion",
    "Comercio",
    "Transporte",
    "Alojamiento",
    "Telecomunicaciones",
    "Financieras",
    "Inmobiliarias",
    "Profesionales",
    "Admin_Publica",
    "Educacion_Salud",
    "Otras",
    "PIB_Var_Interanual",
    "Impuestos_Var",
    "Valor_Agregado_Var",
    "Agricultura_Var",
    "Minas_Var",
    "Manufactura_Var",
    "Electricidad_Var",
    "Construccion_Var",
    "Comercio_Var",
    "Transporte_Var",
    "Alojamiento_Var",
    "Telecom_Var",
    "Financieras_Var",
    "Inmobiliarias_Var",
    "Profesionales_Var",
    "Admin_Var",
    "Educacion_Var",
    "Otras_Var",
]

PALETA = {
    "fondo": "#fbfefb",
    "panel": "#f2fbf4",
    "panel_fuerte": "#e3f7e7",
    "acento": "#cfeecf",
    "texto": "#284332",
    "texto_suave": "#6f8d76",
    "blanco": "#ffffff",
    "linea": "#dfeee2",
    "seleccion": "#f2fbf4",
}


def get_excel_path() -> Path:
    project_root = Path(__file__).resolve().parent.parent
    candidates = [
        project_root / "Producto interno bruto por actividad económica.xlsx",
        project_root.parent / "Producto interno bruto por actividad económica.xlsx",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    searched = "\n".join(str(path) for path in candidates)
    raise FileNotFoundError(f"No se encontro el archivo Excel. Rutas revisadas:\n{searched}")