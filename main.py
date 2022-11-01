import datetime
from os.path import exists
import pandas as pd
from tabulate import tabulate
import sqlite3
from sqlite3 import Error

# Se necesita instalar openpyxl para el guardado del reporte en Excel.

conexion = sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
check = 0
try:

    if exists("reservas.db"):
        check = 1

    with conexion as conn:
        cursor = conn.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id_user INTEGER,
                            name_user TEXT NOT NULL,
                            PRIMARY KEY(id_user)
                        );
                        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS salas (
                            id_sala INTEGER,
                            nombre_sala TEXT NOT NULL,
                            capacidad_sala INTEGER NOT NULL,
                            PRIMARY KEY(id_sala)
                        );
                        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS reservaciones (
                            folio INTEGER,
                            fecha timestamp NOT NULL,
                            sala INTEGER NOT NULL,
                            turno INTEGER NOT NULL,
                            cliente INTEGER NOT NULL,
                            nombre_evento TEXT NOT NULL,
                            FOREIGN KEY(sala) REFERENCES salas(id_sala),
                            FOREIGN KEY(cliente) REFERENCES users(id_user),
                            PRIMARY KEY(folio)
                        );
                        """)
        if check == 1:
            print("Se cargo la base de datos con exito.\n")
        else:
            print("Se creo la base de datos con exito.\n")

except Error as e:
    print(e)
except:
    print("Ocurrió un error")

turnos = {1: "Matutino", 2: "Vespertino", 3: "Nocturno"}
fecha_hoy = datetime.datetime.today().date()

while True:

    opcion = input("""+----------------------------------------+
|             MENÚ PRINCIPAL             |
|-------+--------------------------------|
|   a)  | Reservaciones                  |
|   b)  | Reportes                       |
|   c)  | Alta de salas                  |
|   d)  | Alta de clientes               |
|   e)  | Salir                          |
+-------+--------------------------------+
Opción: """).lower()

    if opcion == "a":

        while True:
            opcion_reserva = input("""+-------+--------------------------------------------+
|              MENÚ DE RESERVACIONES:                |
|-------+--------------------------------------------|
|   a)  | Registrar una nueva reservación            |
|   b)  | Modificar descripción de una reservación   |
|   c)  | Disponibilidad de salas para una fecha     |
|   d)  | Eliminar una reserva                       |
|   e)  | Volver al Menú Principal                   |
+-------+--------------------------------------------+
Opción: """).lower()

            if opcion_reserva == "":
                print("No se puede dejar la opción vacía.\n")
                continue

            elif opcion_reserva == "a":

                with conexion as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM salas;")
                    salas = cursor.fetchall()
                    if salas:
                        pass
                    else:
                        print("No hay salas registradas.\n")
                        continue
                    cursor.execute("SELECT * FROM users;")

                    usuarios = cursor.fetchall()
                    if usuarios:
                        pass
                    else:
                        print("No hay clientes registrados.\n")
                        continue

                    usuarios_reporte = list()

                    for usuario in usuarios:
                        usuarios_reporte.append([usuario[0], usuario[1]])

                    print(tabulate(usuarios_reporte, headers=["Clave", "Nombre"], tablefmt='psql', showindex=False))

                while True:

                    try:

                        user_id = int(input("Ingrese su clave de usuario:\n"))
                        break

                    except ValueError:

                        continue

                with conexion as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE id_user=(?);", [user_id])
                    comprobacion_id = cursor.fetchall()

                if comprobacion_id:

                    while True:

                        try:
                            fecha_reserva = input("Ingrese la fecha a reservar (dd/mm/aaaa):\n")
                            fecha_datetime = datetime.datetime.strptime(fecha_reserva, '%d/%m/%Y')
                            break

                        except ValueError:

                            print("Ingrese una fecha valida.\n")
                            continue

                    limite_reserva = (fecha_datetime.date() - fecha_hoy).days

                    if limite_reserva >= 2:

                        with conexion as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT * FROM salas")
                            salas_cursor = cursor.fetchall()
                            salas = []
                            for i in salas_cursor:
                                salas.append([i[0], i[1], i[2]])
                        print(tabulate(salas, headers=["Clave", "Sala", "Cupo"], tablefmt='psql', numalign="left"))

                        while True:

                            try:

                                sala_id = int(input("Ingrese la clave de la sala:\n"))
                                break

                            except ValueError:
                                continue

                        with conexion as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT * FROM salas WHERE id_sala=(?)", [sala_id])
                            consulta_sala = cursor.fetchall()

                        if consulta_sala:

                            while True:

                                turno = input("""+------------------------------------+
