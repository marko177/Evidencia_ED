import csv
import datetime
from tabulate import tabulate

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

                                    print(tabulate([[folio, fecha_reserva, salas[sala_id][0], horario_reserva,
                                                     usuarios[user_id], nombre_evento]],
                                                   headers=["Folio", "Fecha", "Sala", "Turno", "Cliente", "Evento"],
                                                   tablefmt='psql', numalign="left"))
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

            print(f"El evento \"{nombre_previo}\" fue modificado a \"{nombre_nuevo}\" con exito.\n")

        else:
            print("Folio invalido.\n")

    elif opcion == "e":

        while True:
            try:
                fecha_reporte = input("ingrese la fecha de la reserva (dd/mm/aaaa):\n")
                fecha = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y').date()
                break

            except ValueError:
                print("Ingrese una fecha valida en el formato dd/mm/aaaa.\n")
                continue

        reporte = []

        for k, v in reservas.items():
            if fecha_reporte in v:
                reporte.append([k, v[0], salas[v[1]][0], v[2], usuarios[v[3]], v[4]])

        if reporte:
            print(tabulate(reporte, headers=["Folio", "Fecha", "Sala", "Turno", "Cliente", "Evento"],
                           tablefmt='psql', numalign="left"))

        else:
            print(f"No hay reservas el dia {fecha_reporte}.\n")

    elif opcion == "f":
        break

    elif opcion == "g":
        pass

    # ********************************* TESTING BORRAR *********************************

    elif opcion == "t":

        print(usuarios)  # ********************************* TESTING BORRAR *********************************
        print(salas)  # ********************************* TESTING BORRAR *********************************
        print(reservas)  # ********************************* TESTING BORRAR *********************************

    else:

        print("Opción no valida.\n")

print("Programa finalizado.")

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
