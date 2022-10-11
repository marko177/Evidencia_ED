import csv
import datetime
import pandas
from tabulate import tabulate


def imprimir_reporte(fecha_f):
    fecha_formato = fecha_f.strftime("%d/%m/%Y")

    reservas_formato = {
        "FOLIO": [],
        "SALA": [],
        "CLIENTE": [],
        "EVENTO": [],
        "TURNO": []
    }

    contador = 0

    for reserva_en_turno in reservas.items():

        if fecha_formato == reserva_en_turno[1][0]:
            contador += 1
            reservas_formato["FOLIO"].append(reserva_en_turno[0])
            reservas_formato["SALA"].append(salas[reserva_en_turno[1][1]][0])
            reservas_formato["CLIENTE"].append(usuarios[reserva_en_turno[1][3]].capitalize())
            reservas_formato["EVENTO"].append(reserva_en_turno[1][4].capitalize())
            reservas_formato["TURNO"].append(reserva_en_turno[1][2].capitalize())

            pass

    if contador != 0:

        df = pandas.DataFrame(reservas_formato)

        print(f"\nREPORTE DE RESERVACIONES PARA LA FECHA {fecha_formato}")

        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

        print("")

    else:

        print("No hay reservas en esa fecha.\n")


def imprimir_confirmacion(folio_func, fecha_f, sala, user, evento, horario):
    formato_impresion = {
        "FOLIO": [folio_func],
        "FECHA": [fecha_f],
        "SALA": [salas[sala][0].capitalize()],
        "CLIENTE": [usuarios[user].capitalize()],
        "NOMBRE DEL EVENTO": [evento.capitalize()],
        "TURNO": [horario.capitalize()]
    }

    df_impresion = pandas.DataFrame(formato_impresion)

    print("\nReserva exitosa.")

    print(tabulate(df_impresion, headers='keys', tablefmt='psql', showindex=False))

    print("")


try:
    salas = {}

    with open("salas.csv", "r") as file:

        reader = csv.reader(file)

        for row in reader:
            salas[int(row[0])] = [row[1], int(row[2])]

except FileNotFoundError:
    salas = {}

try:
    usuarios = {}

    with open("usuarios.csv", "r") as file:

        reader = csv.reader(file)

        for row in reader:
            usuarios[int(row[0])] = row[1]

except:
    usuarios = {}

try:
    reservas = {}

    with open("reservas.csv", "r") as file:

        reader = csv.reader(file)

        for row in reader:
            reservas[int(row[0])] = [row[1], int(row[2]), row[3], int(row[4]), row[5]]

except FileNotFoundError:
    reservas = {}

# usuarios = {1: "User"}
# salas = {1: ("Sala", 10)}
# reservas = {1: ["12/12/2022", 1, "matutino", 1, "evento"]}

fecha_hoy = datetime.date.today()