| Ingrese el horario del evento:     |
|-------+----------------------------|
|   a)  | Matutino                   |
|   b)  | Vespertino                 |
|   c)  | Nocturno                   |
+-------+----------------------------+
Opción: """).lower()
                                if turno == "a":
                                    turno = 1
                                    break
                                elif turno == "b":
                                    turno = 2
                                    break
                                elif turno == "c":
                                    turno = 3
                                    break
                                else:
                                    print("Opción no valida.")
                                    continue

                            try:
                                with conexion as conn:
                                    datos = fecha_datetime, sala_id, turno
                                    cursor = conn.cursor()
                                    cursor.execute("SELECT * FROM reservaciones WHERE fecha=(?) and sala=(?) and "
                                                   "turno=(?)", datos)

                                    consulta = cursor.fetchall()

                            except e:
                                print(e)

                            if consulta:
                                print("Horario Ocupado.\n")
                                break

                            else:

                                while True:

                                    nombre_evento = input("Ingrese el nombre del evento:\n")

                                    if nombre_evento == "":

                                        print("El nombre no puede quedar vació.\n")
                                        continue

                                    else:

                                        try:

                                            with conexion as conn:

                                                cursor = conn.cursor()
                                                cursor.execute(
                                                    "INSERT INTO reservaciones(fecha,sala,turno,cliente,nombre_evento) "
                                                    "VALUES(?, ?, ?, ?, ?)",
                                                    (fecha_datetime, sala_id, turno, user_id, nombre_evento))

                                                cursor.execute("SELECT nombre_sala FROM salas WHERE id_sala=(?)",
                                                               [sala_id])
                                                nombre_sala = cursor.fetchall()

                                                cursor.execute("SELECT name_user FROM users WHERE id_user=(?)",
                                                               [user_id])
                                                nombre_usuario = cursor.fetchall()

                                                cursor.execute("SELECT folio FROM reservaciones WHERE (fecha, sala, "
                                                               "turno) = (?, ?, ?)", (fecha_datetime, sala_id, turno,))
                                                folio = cursor.fetchall()[0][0]

                                                print(tabulate([[folio, fecha_reserva, nombre_sala[0][0], turnos[turno],
                                                                 nombre_usuario[0][0], nombre_evento]],
                                                               headers=["Folio", "Fecha", "Sala", "Turno", "Cliente",
                                                                        "Evento"],
                                                               tablefmt='psql', numalign="left"))

                                        except Error as e:
                                            print(e)

                                        break
                        else:
                            print("Sala no registrada.\n")
                    else:
                        print("Se necesitan dos días de anticipación para reservar un evento.\n")
                else:
                    print("Usuario no registrado.\n")

            elif opcion_reserva == "b":

                try:
                    with conexion as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM reservaciones;")
                        validacion_reservas = cursor.fetchall()
                except e:
                    print(e)

                if validacion_reservas:
                    while True:

                        try:
                            folio_mod = int(input("Ingrese el folio de la reserva:\n"))
                            break
                        except ValueError:
                            continue

                    try:
                        with conexion as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT * FROM reservaciones WHERE folio=(?)", [folio_mod])
                            consulta_reserva = cursor.fetchall()
                    except e:
                        print(e)

                    if consulta_reserva:

                        nombre_nuevo = input("Ingrese el nuevo nombre del evento:\n")

                        datos = folio_mod, nombre_nuevo
                        try:
                            with conexion as conn:
                                cursor = conn.cursor()
                                cursor.execute("SELECT nombre_evento FROM reservaciones WHERE folio=(?);", [folio_mod])
                                nombre_antiguo = cursor.fetchall()
                                cursor.execute("UPDATE reservaciones SET nombre_evento=(?) WHERE folio=(?);", datos)

                        except e:
                            print(e)

                        print(f"El evento \"{nombre_antiguo[0][0]}\" fue modificado a \"{nombre_nuevo}\" con éxito.\n")

                    else:
                        print("Folio invalido.\n")
                else:
                    print("No hay reservas registradas.\n")

            elif opcion_reserva == "c":

                while True:
                    try:
                        fecha_reporte = input("Ingrese la fecha para el reporte (dd/mm/aaaa):\n")
                        fecha_datetime = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y')
                        break
                    except ValueError:
                        print("Ingrese una fecha valida en el formato dd/mm/aaaa.\n")
                        continue

                try:
                    with conexion as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT sala, turno FROM reservaciones WHERE fecha=(?)", [fecha_datetime])
                        salas_ocupadas = set(cursor.fetchall())

                        cursor.execute("SELECT id_sala FROM salas")
                        salas_creadas = cursor.fetchall()
                        salas_posibles = []
                        for sala in salas_creadas:
                            for turno in turnos.keys():
                                salas_posibles.append((sala[0], turno))
                        salas_posibles = set(salas_posibles)

                        salas_disponibles = salas_posibles - salas_ocupadas

                        reporte_salas = []

                        for id_sala, turno in salas_disponibles:

                            try:

                                with conexion as conn:
                                    cursor = conn.cursor()
                                    cursor.execute("SELECT nombre_sala FROM salas WHERE id_sala = (?)", (id_sala,) )
                                    nombre_sala = cursor.fetchall()[0][0]

                                    reporte_salas.append([id_sala, nombre_sala, turnos[turno]])

                            except Error as e:
                                print(e)

                        print(tabulate(reporte_salas, tablefmt="psql", headers=["Clave", "Nombre", "Turno"]))

                except Error as e:
                    print(e)

            elif opcion_reserva == "d":

                try:
                    with conexion as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM reservaciones;")
                        validacion_reservas = cursor.fetchall()
                except e:
                    print(e)

                if validacion_reservas:
                    while True:

                        try:
                            folio_id = int(input("Ingrese el folio de la reserva:\n"))
                            break
                        except ValueError:
                            continue

                    try:
                        with conexion as conn:
                            reporte = []
                            cursor = conn.cursor()
                            cursor.execute("SELECT * FROM reservaciones WHERE folio = (?)", [folio_id])
                            reserva = cursor.fetchall()
                            for i in reserva:
                                cursor.execute("SELECT nombre_sala FROM salas WHERE id_sala=(?)", [i[2]])
                                nombre_sala = cursor.fetchall()
                                cursor.execute("SELECT name_user FROM users WHERE id_user=(?)", [i[4]])
                                nombre_cliente = cursor.fetchall()
                                reporte.append(
                                    [i[0], i[1].strftime('%d/%m/%Y'), nombre_sala[0][0], turnos[i[3]],
                                     nombre_cliente[0][0], i[5]])

                    except e:
                        print(e)

                    if reserva:
                        # leer variable "fechad" para proceder a restar esa fecha con el dia de la consulta
                        with conexion as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT fecha FROM reservaciones WHERE folio=(?);", [folio_id])
                            reserva = cursor.fetchall()

                            fecha_datetime = reserva[0][0]

                        fecha_limite = (fecha_datetime.date() - fecha_hoy).days

                        if fecha_limite >= 3:
                            print("Una vez eliminada la reserva no se pueden deshacer los cambios.")
                            print(tabulate(reporte,
                                           headers=["Folio", "Fecha", "Sala", "Turno", "Cliente", "Nombre Evento"],
                                           tablefmt='psql', numalign="left"))
                            while True:
                                continuar = input("¿Desea continuar con la eliminación de la reserva? (S/N)\n").upper()

                                if continuar == "S":
                                    with conexion as conn:
                                        cursor = conn.cursor()
                                        cursor.execute("DELETE FROM reservaciones WHERE folio=(?);", [folio_id])
                                        print("Reserva eliminada exitosamente.\n")
                                        break
                                elif continuar == "N":
                                    break
                                else:
                                    print("Opcion no valida, intente de nuevo.\n")
                                    continue
                        else:
                            print("Se necesitan 3 dias de anticipacion para cancelar una reserva.\n")

                    else:
                        print("Folio no existente.\n")
                else:
                    print("No hay reservas disponibles.\n")

            elif opcion_reserva == "e":
                break

            else:
                print("Opción invalida, ingrese una opción del menú.\n")
                continue

    elif opcion == "b":

        while True:

            opcion_reporte = input("""+------------------------------------+
