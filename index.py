import pyodbc
import sys
import os

def limpiar_consola():
    # Verificar el sistema operativo
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux, macOS
        os.system('clear')

def conectar_sql_server():
    try:
        server = 'ADALBERTO' # Nombre del server de la BDD SQL SERVER
        database = 'Samsung'
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        conexion = pyodbc.connect(connection_string)
        print("Conexión exitosa a SQL Server")
        return conexion
    except Exception as e:
        print(f"Error al conectar a SQL Server: {str(e)}")
        return None

def obtener_estudiantes():
    conexion = conectar_sql_server()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()
        cursor.execute('SELECT EstudianteID, Nombre, Apellido FROM Estudiantes')
        estudiantes = cursor.fetchall()
        return estudiantes
    except Exception as e:
        print(f"Error al obtener estudiantes: {str(e)}")
        return None
    finally:
        conexion.close()

def obtener_cursos():
    conexion = conectar_sql_server()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()
        cursor.execute('SELECT CursoID, Nombre FROM Cursos')
        cursos = cursor.fetchall()
        return cursos
    except Exception as e:
        print(f"Error al obtener cursos: {str(e)}")
        return None
    finally:
        conexion.close()

def agregar_calificacion(id_profesor):
    conexion = conectar_sql_server()
    if not conexion:
        return

    estudiantes = obtener_estudiantes()
    cursos = obtener_cursos()

    if not estudiantes or not cursos:
        print("No se pueden obtener estudiantes o cursos.")
        return

    try:
        cursor = conexion.cursor()

        # Mostrar la lista de estudiantes al profesor
        print("Lista de estudiantes:")
        for estudiante in estudiantes:
            print(f"{estudiante.EstudianteID}. {estudiante.Nombre} {estudiante.Apellido}")

        # Solicitar al profesor que seleccione un estudiante por su ID
        estudiante_id = int(input("Ingrese el ID del estudiante al que desea agregar una calificación: "))

        # Verificar si el estudiante existe
        estudiante_existente = next((estudiante for estudiante in estudiantes if estudiante.EstudianteID == estudiante_id), None)
        if not estudiante_existente:
            print("El ID de estudiante ingresado no existe.")
            return

        # Mostrar la lista de cursos disponibles
        print("Lista de cursos disponibles:")
        for curso in cursos:
            print(f"{curso.CursoID}. {curso.Nombre}")

        # Solicitar al profesor que seleccione un curso por su ID
        curso_id = int(input("Ingrese el ID del curso al que desea agregar una calificación: "))

        # Verificar si el curso existe
        curso_existente = next((curso for curso in cursos if curso.CursoID == curso_id), None)
        if not curso_existente:
            print("El ID de curso ingresado no existe.")
            return

        # Solicitar al profesor que ingrese la calificación
        calificacion = float(input("Ingrese la calificación del estudiante: "))

        cursor.execute('INSERT INTO Calificaciones (EstudianteID, ProfesorID, CursoID, Calificacion) VALUES (?, ?, ?, ?)',
                    (estudiante_id, id_profesor, curso_id, calificacion))
     

        conexion.commit()
        print("Calificación agregada exitosamente.")
    except Exception as e:
        print(f"Error al agregar la calificación: {str(e)}")
    finally:
        conexion.close()

