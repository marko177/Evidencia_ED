import datetime
from os.path import exists
import os
import pandas as pd
from tabulate import tabulate
import sqlite3
from sqlite3 import Error


def clear():
    os.system("cls")


# Se necesita instalar openpyxl para el guardado del reporte en Excel.

if not exists("reservas.db"):
    check = 0
    print("\n**\tBase de datos creada.\t**\n")

else:
    check = 1

try:

    with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS Customers (
                            CustomerID INTEGER,
                            Customer_Name TEXT NOT NULL,
                            PRIMARY KEY(CustomerID)
                        );
                        """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Rooms (
                            RoomID INTEGER,
                            Room_name TEXT NOT NULL,
                            RoomCap INTEGER NOT NULL,
                            PRIMARY KEY(RoomID)
                        );
                        """)
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS Slots (
                            SlotID INTEGER,
                            Slot_name TEXT UNIQUE,
                            PRIMARY KEY(SlotID)
                        );
                        """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS Bookings (
                            BookingID INTEGER,
                            Date timestamp NOT NULL,
                            RoomID INTEGER NOT NULL,
                            SlotID INTEGER NOT NULL,
                            CustomerID INTEGER NOT NULL,
                            Event_name TEXT NOT NULL,
                            FOREIGN KEY(RoomID) REFERENCES Rooms(RoomID),
                            FOREIGN KEY(CustomerID) REFERENCES Customers(CustomerID),
                            FOREIGN KEY(SlotID) REFERENCES Slots(SlotID),
                            PRIMARY KEY(BookingID)
                        );
                        """)

        if check == 0:
            cursor.execute("""
                            INSERT INTO Slots VALUES(1,"Matutino");
                            """)

            cursor.execute("""
                            INSERT INTO Slots VALUES(2,"Vespertino");
                            """)

            cursor.execute("""
                            INSERT INTO Slots VALUES(3, "Nocturno");
                            """)

        else:
            print("\n**\tBase de datos cargada.\t**\n")

except Error as e:
    print(e)
except:
    print("Ocurrió un error")

fecha_hoy = datetime.datetime.today().date()