|          MENÚ REPORTES:            |
|-------+----------------------------|
|   a)  | Reporte en pantalla        |
|   b)  | Exportar reporte a Excel   |
|   c)  | Volver al Menú Principal   |
+-------+----------------------------+
Opción: """).lower()

            if opcion_reporte == "a":

                try:
                    with conexion as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM reservaciones;")
                        validacion_reservas = cursor.fetchall()
                except e:
                    print(e)

                if validacion_reservas:

                    while True:
                        try:
                            fecha_reporte = input("Ingrese la fecha para el reporte (dd/mm/aaaa):\n")
                            fecha_datetime = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y')
                            break
                        except ValueError:
                            print("Ingrese una fecha valida en el formato dd/mm/aaaa.\n")
                            continue

                    try:
                        with conexion as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT * FROM reservaciones WHERE fecha=(?)", [fecha_datetime])
                            reporte = cursor.fetchall()
                            lista_reporte = []

                            for i in reporte:
                                cursor.execute("SELECT nombre_sala FROM salas WHERE id_sala=(?)", [i[2]])
                                nombre_sala = cursor.fetchall()
                                cursor.execute("SELECT name_user FROM users WHERE id_user=(?)", [i[4]])
                                nombre_cliente = cursor.fetchall()
                                lista_reporte.append(
                                    [i[0], i[1].strftime('%d/%m/%Y'), nombre_sala[0][0], turnos[i[3]], nombre_cliente[0][0], i[5]])
                    except e:
                        print(e)

                    if lista_reporte:
                        print(tabulate(lista_reporte, headers=["Folio", "Fecha", "Sala", "Turno", "Cliente", "Evento"],
                                       tablefmt='psql',
                                       numalign="left"))
                    else:
                        print(f"No hay reservas el día {fecha_reporte}.\n")

                else:
                    print("No hay reservas registradas.\n")

            elif opcion_reporte == "b":

                try:
                    with conexion as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM reservaciones;")
                        validacion_reservas = cursor.fetchall()
                except e:
                    print(e)

                if validacion_reservas:

                    while True:
                        try:
                            fecha_reporte = input("Ingrese la fecha para el reporte (dd/mm/aaaa):\n")
                            fecha_datetime = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y')
                            break
                        except ValueError:
                            print("Ingrese una fecha valida en el formato dd/mm/aaaa.\n")
                            continue

                    try:
                        with conexion as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT * FROM reservaciones WHERE fecha=(?)", [fecha_datetime])
                            reporte = cursor.fetchall()
                            lista_reporte = []

                            for i in reporte:
                                cursor.execute("SELECT nombre_sala FROM salas WHERE id_sala=(?)", [i[2]])
                                nombre_sala = cursor.fetchall()
                                cursor.execute("SELECT name_user FROM users WHERE id_user=(?)", [i[4]])
                                nombre_cliente = cursor.fetchall()
                                lista_reporte.append(
                                    [i[0], i[1].strftime('%d/%m/%Y'), nombre_sala[0][0], turnos[i[3]], nombre_cliente[0][0], i[5]])

                    except e:
                        print(e)

                    if lista_reporte:
                        df = pd.DataFrame(lista_reporte,
                                          columns=["Folio", "Fecha", "Sala", "Horario", "Cliente", "Evento"])

                        with pd.ExcelWriter(f"reporte-{fecha_reporte.replace('/', '-')}.xlsx") as writer:
                            df.to_excel(writer)

                        print(f"Se exporto el reporte como reporte-{fecha_reporte.replace('/', '-')}.xlsx\n")

                    else:
                        print("No har reservas para esa fecha.\n")

                else:
                    print("No hay reservas registradas.\n")

            elif opcion_reporte == "c":
                break

            else:
                print("Opción invalida, ingrese una opción del menú.\n")
                continue

    elif opcion == "c":

        while True:

            nombre_sala = input("Ingrese el nombre de la sala:\n")

            if nombre_sala == "":
                print("El nombre no puede quedar vació.\n")
                continue

            else:
                break

        while True:

            try:
                cupo_sala = int(input("Ingrese la capacidad de la sala:\n"))
                if cupo_sala > 0:
                    break
                else:
                    print("La capacidad de la sala debe ser mayor a 0.\n")
                    continue

            except ValueError:
                print("Ingrese un numero entero.")

        with conexion as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO salas(nombre_sala,capacidad_sala) VALUES(?,?);", (nombre_sala, cupo_sala))
            try:
                cursor.execute("SELECT max(id_sala) FROM salas")
                max_id = cursor.fetchall()
                id_sala = max_id[0][0]
            except e:
                id_sala = 1

        print(f"\nLa sala '{nombre_sala}' fue registrada con clave '{id_sala}'.\n")

    elif opcion == "d":

        while True:

            nombre_user = input("Ingrese el nombre del usuario:\n")

            if nombre_user == "":
                print("El nombre no puede quedar vació.\n")
                continue

            else:

                with conexion as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO users(name_user) VALUES(?);", [nombre_user])
                    try:
                        cursor.execute("SELECT max(id_user) FROM users")
                        max_id = cursor.fetchall()
                        id_user = max_id[0][0]
                    except e:
                        id_user = 1

                print(f"\nEl usuario '{nombre_user}' fue registrado con la clave '{id_user}'.\n")
                break

    elif opcion == "e":
        break

    else:
        print("Opción no valida.\n")
