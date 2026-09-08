
# Archivo principal del programa

from almacenamiento import cargar_datos
from interfaz import ver_horario_semanal, mostrar_reporte_paginado
from operaciones import registrar_materia, modificar_materia, eliminar_materia, generar_reporte


def menu():
    horarios = cargar_datos()

    while True:
        print("\n" + "=" * 42)
        print("GENERADOR DE HORARIOS PARA ESTUDIANTES")
        print("=" * 42)
        print("1. Registrar una materia o actividad")
        print("2. Ver horario semanal")
        print("3. Modificar una materia o actividad")
        print("4. Eliminar una materia o actividad")
        print("5. Generar reporte del horario")
        print("6. Salir")
        print("=" * 42)

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            print("\n--- Registrar Materia ---")
            estudiante = input("Nombre del estudiante: ").strip()
            materia = input("Ingrese el nombre de la materia o actividad: ").strip()
            dia = input("Ingrese el dia de la semana (Lunes, Martes, ...): ").strip()
            hora_inicio = input("Ingrese la hora de inicio (Formato 24H - Ejemplo: 14:00): ").strip()
            hora_fin = input("Ingrese la hora de fin (Formato 24H - Ejemplo: 16:00): ").strip()
            ubicacion = input("Ingrese la ubicacion (opcional, presione ENTER para omitir): ").strip()

            exito, msj = registrar_materia(horarios, estudiante, materia, dia, hora_inicio, hora_fin, ubicacion)
            print("\n" + msj)

        elif opcion == "2":
            estudiante = input("Nombre del estudiante: ").strip()
            ver_horario_semanal(horarios, estudiante)

        elif opcion == "3":
            print("\n--- Modificar Materia ---")
            estudiante = input("Nombre del estudiante: ").strip()
            materia_actual = input("Ingrese el nombre de la materia o actividad a modificar: ").strip()
            nueva_materia = input("Ingrese el nuevo nombre de la materia (ENTER para mantener): ").strip()
            nuevo_dia = input("Ingrese el nuevo dia de la semana: ").strip()
            nueva_hora_inicio = input("Ingrese la nueva hora de inicio: ").strip()
            nueva_hora_fin = input("Ingrese la nueva hora de fin: ").strip()
            nueva_ubicacion = input("Ingrese la nueva ubicacion (ENTER para mantener la misma): ").strip()

            if not nueva_materia:
                nueva_materia = materia_actual

            exito, msj = modificar_materia(
                horarios, estudiante, materia_actual, nueva_materia,
                nuevo_dia, nueva_hora_inicio, nueva_hora_fin, nueva_ubicacion
            )
            print("\n" + msj)

        elif opcion == "4":
            print("\n--- Eliminar Materia ---")
            estudiante = input("Nombre del estudiante: ").strip()
            materia = input("Ingrese el nombre de la materia o actividad que desea eliminar: ").strip()

            exito, msj = eliminar_materia(horarios, estudiante, materia)
            print("\n" + msj)

        elif opcion == "5":
            estudiante = input("Nombre del estudiante (ENTER para reporte de todos): ").strip()
            estudiante = estudiante if estudiante else None

            exito, msj, reporte = generar_reporte(horarios, estudiante)
            mostrar_reporte_paginado(reporte)

        elif opcion == "6":
            print("\nChao, saliendo del programa...")
            break

        else:
            print("\nOpcion invalida, intenta de nuevo.")


if __name__ == "__main__":
    menu()