while True:

    opcion = input("""+----------------------------------------+
|       Ingrese la opción deseada:       |
|-------+--------------------------------|
|   a)  | Alta de usuario                |
|   b)  | Alta de sala                   |
|   c)  | Reservar una sala              |
|   d)  | Modificar una reserva          |
|   e)  | Reporte de reservas por fecha  |
|   f)  | Salir                          |
+-------+--------------------------------+
""").lower()

    if opcion == "a":

        while True:

            nombre_user = input("Ingrese el nombre del usuario:\n")

            if nombre_user == "":
                print("El nombre no puede quedar vació.\n")
                continue

            else:

                id_user = max(usuarios, default=0) + 1

                usuarios[id_user] = nombre_user

                print(f"\nEl usuario '{nombre_user}' fue registrado con la clave '{id_user}'.\n")
                break

    elif opcion == "b":

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

        id_sala = max(salas, default=0) + 1

        salas[id_sala] = [nombre_sala, cupo_sala]

        print(f"\nLa sala '{nombre_sala}' fue registrada con clave '{id_sala}'.\n")

    elif opcion == "c":

        if usuarios:

            print(tabulate(usuarios.items(), headers=["Clave", "Nombre"], tablefmt='psql', showindex=False))

        else:
            print("No hay clientes registrados.\n")
            continue

        while True:

            try:

                user_id = int(input("Ingrese su clave de usuario:\n"))
                break

            except ValueError:

                continue

        if user_id in usuarios.keys():

            if salas:

                while True:

                    try:

                        fecha_reserva = input("Ingrese la fecha a reservar (dd/mm/aaaa):\n")
                        fecha_datetime = datetime.datetime.strptime(fecha_reserva, '%d/%m/%Y').date()
                        break

                    except ValueError:

                        print("Ingrese una fecha valida.")
                        continue

                limite_reserva = (fecha_datetime - fecha_hoy).days

                if limite_reserva > 2:

                    print(tabulate([[k, ] + v for k, v in salas.items()], headers=["Clave", "Nombre", "Cupo"],
                                   tablefmt='psql', numalign="left"))

                    while True:

                        try:

                            sala_id = int(input("Ingrese la clave de la sala:\n"))
                            break

                        except ValueError:

                            continue

                    if sala_id in salas.keys():

                        while True:

                            horario_reserva = input("""+------------------------------------+
| Ingrese el horario de la sala:     |
|-------+----------------------------|
|   a)  | Matutino                   |
|   b)  | Vespertino                 |
|   c)  | Nocturno                   |
+-------+----------------------------+
""").lower()

                            if horario_reserva == "a":

                                horario_reserva = "matutino"
                                break

                            elif horario_reserva == "b":

                                horario_reserva = "vespertino"
                                break

                            elif horario_reserva == "c":

                                horario_reserva = "nocturno"
                                break

                            else:

                                print("Opción no valida.")
                                continue

                        for reserva in reservas.values():

                            if [fecha_reserva, sala_id, horario_reserva] == reserva[:3]:
                                print("Horario Ocupado")
                                break

                        else:
                            while True:

                                nombre_evento = input("Ingrese el nombre del evento\n")

                                if nombre_evento == "":
                                    print("El nombre no puede quedar vació.\n")
                                    continue

                                else:

                                    folio = max(reservas, default=0) + 1

                                    reservas[folio] = [fecha_reserva, sala_id, horario_reserva, user_id, nombre_evento]

                                    imprimir_confirmacion(folio, fecha_datetime.strftime("%d/%m/%Y"), sala_id,
                                                          user_id, nombre_evento, horario_reserva)
                                    break

                    else:
                        print("Sala no registrada.\n")

                else:
                    print("Se necesitan dos días de anticipación para reservar un evento.\n")
            else:
                print("No hay salas registradas.\n")
                continue
        else:
            print("Usuario no registrado.\n")

    elif opcion == "d":

        while True:

            try:

                folio_mod = int(input("Ingrese el folio de la reserva:\n"))
                break

            except ValueError:

                continue

        if folio_mod in reservas.keys():

            nombre_nuevo = input("Ingrese el nuevo nombre del evento:\n")

            nombre_previo = reservas[folio_mod][4]

            reservas[folio_mod][4] = nombre_nuevo

            print(f"El evento {nombre_previo} fue modificado a {nombre_nuevo} con exito.\n")

        else:

            print("Folio invalido.\n")

    elif opcion == "e":

        while True:

            try:

                fecha_reporte = input("ingrese la fecha de la reserva (dd/mm/aaaa):\n")
                fecha = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y').date()
                break

            except ValueError:
                print("La fecha no es valida")

                continue

        imprimir_reporte(fecha)

    elif opcion == "f":
        break

    # ********************************* TESTING BORRAR *********************************
    elif opcion == "g":
        print("reporte excel")

    # ********************************* TESTING BORRAR *********************************
    elif opcion == "t":

        print(reservas)
        print(reservas.values())

    else:

        print("Opción no valida.\n")

reporte = [[k, ] + v for k, v in reservas.items()]

with open("reservas.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(reporte)

reporte = [[k, ] + v for k, v in salas.items()]

with open("salas.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(reporte)

reporte = [[k, v] for k, v in usuarios.items()]

with open("usuarios.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(reporte)

print(usuarios)  # ********************************* TESTING BORRAR *********************************
print(salas)  # ********************************* TESTING BORRAR *********************************
print(reservas)  # ********************************* TESTING BORRAR *********************************