def modificar_calificacion(id_profesor):
    conexion = conectar_sql_server()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()

        # Mostrar la lista de estudiantes al profesor
        print("Lista de estudiantes:")
        estudiantes = obtener_estudiantes()
        for estudiante in estudiantes:
            print(f"{estudiante.EstudianteID}. {estudiante.Nombre} {estudiante.Apellido}")

        # Solicitar al profesor que seleccione un estudiante por su ID
        estudiante_id = int(input("Ingrese el ID del estudiante cuya calificación desea modificar: "))

        # Verificar si el estudiante existe
        estudiante_existente = next((estudiante for estudiante in estudiantes if estudiante.EstudianteID == estudiante_id), None)
        if not estudiante_existente:
            print("El ID de estudiante ingresado no existe.")
            return

        # Mostrar las calificaciones del estudiante seleccionado
        cursor.execute('SELECT CursoID, Calificacion FROM Calificaciones WHERE EstudianteID = ?', (estudiante_id,))
        calificaciones = cursor.fetchall()

        if not calificaciones:
            print("El estudiante seleccionado no tiene calificaciones registradas.")
            return

        print(f"Calificaciones del estudiante {estudiante_existente.Nombre} {estudiante_existente.Apellido}:")
        for calificacion in calificaciones:
            curso_id, nota = calificacion
            print(f"Curso ID: {curso_id}, Calificación: {nota}")

        # Solicitar al profesor que seleccione una calificación por su curso
        curso_id_modificar = int(input("Ingrese el ID del curso cuya calificación desea modificar: "))

        # Verificar si el curso existe para el estudiante seleccionado
        curso_existente = next((calificacion for calificacion in calificaciones if calificacion.CursoID == curso_id_modificar), None)
        if not curso_existente:
            print("El curso ingresado no tiene calificación registrada para el estudiante seleccionado.")
            return

        # Solicitar al profesor que ingrese la nueva calificación
        nueva_calificacion = float(input("Ingrese la nueva calificación para el estudiante: "))

        # Actualizar la calificación en la base de datos
        cursor.execute('UPDATE Calificaciones SET Calificacion = ? WHERE EstudianteID = ? AND CursoID = ?',
                       (nueva_calificacion, estudiante_id, curso_id_modificar))

        conexion.commit()
        print("Calificación modificada exitosamente.")
    except Exception as e:
        print(f"Error al modificar la calificación: {str(e)}")
    finally:
        conexion.close()

def mostrar_promedio_materia():
    conexion = conectar_sql_server()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()

        cursos = obtener_cursos()
        if not cursos:
            print("No se pueden obtener cursos.")
            return

        # Mostrar la lista de cursos disponibles
        print("Lista de cursos disponibles:")
        for curso in cursos:
            print(f"{curso.CursoID}. {curso.Nombre}")

        # Solicitar al profesor que seleccione un curso por su ID
        curso_id = int(input("Ingrese el ID del curso para calcular el promedio de notas: "))

        # Verificar si el curso existe
        curso_existente = next((curso for curso in cursos if curso.CursoID == curso_id), None)
        if not curso_existente:
            print("El ID de curso ingresado no existe.")
            return

        # Obtener las calificaciones de todos los estudiantes para el curso seleccionado
        cursor.execute('SELECT Calificacion FROM Calificaciones WHERE CursoID = ?', (curso_id,))
        calificaciones = cursor.fetchall()

        if not calificaciones:
            print("No hay calificaciones registradas para el curso seleccionado.")
            return

        # Calcular el promedio de notas para el curso seleccionado
        total_calificaciones = len(calificaciones)
        suma_calificaciones = sum(calificacion.Calificacion for calificacion in calificaciones)
        promedio_calificaciones = suma_calificaciones / total_calificaciones

        print(f"Promedio de notas para el curso {curso_existente.Nombre}: {promedio_calificaciones:.2f}")
    except Exception as e:
        print(f"Error al calcular el promedio de notas: {str(e)}")
    finally:
        conexion.close()

def mostrar_promedio_global():
    conexion = conectar_sql_server()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()

        # Obtener todas las calificaciones
        cursor.execute('SELECT Calificacion FROM Calificaciones')
        calificaciones = cursor.fetchall()

        if not calificaciones:
            print("No hay calificaciones registradas.")
            return

        # Calcular el promedio global de notas para todas las calificaciones
        total_calificaciones = len(calificaciones)
        suma_calificaciones = sum(calificacion.Calificacion for calificacion in calificaciones)
        promedio_global_calificaciones = suma_calificaciones / total_calificaciones

        print(f"Promedio global de todas las calificaciones: {promedio_global_calificaciones:.2f}")
    except Exception as e:
        print(f"Error al calcular el promedio global de notas: {str(e)}")
    finally:
        conexion.close()

