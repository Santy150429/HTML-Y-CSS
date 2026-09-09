
# Este archivo almacena la informacion del programa

import json

archivo_datos = "horarios.json"
archivo_reporte = "reporte_horario.json"
archivo_calendario = "calendario.json"


def cargar_datos():
    "carga los datos guardados de archivo json"
    try:
        with open(archivo_datos, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def guardar_datos(horarios):
    "Guarda los horarios en el archivo Json"
    with open(archivo_datos, "w", encoding="utf-8") as f:
        json.dump(horarios, f, indent=4, ensure_ascii=False)


def guardar_reporte(reporte):
    "guarda el reporte en un archivo Json"
    with open(archivo_reporte, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=4, ensure_ascii=False)       


def guardar_calendario(calendario):
    "guarda el calendario en un archivo Json"
    with open(archivo_calendario, "W", encoding="utf-8") as f:
        json.dump(calendario, f, indent=4, ensure_ascii=False)