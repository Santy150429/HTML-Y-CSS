
#Ejercicio 1: Filtrar materias por un rango de horas (Examen clásico de lógica y condiciones)

def materias_en_rango(horarios, hora_inicio_filtro, hora_fin_filtro):
    # Convertimos el filtro a minutos usando tu función horas_a_minutos
    inicio_f = horas_a_minutos(hora_inicio_filtro)
    fin_f = horas_a_minutos(hora_fin_filtro)
    
    materias_encontradas = []
    for evento in horarios:
        inicio_ev = horas_a_minutos(evento["hora_inicio"])
        fin_ev = horas_a_minutos(evento["hora_fin"])
        
        # Si la materia está completamente dentro del rango pedido
        if inicio_ev >= inicio_f and fin_ev <= fin_f:
            materias_encontradas.append(evento)
            
    return materias_encontradas

#Ejercicio 2: Contar cuántas materias tiene cada estudiante (Uso de diccionarios acumuladores)

def contar_materias_por_estudiante(horarios):
    resumen = {}
    
    for evento in horarios:
        estudiante = evento.get("estudiante", "Desconocido")
        
        # Si el estudiante ya está en el diccionario, sumamos 1; si no, empezamos en 1
        if estudiante in resumen:
            resumen[estudiante] += 1
        else:
            resumen[estudiante] = 1
            
    return resumen
# Ejemplo de uso: {"Carlos": 3, "Ana": 5}

#Ejercicio 3: Validación extra - Límite de materias por día
def validar_limite_diario(horarios, estudiante, dia_nuevo):
    contador = 0
    for evento in horarios:
        if (evento.get("estudiante", "").lower() == estudiante.lower() and 
            evento.get("dia", "").lower() == dia_nuevo.lower()):
            contador += 1
            
    # Si ya tiene 3 o más
    if contador >= 3:
        return True, f"Límite alcanzado: {estudiante} ya tiene 3 materias el {dia_nuevo}."
    return False, ""

#Ejercicio 4: Búsqueda flexible por texto parcial (Usando in)
def buscar_materia_parcial(horarios, texto_busqueda):
    texto_busqueda = texto_busqueda.lower().strip()
    resultados = []
    
    for evento in horarios:
        nombre_materia = evento.get("materia", "").lower()
        # Si el texto buscado está contenido dentro del nombre de la materia
        if texto_busqueda in nombre_materia:
            resultados.append(evento)
            
    return resultados

#Ejercicio 5: Exportar datos a un archivo de texto plano (.txt)
def exportar_a_txt(horarios, estudiante_objetivo):
    nombre_archivo = f"horario_{estudiante_objetivo}.txt"
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"=== HORARIO DE {estudiante_objetivo.upper()} ===\n\n")
        
        encontrados = False
        for evento in horarios:
            if evento.get("estudiante", "").lower() == estudiante_objetivo.lower():
                f.write(f"Materia: {evento['materia']}\n")
                f.write(f"Día: {evento['dia']} | Hora: {evento['hora_inicio']} - {evento['hora_fin']}\n")
                f.write(f"Ubicación: {evento['ubicacion']}\n")
                f.write("-" * 30 + "\n")
                encontrados = True
                
    if encontrados:
        print(f"¡Exportado correctamente a {nombre_archivo}!")
    else:
        print("No se encontraron datos para ese estudiante.")

#Opción 1: Filtro de horarios por Jornada (Mañana / Tarde)
def filtrar_por_jornada(horarios, estudiante, jornada):
    "Filtra las materias según la jornada: 'manana' o 'tarde'"
    resultados = []
    
    # 12:00 PM en minutos son 720 minutos (12 horas * 60 minutos)
    MEDIODIA_MINUTOS = 720 
    
    for evento in horarios:
        # Validamos que sea el estudiante correcto
        if evento.get("estudiante", "").lower() == estudiante.lower():
            # Usamos tu función para convertir la hora de inicio a minutos
            inicio_min = horas_a_minutos(evento["hora_inicio"])
            
            if inicio_min != -1:
                if jornada.lower() == "manana" and inicio_min < MEDIODIA_MINUTOS:
                    resultados.append(evento)
                elif jornada.lower() == "tarde" and inicio_min >= MEDIODIA_MINUTOS:
                    resultados.append(evento)
                    
    return resultados

# Ejemplo de uso:
# clases_manana = filtrar_por_jornada(horarios, "Carlos", "manana")