def menu_profesor(id_profesor):
    while True:
        print("\n--- Menú del Profesor ---")
        print("1. Agregar una calificación")
        print("2. Modificar una calificación")
        print("3. Mostrar el promedio de notas de todos los estudiantes en una materia")
        print("4. Mostrar el promedio global de una materia")
        print("0. Salir")
        
        opcion = input("Ingrese el número de la opción que desea realizar: ")

        if opcion == '1':
            limpiar_consola()
            agregar_calificacion(id_profesor)
        elif opcion == '2':
            limpiar_consola()
            modificar_calificacion(id_profesor)
        elif opcion == '3':
            limpiar_consola()
            mostrar_promedio_materia()
        elif opcion == '4':
            limpiar_consola()
            mostrar_promedio_global()
        elif opcion == '0':
            print("Saliendo del sistema.")
            sys.exit()
        else:
            print("Opción inválida. Intente nuevamente.")

def menu_estudiante(id_estudiante):
    while True:
        print("\n--- Menú del Estudiante ---")
        print("1. Ver calificaciones")
        print("2. Ver promedio")
        print("0. Salir")
        
        opcion = input("Ingrese el número de la opción que desea realizar: ")

        if opcion == '1':
            limpiar_consola()
            ver_calificaciones(id_estudiante)
        elif opcion == '2':
            limpiar_consola()
            ver_promedio(id_estudiante)
        elif opcion == '0':
            print("Saliendo del sistema.")
            sys.exit()
        else:
            print("Opción inválida. Intente nuevamente.")

def ver_calificaciones(id_estudiante):
    conexion = conectar_sql_server()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()

        # Obtener las calificaciones del estudiante con el ID proporcionado
        cursor.execute('SELECT CursoID, Calificacion FROM Calificaciones WHERE EstudianteID = ?', (id_estudiante,))
        calificaciones_estudiante = cursor.fetchall()

        if not calificaciones_estudiante:
            print("No hay calificaciones registradas para el estudiante.")
            return

        # Mostrar las calificaciones del estudiante por curso
        print("Calificaciones del estudiante:")
        for calificacion in calificaciones_estudiante:
            curso_id = calificacion.CursoID
            calificacion_estudiante = calificacion.Calificacion

            # Obtener el nombre del curso asociado al CursoID
            cursor.execute('SELECT Nombre FROM Cursos WHERE CursoID = ?', (curso_id,))
            curso_nombre = cursor.fetchone().Nombre

            print(f"Curso: {curso_nombre}, Calificación: {calificacion_estudiante:.2f}")

        # Calcular el promedio individual del estudiante
        total_calificaciones = len(calificaciones_estudiante)
        suma_calificaciones = sum(calificacion.Calificacion for calificacion in calificaciones_estudiante)
        promedio_individual_estudiante = suma_calificaciones / total_calificaciones

        print(f"Promedio individual del estudiante: {promedio_individual_estudiante:.2f}")
    except Exception as e:
        print(f"Error al obtener las calificaciones del estudiante: {str(e)}")
    finally:
        conexion.close()

def ver_promedio(id_estudiante):

    conexion = conectar_sql_server()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()

        # Obtener las calificaciones del estudiante con el ID proporcionado
        cursor.execute('SELECT Calificacion FROM Calificaciones WHERE EstudianteID = ?', (id_estudiante,))
        calificaciones_estudiante = cursor.fetchall()

        if not calificaciones_estudiante:
            print("No hay calificaciones registradas para el estudiante.")
            return

        # Calcular el promedio del estudiante
        total_calificaciones = len(calificaciones_estudiante)
        suma_calificaciones = sum(calificacion.Calificacion for calificacion in calificaciones_estudiante)
        promedio_estudiante = suma_calificaciones / total_calificaciones

        print(f"Promedio del estudiante: {promedio_estudiante:.2f}")
    except Exception as e:
        print(f"Error al obtener el promedio del estudiante: {str(e)}")
    finally:
        conexion.close()

