import datetime
import pandas
from tabulate import tabulate


def imprimir_reporte():
    while True:

        try:

            fecha_reporte = input("ingrese la fecha de la reserva (dd/mm/aaaa):\n")
            formato_datetime = datetime.datetime.strptime(fecha_reporte, '%d/%m/%Y').date()
            break

        except ValueError:
            print("La fecha no es valida")

            continue

    fecha_formato = formato_datetime.strftime("%d/%m/%Y")

    reservas_formato = {"SALA": [],
                        "CLIENTE": [],
                        "EVENTO": [],
                        "TURNO": []
                        }

    contador = 0

    for reserva_en_turno in reservas.items():

        if fecha_formato in reserva_en_turno[1].values():
            contador += 1

            reservas_formato["SALA"].append(salas[reserva_en_turno[1]["sala"]]["nombre_sala"])
            reservas_formato["CLIENTE"].append(usuarios[reserva_en_turno[1]["usuario"]].capitalize())
            reservas_formato["EVENTO"].append(reserva_en_turno[1]["evento"].capitalize())
            reservas_formato["TURNO"].append(reserva_en_turno[1]["horario"].capitalize())

            pass

    if contador != 0:

        df = pandas.DataFrame(reservas_formato)

        print(f"\nREPORTE DE RESERVACIONES PARA LA FECHA {fecha_formato}")

        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

        print("")

    else:

        print("No hay reservas en esa fecha.\n")


def imprimir_confirmacion(folio_func, fecha, sala, cliente, evento, horario):
    formato_impresion = {
        "FOLIO": [folio_func],
        "FECHA": [fecha],
        "SALA": [salas[sala]["nombre_sala"]],
        "CLIENTE": [cliente.capitalize()],
        "NOMBRE DEL EVENTO": [evento.capitalize()],
        "TURNO": [horario.capitalize()]
    }

    df_impresion = pandas.DataFrame(formato_impresion)

    print("\nReserva exitosa.")

    print(tabulate(df_impresion, headers='keys', tablefmt='psql', showindex=False))

    print("")


def guardar_reserva(diccionario, folio_func, fecha, sala, cliente, evento, horario):
    diccionario[folio_func] = {
        "fecha": fecha,
        "sala": sala,
        "horario": horario,
        "usuario": cliente,
        "evento": evento,
    }


usuarios = {}
salas = {}
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

                id_user = max(usuarios, default=100) + 1

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
                break

            except ValueError:
                print("Ingrese un numero entero.")

        id_sala = max(salas, default=0) + 1

        salas[id_sala] = {"nombre_sala": nombre_sala, "cupo": cupo_sala}

        print(f"\nLa sala '{nombre_sala}' fue registrada con clave '{id_sala}'.\n")

    elif opcion == "c":

        while True:

            try:

                user_id = int(input("Ingrese su clave de usuario:\n"))
                break

            except ValueError:

                continue

        if user_id in usuarios.keys():

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

                        if fecha_reserva in reserva.values():

                            if sala_id in reserva.values():

                                if horario_reserva not in reserva.values():

                                    while True:

                                        nombre_evento = input("Ingrese el nombre del evento\n")

                                        if nombre_evento == "":
                                            print("El nombre no puede quedar vació.\n")
                                            continue

                                        else:

                                            folio = max(reservas, default=10000) + 1

                                            guardar_reserva(reservas, folio, fecha_reserva,
                                                            sala_id,
                                                            user_id, nombre_evento, horario_reserva)

                                            imprimir_confirmacion(folio, fecha_datetime.strftime("%d/%m/%Y"), sala_id,
                                                                  usuarios[user_id], nombre_evento, horario_reserva)

                                            break
                                    break
                                else:

                                    print("Horario Ocupado")
                                    break

                            else:

                                while True:

                                    nombre_evento = input("Ingrese el nombre del evento\n")

                                    if nombre_evento == "":
                                        print("El nombre no puede quedar vació.\n")
                                        continue

                                    else:

                                        folio = max(reservas, default=10000) + 1

                                        guardar_reserva(reservas, folio, fecha_reserva, sala_id,
                                                        user_id, nombre_evento, horario_reserva)

                                        imprimir_confirmacion(folio, fecha_datetime.strftime("%d/%m/%Y"), sala_id,
                                                              usuarios[user_id], nombre_evento, horario_reserva)
                                        break
                                break
                        else:

                            while True:

                                nombre_evento = input("Ingrese el nombre del evento\n")

                                if nombre_evento == "":
                                    print("El nombre no puede quedar vació.\n")
                                    continue

                                else:

                                    folio = max(reservas, default=10000) + 1

                                    guardar_reserva(reservas, folio, fecha_reserva, sala_id,
                                                    user_id, nombre_evento, horario_reserva)

                                    imprimir_confirmacion(folio, fecha_datetime.strftime("%d/%m/%Y"), sala_id,
                                                          usuarios[user_id], nombre_evento, horario_reserva)
                                    break
                        break
                    else:

                        while True:

                            nombre_evento = input("Ingrese el nombre del evento\n")

                            if nombre_evento == "":
                                print("El nombre no puede quedar vació.\n")
                                continue

                            else:

                                folio = max(reservas, default=10000) + 1

                                guardar_reserva(reservas, folio, fecha_reserva, sala_id,
                                                user_id, nombre_evento, horario_reserva)

                                imprimir_confirmacion(folio, fecha_datetime.strftime("%d/%m/%Y"),
                                                      sala_id,
                                                      usuarios[user_id], nombre_evento, horario_reserva)
                                break

                else:

                    print("Sala no registrada.\n")

            else:

                print("Se necesitan dos días de anticipación para reservar un evento.\n")
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

            nombre_evento = input("Ingrese el nuevo nombre del evento:\n")

            reservas[folio_mod]["evento"] = nombre_evento

            print("Evento modificado con exito.\n")

        else:

            print("Folio invalido.\n")

    elif opcion == "e":

        imprimir_reporte()

    elif opcion == "f":
        break

    else:

        print("Opción no valida.\n")
