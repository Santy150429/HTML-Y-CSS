
# Este archivo contiene la logica de negocio del programa

import json
from almacenamiento import guardar_datos, guardar_reporte

dias_validos = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]


def limpiar_texto(texto):
    "Convierte a minúsculas, elimina espacios extras y remueve tildes"
    texto = texto.lower().strip()
    reemplazos = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    for origen, destino in reemplazos:
        texto = texto.replace(origen, destino)
    return texto


def dia_valido(dia):
    "revisa que el dia este dentro de lunes a viernes"
    return limpiar_texto(dia) in [limpiar_texto(d) for d in dias_validos]


def horas_a_minutos(hora_str):
    try:
        partes = hora_str.strip().split(":")
        if len(partes) != 2:
            return -1
        horas, minutos = int(partes[0]), int(partes[1])
        if not (0 <= horas <= 23) or not (0 <= minutos <= 59):
            return -1
        return horas * 60 + minutos
    except ValueError:
        return -1


def hay_conflicto(horarios, estudiante, dia, hora_inicio, hora_fin, materia_actual=None):

    if not dia_valido(dia):
        return True, f"Dia invalido. Debe ser uno de: {', '.join(dias_validos)}."

    hora_inicio_nuevo = horas_a_minutos(hora_inicio)
    hora_fin_nuevo = horas_a_minutos(hora_fin)

    if hora_inicio_nuevo == -1 or hora_fin_nuevo == -1:
        return True, "El formato de hora debe ser HH:MM (24 horas), con valores validos."

    if hora_inicio_nuevo >= hora_fin_nuevo:
        return True, "La hora de inicio debe ser menor a la hora de fin."

    for evento in horarios:
        if evento.get("estudiante", "").lower() == estudiante.lower():
            if materia_actual and evento["materia"].lower() == materia_actual.lower() and evento["dia"].lower() == dia.lower():
                continue

            if evento["dia"].lower() == dia.lower():
                hora_inicio_existente = horas_a_minutos(evento["hora_inicio"])
                hora_fin_existente = horas_a_minutos(evento["hora_fin"])

                if max(hora_inicio_nuevo, hora_inicio_existente) < min(hora_fin_nuevo, hora_fin_existente):
                    return True, f"Choque de horario con '{evento['materia']}' ({evento['hora_inicio']} - {evento['hora_fin']})."

    return False, ""


def registrar_materia(horarios, estudiante, materia, dia, hora_inicio, hora_fin, ubicacion):
    conflicto, msj = hay_conflicto(horarios, estudiante, dia, hora_inicio, hora_fin)
    if conflicto:
        return False, msj

    nuevo_evento = {
        "estudiante": estudiante,
        "materia": materia,
        "dia": dia.capitalize(),
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "ubicacion": ubicacion if ubicacion else "No especificada"
    }
    horarios.append(nuevo_evento)
    guardar_datos(horarios)
    return True, f"Materia '{materia}' registrada exitosamente para {estudiante}."


def modificar_materia(horarios, estudiante, materia_actual, nueva_materia, nuevo_dia, nueva_hora_inicio, nueva_hora_fin, nueva_ubicacion):
    conflicto, msj = hay_conflicto(horarios, estudiante, nuevo_dia, nueva_hora_inicio, nueva_hora_fin, materia_actual)
    if conflicto:
        return False, msj

    encontrado = False
    for evento in horarios:
        if evento.get("estudiante", "").lower() == estudiante.lower() and evento["materia"].lower() == materia_actual.lower():
            evento["materia"] = nueva_materia
            evento["dia"] = nuevo_dia.capitalize()
            evento["hora_inicio"] = nueva_hora_inicio
            evento["hora_fin"] = nueva_hora_fin
            evento["ubicacion"] = nueva_ubicacion if nueva_ubicacion else "Sin asignacion"
            encontrado = True
            break

    if not encontrado:
        return False, f"No se encontro la materia '{materia_actual}' para {estudiante}."

    guardar_datos(horarios)
    return True, "Materia actualizada exitosamente."


def eliminar_materia(horarios, estudiante, materia):
    nuevos_horarios = []
    encontrado = False

    for evento in horarios:
        if evento.get("estudiante", "").lower() == estudiante.lower() and evento["materia"].lower() == materia.lower():
            encontrado = True
        else:
            nuevos_horarios.append(evento)

    if not encontrado:
        return False, f"No se encontro la materia '{materia}' para {estudiante}."

    horarios.clear()
    horarios.extend(nuevos_horarios)
    guardar_datos(horarios)
    return True, f"Materia '{materia}' de {estudiante} eliminada correctamente."


def generar_reporte(horarios, estudiante=None):
    "arma el reporte ordenado por dia y hora, lo guarda en json y lo devuelve para mostrarlo en consola"

    if estudiante:
        eventos = [e for e in horarios if e.get("estudiante", "").lower() == estudiante.lower()]
    else:
        eventos = horarios

    orden_dias = {dia: i for i, dia in enumerate(dias_validos)}
    eventos_ordenados = sorted(eventos, key=lambda e: (orden_dias.get(e["dia"], 99), horas_a_minutos(e["hora_inicio"])))

    reporte_por_dia = {}
    for evento in eventos_ordenados:
        dia = evento["dia"]
        reporte_por_dia.setdefault(dia, []).append({
            "materia": evento["materia"],
            "hora_inicio": evento["hora_inicio"],
            "hora_fin": evento["hora_fin"],
            "ubicacion": evento["ubicacion"]
        })

    reporte = [{"dia": dia, "eventos": reporte_por_dia[dia]} for dia in dias_validos if dia in reporte_por_dia]

    guardar_reporte(reporte)
    return True, "Reporte generado en 'reporte_horario.json'.", reporte