def login():
    print("Bienvenido al sistema de gestión de calificaciones.")

    while True:
        opcion_registro = input("Ingrese '1' para Ingresar o '2' para Registrarse: ")

        if opcion_registro == '1':
            # Ingresar
            while True:
                tipo_usuario = input("Ingrese 'e' si es estudiante, 'p' si es profesor: ").lower()
                if tipo_usuario in ['e', 'p']:
                    limpiar_consola()
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")

            conexion = conectar_sql_server()
            if not conexion:
                sys.exit()

            cursor = conexion.cursor()
            cursor.execute('SELECT Usuario, Contraseña, EstudianteID FROM Estudiantes')
            estudiantes = {row.Usuario: {'contraseña': row.Contraseña, 'id': row.EstudianteID} for row in cursor.fetchall()}

            cursor.execute('SELECT Usuario, Contraseña, ProfesorID FROM Profesores')
            profesores = {row.Usuario: {'contraseña': row.Contraseña, 'id': row.ProfesorID} for row in cursor.fetchall()}

            usuarios = estudiantes if tipo_usuario == 'e' else profesores

            for _ in range(3):
                limpiar_consola()
                usuario = input("Nombre de usuario: ")
                contraseña = input("Contraseña: ")

                if usuario in usuarios and usuarios[usuario]['contraseña'] == contraseña:
                    if tipo_usuario == 'e':
                        limpiar_consola()
                        print("Bienvenido, estudiante!")
                        menu_estudiante(usuarios[usuario]['id'])
                    elif tipo_usuario == 'p':
                        limpiar_consola()
                        print("Bienvenido, profesor!")
                        menu_profesor(usuarios[usuario]['id'])
                    sys.exit()
                else:
                    print(f"Credenciales incorrectas. Intentos restantes: {2 - _}")

            print("Has alcanzado el límite de intentos. El programa se cerrará.")
            conexion.close()

        elif opcion_registro == '2':
            # Registrarse
            while True:
                tipo_usuario = input("Ingrese 'e' si desea registrarse como estudiante, 'p' si desea registrarse como profesor: ").lower()
                if tipo_usuario in ['e', 'p']:
                    limpiar_consola()
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")

            conexion = conectar_sql_server()
            if not conexion:
                sys.exit()

            cursor = conexion.cursor()

            usuario = input("Ingrese un nombre de usuario: ")
            contraseña = input("Ingrese una contraseña: ")

            if tipo_usuario == 'e':
                # Registro de estudiante
                nombre = input("Ingrese su nombre: ")
                apellido = input("Ingrese su apellido: ")
                estudiante_id = int(input("Ingrese su ID de estudiante: "))

                try:
                    cursor.execute('INSERT INTO Estudiantes (EstudianteID, Nombre, Apellido, Usuario, Contraseña) VALUES (?, ?, ?, ?, ?)',
                                   (estudiante_id, nombre, apellido, usuario, contraseña))
                    conexion.commit()
                    print("Registro exitoso como estudiante.")
                    login()
                except Exception as e:
                    print(f"Error al registrar estudiante: {str(e)}")
                    login()
                finally:
                    conexion.close()

            elif tipo_usuario == 'p':
                # Registro de profesor
                nombre = input("Ingrese su nombre: ")
                apellido = input("Ingrese su apellido: ")
                profesor_id = int(input("Ingrese su ID de profesor: "))

                try:
                    cursor.execute('INSERT INTO Profesores (ProfesorID, Nombre, Apellido, Usuario, Contraseña) VALUES (?, ?, ?, ?, ?)',
                                   (profesor_id, nombre, apellido, usuario, contraseña))
                    conexion.commit()
                    print("Registro exitoso como profesor.")
                    login()
                except Exception as e:
                    print(f"Error al registrar profesor: {str(e)}")
                    login()
                finally:
                    conexion.close()

            sys.exit()

        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == '__main__':
    login()
