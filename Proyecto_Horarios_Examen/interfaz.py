
# Este archivo se encarga de mostrar la informacion en consola

from operaciones import dias_validos

eventos_por_pagina = 5


def limpiar_texto(texto):
    "Convierte a minúsculas, elimina espacios extras y remueve tildes"
    texto = texto.lower().strip()
    reemplazos = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    for origen, destino in reemplazos:
        texto = texto.replace(origen, destino)
    return texto


def horas_a_minutos(hora_str):
    try:
        horas, minutos = map(int, hora_str.strip().split(":"))
        return horas * 60 + minutos
    except ValueError:
        return -1


def formato_12h(hora_str):
    "convierte HH:MM (24h) a hh:MM AM/PM"
    try:
        horas, minutos = map(int, hora_str.split(":"))
    except ValueError:
        return hora_str
    periodo = "AM" if horas < 12 else "PM"
    hora_12 = horas % 12
    if hora_12 == 0:
        hora_12 = 12
    return f"{hora_12:02d}:{minutos:02d} {periodo}"


def ver_horario_semanal(horarios, estudiante):
    "Muestra el horario semanal de un estudiante"

    materias_estudiante = []
    for evento in horarios:
        if limpiar_texto(evento.get("estudiante", "")) == limpiar_texto(estudiante):
            materias_estudiante.append(evento)

    if not materias_estudiante:
        print(f"\nNo hay materias registradas para {estudiante}")
        return

    # franjas armadas segun las horas que realmente se registraron,
    # asi ningun evento se queda por fuera de la tabla
    horas_inicio = sorted({e["hora_inicio"] for e in materias_estudiante}, key=horas_a_minutos)

    print("\n" + "=" * 100)
    print(f"HORARIO DE: {estudiante.upper()}")
    print("=" * 100)
    print(f"{'Hora':<15} | " + " | ".join(f"{dia:<12}" for dia in dias_validos))
    print("=" * 100)

    for hora_inicio in horas_inicio:
        fila = f"{formato_12h(hora_inicio):<15} | "

        for dia in dias_validos:
            actividad = "Libre"

            for evento in materias_estudiante:
                if limpiar_texto(dia) in limpiar_texto(evento["dia"]) and evento["hora_inicio"] == hora_inicio:
                    actividad = evento["materia"]
                    break

            fila += f"{actividad:<12} | "

        print(fila)

    print("=" * 100)


def mostrar_reporte_paginado(reporte):
    "Muestra el reporte del horario en consola, pidiendo ENTER cada cierto numero de eventos"

    if not reporte:
        print("\nNo hay materias registradas para generar el reporte.")
        return

    print("\n" + "=" * 42)
    print("REPORTE DEL HORARIO SEMANAL")
    print("=" * 42)

    contador = 0
    for bloque_dia in reporte:
        print(f"\n{bloque_dia['dia']}:")

        for evento in bloque_dia["eventos"]:
            print(f"- {evento['materia']} ({evento['hora_inicio']} - {evento['hora_fin']}) en {evento['ubicacion']}")
            contador += 1

            if contador % eventos_por_pagina == 0:
                input("\nPresione ENTER para continuar...")

        print("-" * 42)

    print("\nReporte tambien guardado en 'reporte_horario.json'.")