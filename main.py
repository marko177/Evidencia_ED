import csv
import datetime
import pandas as pd
from tabulate import tabulate

# Se necesita instalar openpyxl para el guardado del reporte en Excel.

check = 0

try:
    salas = {}

    with open("salas.csv", "r") as file:

        reader = csv.reader(file)

        for row in reader:
            salas[int(row[0])] = [row[1], int(row[2])]

    check += 1

except FileNotFoundError:
    salas = {}

try:
    usuarios = {}

    with open("usuarios.csv", "r") as file:

        reader = csv.reader(file)

        for row in reader:
            usuarios[int(row[0])] = row[1]

    check += 1

except:
    usuarios = {}

try:
    reservas = {}

    with open("reservas.csv", "r") as file:

        reader = csv.reader(file)

        for row in reader:
            reservas[int(row[0])] = [row[1], int(row[2]), int(row[3]), int(row[4]), row[5]]
    check += 1

except FileNotFoundError:
    reservas = {}

if check == 3:
    print("\n**\tSe cargaron los registros de reservas, salas y usuarios correctamente.\t**\n")

else:
    print("\n**\tNo se encontraron registros, se guardaran al finalizar el programa.\t**\n")

turnos = {1: "Matutino", 2: "Vespertino", 3: "Nocturno"}
fecha_hoy = datetime.date.today()

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
|   d)  | Volver al Menú Principal                   |
+-------+--------------------------------------------+
Opción: """).lower()

            if opcion_reserva == "":
                print("No se puede dejar la opción vacía.\n")
                continue

            elif opcion_reserva == "a":
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

                                print("Ingrese una fecha valida.\n")
                                continue

                        limite_reserva = (fecha_datetime - fecha_hoy).days

                        if limite_reserva > 2:

                            print(tabulate([[folio, ] + datos for folio, datos in salas.items()],
                                           headers=["Clave", "Sala", "Cupo"], tablefmt='psql', numalign="left"))

                            while True:

                                try:

                                    sala_id = int(input("Ingrese la clave de la sala:\n"))
                                    break

                                except ValueError:

                                    continue

                            if sala_id in salas.keys():

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

                                for reserva in reservas.values():
                                    if [fecha_reserva, sala_id, turno] == reserva[:3]:
                                        print("Horario Ocupado")
                                        break
                                else:
                                    while True:
                                        nombre_evento = input("Ingrese el nombre del evento:\n")

                                        if nombre_evento == "":
                                            print("El nombre no puede quedar vació.\n")
                                            continue

                                        else:
                                            folio = max(reservas, default=0) + 1

                                            reservas[folio] = [fecha_reserva, sala_id, turno, user_id, nombre_evento]

                                            print(tabulate([[folio, fecha_reserva, salas[sala_id][0], turnos[turno],
                                                             usuarios[user_id], nombre_evento]],
                                                           headers=["Folio", "Fecha", "Sala", "Turno", "Cliente",
                                                                    "Evento"],
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

            elif opcion_reserva == "b":

                if reservas:
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
                        print(f"El evento \"{nombre_previo}\" fue modificado a \"{nombre_nuevo}\" con éxito.\n")

                    else:
                        print("Folio invalido.\n")
                else:
                    print("No hay reservas registradas.\n")

            elif opcion_reserva == "c":

                while True:
                    try:
                        fecha_requerida = input("Ingrese la fecha a revisar (dd/mm/aaaa):\n")
                        requerida_fecha = datetime.datetime.strptime(fecha_requerida, '%d/%m/%Y').date()
                        break
                    except ValueError:
                        print("Ingrese una fecha valida en el formato dd/mm/aaaa.\n")
                        continue

                reservas_actuales = set([(v[1], v[2]) for v in reservas.values() if v[0] == fecha_requerida])
                salas_posibles = set([(sala, turno) for sala in salas.keys() for turno in turnos.keys()])

                salas_disponibles = sorted(list(salas_posibles - reservas_actuales))

                reporte = [[sala, salas[sala][0], turnos[turno]] for sala, turno in salas_disponibles]
                
                if reporte:
                    print(f"Salas disponibles el día {fecha_requerida}:")
                    print(tabulate(reporte, headers=["Clave", "Sala", "Turno"], tablefmt='psql', numalign="left"))
                    print("")
                else:
                    print("No hay salas disponibles")
                    print("")
                    
            elif opcion_reserva == "d":
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

                if reservas:

                    while True:
                        try:
                            fecha_reporte = input("Ingrese la fecha para el reporte (dd/mm/aaaa):\n")
                            fecha = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y').date()
                            break
                        except ValueError:
                            print("Ingrese una fecha valida en el formato dd/mm/aaaa.\n")
                            continue

                    reporte = [[k, v[0], salas[v[1]][0], turnos[v[2]], usuarios[v[3]], v[4]] for k, v in
                               reservas.items()
                               if fecha_reporte in v]

                    if reporte:
                        print(tabulate(reporte, headers=["Folio", "Fecha", "Sala", "Turno", "Cliente", "Evento"],
                                       tablefmt='psql',
                                       numalign="left"))
                    else:
                        print(f"No hay reservas el día {fecha_reporte}.\n")

                else:
                    print("No hay reservas registradas.\n")

            elif opcion_reporte == "b":

                if reservas:

                    while True:
                        try:
                            fecha_reporte = input("Ingrese la fecha para el reporte (dd/mm/aaaa):\n")
                            fecha = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y').date()
                            break
                        except ValueError:
                            print("Ingrese una fecha valida en el formato dd/mm/aaaa.\n")
                            continue

                    reporte = [[k, v[0], salas[v[1]][0], turnos[v[2]], usuarios[v[3]], v[4]] for k, v in
                               reservas.items() if fecha_reporte in v]

                    if reporte:
                        df = pd.DataFrame(reporte, columns=["Folio", "Fecha", "Sala", "Horario", "Cliente", "Evento"])

                        writer = pd.ExcelWriter(f"reporte-{fecha_reporte.replace('/', '-')}.xlsx")
                        df.to_excel(writer)
                        writer.save()
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

        id_sala = max(salas, default=0) + 1

        salas[id_sala] = [nombre_sala, cupo_sala]

        print(f"\nLa sala '{nombre_sala}' fue registrada con clave '{id_sala}'.\n")

    elif opcion == "d":

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

    elif opcion == "e":
        break

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