while True:

    opcion = input("""+----------------------------------------+
|             MENÚ PRINCIPAL             |
|-------+--------------------------------|
|   a)  | Reservaciones                  |
|   b)  | Reportes                       |
|   c)  | Alta de Rooms                  |
|   d)  | Alta de clientes               |
|   e)  | Salir                          |
+-------+--------------------------------+
Opción: """).lower()

    clear()

    if opcion == "a":

        while True:
            opcion_reserva = input("""+-------+--------------------------------------------+
|              MENÚ DE Reservaciones:                |
|-------+--------------------------------------------|
|   a)  | Registrar una nueva reservación            |
|   b)  | Modificar descripción de una reservación   |
|   c)  | Disponibilidad de salas para una fecha     |
|   d)  | Eliminar una reserva                       |
|   e)  | Volver al Menú Principal                   |
+-------+--------------------------------------------+
Opción: """).lower()

            clear()

            if opcion_reserva == "" or opcion_reserva.isspace():
                clear()
                print("No se puede dejar la opción vacía.\n")
                continue

            elif opcion_reserva == "a":

                clear()
                with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) \
                        as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM Rooms;")
                    rooms = cursor.fetchall()
                    if rooms:
                        pass
                    else:
                        clear()
                        print("No hay salas registradas.\n")
                        continue
                    cursor.execute("SELECT * FROM Customers;")
                    customers = cursor.fetchall()

                    if customers:
                        pass
                    else:
                        clear()
                        print("No hay clientes registrados.\n")
                        continue

                while True:
                    try:
                        fecha_reserva = input("Ingrese la fecha a reservar (dd/mm/aaaa):\n")
                        fecha_datetime = datetime.datetime.strptime(fecha_reserva, '%d/%m/%Y')
                        limite_reserva = (fecha_datetime.date() - fecha_hoy).days
                        if limite_reserva >= 2:
                            clear()
                            break
                        else:
                            clear()
                            print("Fecha invalida, ingrese una fecha con dos dias de anticipación.")
                            continue

                    except ValueError:
                        clear()
                        print("Ingrese una fecha valida.\n")
                        continue

                while True:

                    customers_report = [[customer_id, customer_name] for customer_id, customer_name in customers]
                    print(tabulate(customers_report, headers=["Clave", "Nombre"], tablefmt='psql', showindex=False))

                    try:
                        customer_id = int(input("Ingrese su clave de usuario:\n"))

                        break
                    except ValueError:
                        clear()
                        print("Ingrese una clave valida.\n")
                        continue

                with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) \
                        as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM Customers WHERE CustomerID=(?);", [customer_id])
                    customer_check = cursor.fetchall()

                if customer_check:

                    clear()

                    rooms_report = [[room_id, room_name, room_cap] for room_id, room_name, room_cap in rooms]

                    while True:

                        print(tabulate(rooms_report, headers=["Clave", "Sala", "Cupo"],
                                       tablefmt='psql', numalign="left"))

                        try:

                            room_id = int(input("Ingrese la clave de la sala:\n"))
                            clear()
                            break

                        except ValueError:
                            clear()
                            print("Ingrese una clave valida.\n")
                            continue

                    with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                     sqlite3.PARSE_COLNAMES) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Rooms WHERE RoomID=(?)", [room_id])
                        room_check = cursor.fetchall()

                    if room_check:

                        while True:

                            with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                             sqlite3.PARSE_COLNAMES) as conn:
                                cursor = conn.cursor()
                                cursor.execute("SELECT * FROM Slots")
                                slots = cursor.fetchall()
                                slots_report = [[slot_id, slot_name] for slot_id, slot_name in slots]

                            while True:

                                print(tabulate(slots_report, headers=["Clave", "Nombre"], tablefmt='psql',
                                               showindex=False))

                                try:

                                    slot_id = int(input("Ingrese la clave del turno:\n"))
                                    clear()
                                    break

                                except ValueError:
                                    clear()
                                    print("Ingrese una clave valida.\n")
                                    continue

                            try:
                                with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                 sqlite3.PARSE_COLNAMES) as conn:
                                    cursor = conn.cursor()
                                    cursor.execute("SELECT * FROM Slots WHERE SlotID=(?)", [slot_id])
                                    slot_check = cursor.fetchall()
                            except Error as e:
                                print(e)

                            if slot_check:

                                try:
                                    with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                     sqlite3.PARSE_COLNAMES) as conn:
                                        datos = fecha_datetime, room_id, slot_id
                                        cursor = conn.cursor()
                                        cursor.execute("SELECT * FROM Bookings WHERE Date=(?) and RoomID=(?) and "
                                                       "SlotID=(?)", datos)

                                        booking_check = cursor.fetchall()

                                except e:
                                    print(e)

                                if booking_check:

                                    respuesta = input("""Horario ocupado, ¿Desea intentar con otro turno?
+-------+--------+
| Clave | Opción |
|-------+--------|
|   1   |   Si   |
|   2   |   No   |
+-------+--------+
Opción: """)
                                    if respuesta == "1":
                                        clear()
                                        continue

                                    elif respuesta == "2":
                                        clear()
                                        break

                                else:

                                    while True:

                                        event_name = input("Ingrese el nombre del evento:\n")

                                        clear()
                                        if event_name == "" or event_name.isspace():
                                            clear()
                                            print("El nombre no puede quedar vació.\n")
                                            continue

                                        else:

                                            try:

                                                with sqlite3.connect("reservas.db",
                                                                     detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                  sqlite3.PARSE_COLNAMES) as conn:

                                                    cursor = conn.cursor()
                                                    cursor.execute(
                                                        "INSERT INTO Bookings(Date,RoomID,SlotID,CustomerID,Event_name)"
                                                        "VALUES(?, ?, ?, ?, ?)",
                                                        (fecha_datetime, room_id, slot_id, customer_id, event_name))
                                                    cursor.execute("SELECT last_insert_rowid()")
                                                    folio = cursor.fetchone()[0]

                                                    cursor.execute("""
                                                    SELECT Bookings.BookingID, Bookings.Date, Rooms.Room_name, 
                                                    Slots.Slot_name, Customers.Customer_Name, Bookings.Event_name 
                                                    FROM (((Bookings 
                                                    INNER JOIN Rooms on Bookings.RoomID = Rooms.RoomID)
                                                    INNER JOIN Slots on Bookings.SlotID = Slots.SlotID)
                                                    INNER JOIN Customers on Bookings.CustomerID = Customers.CustomerID)
                                                    WHERE BookingID=(?) """, [folio])

                                                    reserva = cursor.fetchone()

                                                    print(tabulate([[reserva[0], reserva[1].strftime('%d/%m/%Y'),
                                                                     reserva[2], reserva[3], reserva[4], reserva[5]]],
                                                                   headers=["Folio", "Fecha", "Sala", "Turno",
                                                                            "Cliente", "Evento"], tablefmt='psql',
                                                                   numalign="left"))

                                            except Error as e:
                                                print(e)

                                            break
                                    break
                            else:
                                clear()
                                print("Turno no registrado")
                    else:
                        clear()
                        print("Sala no registrada.\n")
                else:
                    clear()
                    print("Usuario no registrado.\n")

            elif opcion_reserva == "b":

                clear()
                try:
                    with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) \
                            as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Bookings;")
                        validacion_reservas = cursor.fetchall()
                except Error as e:
                    print(e)

                if validacion_reservas:

                    try:
                        with sqlite3.connect("reservas.db",
                                             detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) \
                                as conn:
                            cursor = conn.cursor()
                            cursor.execute("""
                             SELECT Bookings.BookingID, Bookings.Date, Rooms.Room_name, 
                             Slots.Slot_name, Customers.Customer_Name, Bookings.Event_name 
                             FROM (((Bookings 
                             INNER JOIN Rooms on Bookings.RoomID = Rooms.RoomID)
                             INNER JOIN Slots on Bookings.SlotID = Slots.SlotID)
                             INNER JOIN Customers on Bookings.CustomerID = Customers.CustomerID)""")
                            reporte = cursor.fetchall()
                            lista_reporte = [[booking_id, date.strftime('%d/%m/%Y'), room, slot, user, event_name]
                                             for booking_id, date, room, slot, user, event_name in reporte]

                            print(tabulate(lista_reporte, headers=["Folio", "Fecha", "Sala", "Turno", "Cliente",
                                                                   "Evento"], tablefmt='psql', numalign="left"))
                    except Error as e:
                        print(e)

                    while True:

                        try:
                            folio_mod = int(
                                input("Ingrese el folio de la reserva a modificar:\n"))
                            clear()
                            break
                        except ValueError:
                            clear()
                            print("Ingrese un folio valido.\n")
                            continue

                    try:
                        with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                         sqlite3.PARSE_COLNAMES) as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT * FROM Bookings WHERE BookingID=(?)", [folio_mod])
                            booking_check = cursor.fetchone()
                    except Error as e:
                        print(e)

                    if booking_check:

                        while True:

                            nombre_nuevo = input("Ingrese el nuevo nombre del evento:\n")
                            clear()
                            if nombre_nuevo == "" or nombre_nuevo.isspace():
                                clear()
                                print("Nombre invalido, intente de nuevo.")
                                continue
                            else:
                                break
                        datos = nombre_nuevo, folio_mod

                        try:
                            with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                             sqlite3.PARSE_COLNAMES) \
                                    as conn:
                                cursor = conn.cursor()
                                cursor.execute("UPDATE Bookings SET Event_name=(?) WHERE BookingID=(?);", datos)
                        except Error as e:
                            print(e)
                        print(f"El evento \"{booking_check[5]}\" fue modificado a \"{nombre_nuevo}\" con éxito.\n")

                    else:
                        clear()
                        print("No hay reservas con ese folio.\n")
                else:
                    clear()
                    print("No hay reservas registradas.\n")

            elif opcion_reserva == "c":

                try:
                    with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) \
                            as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Rooms;")
                        validacion_salas = cursor.fetchall()
                except Error as e:
                    print(e)

                if validacion_salas:

                    while True:
                        try:
                            fecha_reporte = input("Ingrese la Date para la disponibilidad (dd/mm/aaaa):\n")
                            fecha_datetime = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y')
                            clear()
                            break
                        except ValueError:
                            clear()
                            print("Ingrese una Date valida en el formato dd/mm/aaaa.\n")
                            continue

                    try:
                        with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                         sqlite3.PARSE_COLNAMES) as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT RoomID, SlotID FROM Bookings WHERE Date=(?)", [fecha_datetime])
                            salas_ocupadas = set(cursor.fetchall())

                            cursor.execute("SELECT RoomID FROM Rooms")
                            salas_creadas = cursor.fetchall()
                            cursor.execute("SELECT SlotID FROM Slots")
                            turnos_creados = cursor.fetchall()
                            salas_posibles = []
                            for sala in salas_creadas:
                                for slot in turnos_creados:
                                    salas_posibles.append((sala[0], slot[0]))
                            salas_posibles = set(salas_posibles)

                            salas_disponibles = salas_posibles - salas_ocupadas

                            reporte_salas = []

                            for id_sala, id_turno in salas_disponibles:

                                try:

                                    with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                     sqlite3.PARSE_COLNAMES) as conn:
                                        cursor = conn.cursor()
                                        cursor.execute("SELECT Room_name FROM Rooms WHERE RoomID = (?)", (id_sala,))
                                        room_name = cursor.fetchall()[0][0]
                                        cursor.execute("SELECT Slot_name FROM Slots WHERE SlotID = (?)",
                                                       (id_turno,))
                                        nombre_turno = cursor.fetchall()[0][0]

                                        reporte_salas.append([id_sala, room_name, nombre_turno])

                                except Error as e:
                                    print(e)

                            print(
                                tabulate(sorted(reporte_salas), tablefmt="psql", headers=["Clave", "Sala", "Turno"]))

                    except Error as e:
                        print(e)

                else:
                    print("No hay Rooms registradas.\n")

            elif opcion_reserva == "d":

                try:
                    with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) \
                            as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Bookings;")
                        validacion_reservas = cursor.fetchall()
                except Error as e:
                    print(e)

                if validacion_reservas:
                    while True:

                        try:
                            with sqlite3.connect("reservas.db",
                                                 detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) \
                                    as conn:
                                cursor = conn.cursor()
                                cursor.execute("""
                                SELECT Bookings.BookingID, Bookings.Date, Rooms.Room_name, 
                                Slots.Slot_name, Customers.Customer_Name, Bookings.Event_name 
                                FROM (((Bookings 
                                INNER JOIN Rooms on Bookings.RoomID = Rooms.RoomID)
                                INNER JOIN Slots on Bookings.SlotID = Slots.SlotID)
                                INNER JOIN Customers on Bookings.CustomerID = Customers.CustomerID)""",)
                                reporte = cursor.fetchall()
                                lista_reporte = [[booking_id, date.strftime('%d/%m/%Y'), room, slot, user, event_name]
                                                 for booking_id, date, room, slot, user, event_name in reporte]

                                print(tabulate(lista_reporte, headers=["Folio", "Fecha", "Sala", "Turno", "Cliente",
                                                                       "Evento"], tablefmt='psql', numalign="left"))

                        except Error as e:
                            print(e)
                        try:
                            folio_id = int(
                                input("Ingrese el BookingID de la reserva (Se necesitan 3 dias de anticipacion "
                                      "para cancelar):\n"))
                            break
                        except ValueError:
                            print("Ingrese un BookingID valido.\n")
                            continue

                    try:
                        with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                         sqlite3.PARSE_COLNAMES) as conn:
                            reporte = []
                            cursor = conn.cursor()
                            cursor.execute("SELECT * FROM Bookings WHERE BookingID = (?)", [folio_id])
                            reserva = cursor.fetchall()
                            for i in reserva:
                                cursor.execute("SELECT Room_name FROM Rooms WHERE RoomID=(?)", [i[2]])
                                room_name = cursor.fetchall()
                                cursor.execute("SELECT Slot_name FROM Slots WHERE SlotID=(?)", [i[3]])
                                nombre_turno = cursor.fetchall()
                                cursor.execute("SELECT Customer_Name FROM Customers WHERE CustomerID=(?)", [i[4]])
                                nombre_cliente = cursor.fetchall()
                                reporte.append(
                                    [i[0], i[1].strftime('%d/%m/%Y'), room_name[0][0], nombre_turno[0][0],
                                     nombre_cliente[0][0], i[5]])

                    except Error as e:
                        print(e)

                    if reserva:
                        # leer variable "fechad" para proceder a restar esa fecha con el dia de la consulta
                        with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                         sqlite3.PARSE_COLNAMES) as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT Date FROM Bookings WHERE BookingID=(?);", [folio_id])
                            reserva = cursor.fetchall()

                            fecha_datetime = reserva[0][0]

                        fecha_limite = (fecha_datetime.date() - fecha_hoy).days

                        if fecha_limite >= 3:
                            print("Una vez eliminada la reserva no se pueden deshacer los cambios.")
                            print(tabulate(reporte, headers=["Folio", "Fecha", "Sala", "Turno", "Cliente",
                                                             "Nombre Evento"], tablefmt='psql', numalign="left"))
                            while True:
                                continuar = input("¿Desea continuar con la eliminación de la reserva? (S/N)\n").upper()
                                clear()
                                if continuar == "S":
                                    with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                                     sqlite3.PARSE_COLNAMES) as conn:
                                        cursor = conn.cursor()
                                        cursor.execute("DELETE FROM Bookings WHERE BookingID=(?);", [folio_id])
                                        print("Reserva eliminada exitosamente.\n")
                                        break
                                elif continuar == "N":
                                    break
                                else:
                                    clear()
                                    print("Opcion no valida, intente de nuevo.\n")
                                    continue
                        else:
                            clear()
                            print("Se necesitan 3 dias de anticipacion para cancelar una reserva.\n")

                    else:
                        clear()
                        print("BookingID no existente.\n")
                else:
                    clear()
                    print("No hay reservas disponibles.\n")

            elif opcion_reserva == "e":
                clear()
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

            clear()
            if opcion_reporte == "a":

                try:
                    with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                     sqlite3.PARSE_COLNAMES) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Bookings;")
                        validacion_reservas = cursor.fetchall()
                except Error as e:
                    print(e)

                if validacion_reservas:

                    while True:
                        try:
                            fecha_reporte = input("Ingrese la Date para el reporte (dd/mm/aaaa):\n")
                            fecha_datetime = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y')
                            clear()
                            break
                        except ValueError:
                            clear()
                            print("Ingrese una Date valida en el formato dd/mm/aaaa.\n")
                            continue

                    try:
                        with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                         sqlite3.PARSE_COLNAMES) as conn:
                            cursor = conn.cursor()
                            cursor.execute("""
                            SELECT Bookings.BookingID, Bookings.Date, Rooms.Room_name, 
                            Slots.Slot_name, Customers.Customer_Name, Bookings.Event_name 
                            FROM (((Bookings 
                            INNER JOIN Rooms on Bookings.RoomID = Rooms.RoomID)
                            INNER JOIN Slots on Bookings.SlotID = Slots.SlotID)
                            INNER JOIN Customers on Bookings.CustomerID = Customers.CustomerID)
                            WHERE Date=(?) """, [fecha_datetime])
                            reporte = cursor.fetchall()
                            lista_reporte = [[booking_id, date.strftime('%d/%m/%Y'), room, slot, user, event_name]
                                             for booking_id, date, room, slot, user, event_name in reporte]
                    except Error as e:
                        print(e)

                    if lista_reporte:
                        print(tabulate(lista_reporte,
                                       headers=["Folio", "Fecha", "Sala", "Turno", "Cliente", "Evento"],
                                       tablefmt='psql',
                                       numalign="left"))
                    else:
                        print(f"No hay reservas el día {fecha_reporte}.\n")

                else:
                    print("No hay reservas registradas.\n")

            elif opcion_reporte == "b":

                try:
                    with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                     sqlite3.PARSE_COLNAMES) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Bookings;")
                        validacion_reservas = cursor.fetchall()
                except Error as e:
                    print(e)

                if validacion_reservas:

                    while True:
                        try:
                            fecha_reporte = input("Ingrese la Date para el reporte (dd/mm/aaaa):\n")
                            fecha_datetime = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y')
                            clear()
                            break
                        except ValueError:
                            clear()
                            print("Ingrese una Date valida en el formato dd/mm/aaaa.\n")
                            continue

                    try:
                        with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                                                         sqlite3.PARSE_COLNAMES) as conn:
                            cursor = conn.cursor()
                            cursor.execute("""
SELECT Bookings.BookingID, Bookings.Date, Rooms.Room_name, 
Slots.Slot_name, Customers.Customer_Name, Bookings.Event_name 
FROM (((Bookings 
INNER JOIN Rooms on Bookings.RoomID = Rooms.RoomID)
INNER JOIN Slots on Bookings.SlotID = Slots.SlotID)
INNER JOIN Customers on Bookings.CustomerID = Customers.CustomerID)
WHERE Date=(?) """, [fecha_datetime])
                            reporte = cursor.fetchall()
                            lista_reporte = [[booking_id, date.strftime('%d/%m/%Y'), room, slot, user, event_name]
                                             for booking_id, date, room, slot, user, event_name in reporte]

                    except Error as e:
                        print(e)

                    if lista_reporte:
                        df = pd.DataFrame(lista_reporte,
                                          columns=["Folio", "Fecha", "Sala", "Horario", "Cliente", "Evento"])
                        df_ = df.set_index("Folio")

                        with pd.ExcelWriter(f"reporte-{fecha_reporte.replace('/', '-')}.xlsx") as writer:
                            df_.to_excel(writer)

                        print(f"Se exporto el reporte como reporte-{fecha_reporte.replace('/', '-')}.xlsx\n")

                    else:
                        print("No hay reservas para esa Date.\n")

                else:
                    print("No hay reservas registradas.\n")

            elif opcion_reporte == "c":
                break

            else:
                clear()
                print("Opción invalida, ingrese una opción del menú.\n")
                continue

    elif opcion == "c":

        while True:

            room_name = input("Ingrese el nombre de la RoomID:\n")

            clear()
            if room_name == "" or room_name.isspace():
                clear()
                print("El nombre no puede quedar vació.\n")
                continue

            else:
                clear()
                break

        while True:

            try:
                room_cap = int(input("Ingrese la capacidad de la sala:\n"))
                clear()
                if room_cap > 0:
                    break
                else:
                    clear()
                    print("La capacidad de la sala debe ser mayor a 0.\n")
                    continue

            except ValueError:
                clear()
                print("Ingrese un numero entero.")

        with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Rooms(Room_name,RoomCap) VALUES(?,?);", (room_name, room_cap))
            cursor.execute("SELECT last_insert_rowid()")
            room_id = cursor.fetchone()[0]

        print(f"\nLa sala \"{room_name}\" fue registrada con clave \"{room_id}\".\n")

    elif opcion == "d":

        while True:

            customer_name = input("Ingrese el nombre del usuario:\n")

            clear()
            if customer_name == "" or customer_name.isspace():
                clear()
                print("El nombre no puede quedar vació.\n")
                continue

            else:

                with sqlite3.connect("reservas.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) \
                        as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO Customers(Customer_Name) VALUES(?);", [customer_name])
                    cursor.execute("SELECT last_insert_rowid()")
                    customer_id = cursor.fetchone()[0]

                print(f"\nEl usuario '{customer_name}' fue registrado con la clave '{customer_id}'.\n")
                break

    elif opcion == "e":
        clear()
        break

    else:
        clear()
        print("Opción no valida.\n")