#Opción 2: Buscador de "Huecos Libres" (Las horas más probables o disponibles)
def buscar_espacios_libres(horarios, estudiante, dia):
    "Calcula y devuelve una lista con las franjas horarias libres de un estudiante en un día"
    
    # Jornada académica estándar: de 8:00 (480 min) a 18:00 (1080 min)
    INICIO_JORNADA = 8 * 60  
    FIN_JORNADA = 18 * 60    
    
    # 1. Recolectamos todas las horas ocupadas de ese estudiante en ese día específico
    ocupados = []
    for evento in horarios:
        if (evento.get("estudiante", "").lower() == estudiante.lower() and 
            evento.get("dia", "").lower() == dia.lower()):
            
            ini = horas_a_minutos(evento["hora_inicio"])
            fin = horas_a_minutos(evento["hora_fin"])
            if ini != -1 and fin != -1:
                ocupados.append((ini, fin))
                
    # 2. Si no tiene materias registradas, todo el día está libre
    if not ocupados:
        return [("08:00", "18:00")]
        
    # 3. Ordenamos los eventos ocupados cronológicamente por su hora de inicio
    ocupados.sort(key=lambda x: x[0])
    
    # 4. Buscamos los espacios vacíos entre las clases
    libres = []
    tiempo_actual = INICIO_JORNADA
    
    for ini, fin in ocupados:
        if tiempo_actual < ini:
            # Hay un espacio libre antes de esta clase
            h_ini = f"{tiempo_actual // 60:02d}:{tiempo_actual % 60:02d}"
            h_fin = f"{ini // 60:02d}:{ini % 60:02d}"
            libres.append((h_ini, h_fin))
        tiempo_actual = max(tiempo_actual, fin)
        
    # Si queda tiempo libre al final del día (después de la última clase)
    if tiempo_actual < FIN_JORNADA:
        h_ini = f"{tiempo_actual // 60:02d}:{tiempo_actual % 60:02d}"
        h_fin = f"{FIN_JORNADA // 60:02d}:{FIN_JORNADA % 60:02d}"
        libres.append((h_ini, h_fin))
        
    return libres

# Ejemplo de uso:
# huecos = buscar_espacios_libres(horarios, "Ana", "Lunes")
# Devuelve bloques libres como [('08:00', '10:00'), ('12:00', '14:00')]

#Ejercicio 6: Filtrar materias por un día específico de la semana+
def filtrar_por_dia(horarios, estudiante, dia_buscado):
    "Devuelve una lista con las materias de un estudiante en un día específico"
    materias_del_dia = []
    
    for evento in horarios:
        # Validamos estudiante y día (usando .lower() para evitar errores por mayúsculas)
        if (evento.get("estudiante", "").lower() == estudiante.lower() and 
            evento.get("dia", "").lower() == dia_buscado.lower()):
            materias_del_dia.append(evento)
            
    return materias_del_dia

# Ejemplo de uso:
# clases_lunes = filtrar_por_dia(horarios, "Carlos", "Lunes")

#Ejercicio 7: Encontrar la primera clase del día (Madrugador)
def obtener_primera_clase(horarios, estudiante, dia):
    "Devuelve el evento de la clase que comienza más temprano en el día"
    materias_dia = filtrar_por_dia(horarios, estudiante, dia)
    
    if not materias_dia:
        return None  # No hay clases ese día
    
    # Buscamos la menor hora usando tu función horas_a_minutos como llave de ordenamiento
    primera_clase = min(materias_dia, key=lambda e: horas_a_minutos(e["hora_inicio"]))
    
    return primera_clase

# Ejemplo de uso:
# primera = obtener_primera_clase(horarios, "Ana", "Martes")
# print(f"La primera clase es {primera['materia']} a las {primera['hora_inicio']}")

#Ejercicio 8: Conteo y estadísticas de materias por día de la semana
def conteo_clases_por_dia(horarios):
    "Devuelve un resumen de cuántas materias hay en total por cada día"
    resumen_dias = {
        "Lunes": 0,
        "Martes": 0,
        "Miercoles": 0,
        "Jueves": 0,
        "Viernes": 0
    }
    
    for evento in horarios:
        dia = evento.get("dia", "").capitalize()
        if dia in resumen_dias:
            resumen_dias[dia] += 1
            
    return resumen_dias

# Ejemplo de uso:
# estadisticas = conteo_clases_por_dia(horarios)
# print(estadisticas) -> {'Lunes': 4, 'Martes': 2, ...}

#===================================================#
#💡 Último consejo para el examen:
#Recuerda que en Python, cuando manipulas diccionarios dentro de listas (como tu JSON), las operaciones más seguras usan el método .get("clave", valor_por_defecto) en lugar de corchetes directos ["clave"]. Si en el examen te ponen un JSON mal formado o a un registro le falta un dato, usar .get() evitará que tu programa explote con un error de tipo KeyError.

#¡Mucho éxito, ve con seguridad que tienes buenas bases! ¿Te queda alguna última duda antes de que te prepares?
#======================================================#