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

            reservas_formato["SALA"].append(reserva_en_turno[1]["sala"])
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

        print("No hay reservas en esa fecha.")


def imprimir_confirmacion(folio, fecha, sala, cliente, evento, horario):
    formato_impresion = {
        "FOLIO": [folio],
        "FECHA": [fecha],
        "SALA": [sala],
        "CLIENTE": [cliente.capitalize()],
        "NOMBRE DEL EVENTO": [evento.capitalize()],
        "TURNO": [horario.capitalize()]
    }

    df_impresion = pandas.DataFrame(formato_impresion)

    print("\nReserva exitosa.")

    print(tabulate(df_impresion, headers='keys', tablefmt='psql', showindex=False))

    print("")


usuarios = {}
salas = {}
reservas = {}

id_user = 1000
id_sala = 0
folio = 100000

fecha_hoy = datetime.date.today()

while True:

    opcion = input("""+----------------------------------------+
|       Ingrese la opcion deseada:       |
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

        nombre_user = input("Ingrese el nombre del usuario:\n")

        id_user += 1

        usuarios[str(id_user)] = nombre_user

        print(f"\nEl usuario '{nombre_user}' fue registrado con la clave '{id_user}'.\n")

    elif opcion == "b":

        id_sala += 1

        nombre_sala = input("Ingrese el nombre de la sala:\n")

        while True:

            try:
                cupo_sala = int(input("Ingrese la capacidad de la sala:\n"))
                break

            except ValueError:
                print("Ingrese un numero entero.")

        salas[id_sala] = {"nombre_sala": nombre_sala, "cupo": cupo_sala}

        print(f"\nLa sala '{nombre_sala}' fue registrada con clave '{id_sala}'.\n")

    elif opcion == "c":

        folio += 1

        user_id = input("Ingrese su clave de usuario:\n")

        if user_id in usuarios.keys():

            while True:

                try:

                    fecha_reserva = input("ingrese la fecha de la reserva (dd/mm/aaaa):\n")
                    fecha_datetime = datetime.datetime.strptime(fecha_reserva, '%d/%m/%Y').date()
                    break

                except ValueError:

                    print("Ingrese una fecha valida.")
                    continue

            limite_reserva = (fecha_datetime - fecha_hoy).days

            if limite_reserva > 2:

                sala_id = int(input("Ingrese la clave de la sala:\n"))

                if sala_id in salas.keys():

                    while True:

                        horario_reserva = input("""Ingrese el horario de la sala:
a) Matutino
b) Vespertino
c) Nocturno
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

                            print("Opcion no valida.")
                            continue

                    for reserva in reservas.values():

                        if fecha_reserva in reserva.values():

                            if sala_id in reserva.values():

                                if horario_reserva not in reserva.values():

                                    nombre_evento = input("Ingrese el nombre del evento:\n")

                                    reservas[folio] = {
                                        "fecha": fecha_datetime.strftime("%d/%m/%Y"),
                                        "sala": sala_id,
                                        "horario": horario_reserva,
                                        "usuario": user_id,
                                        "evento": nombre_evento,
                                    }

                                    imprimir_confirmacion(folio, fecha_datetime.strftime("%d/%m/%Y"), sala_id,
                                                          usuarios[user_id], nombre_evento, horario_reserva)

                                    break

                                else:

                                    print("Horario Ocupado")
                                    break

                            else:

                                nombre_evento = input("Ingrese el nombre del evento:\n")

                                reservas[folio] = {
                                    "fecha": fecha_datetime.strftime("%d/%m/%Y"),
                                    "sala": sala_id,
                                    "horario": horario_reserva,
                                    "usuario": user_id,
                                    "evento": nombre_evento,
                                }

                                imprimir_confirmacion(folio, fecha_datetime.strftime("%d/%m/%Y"), sala_id,
                                                      usuarios[user_id], nombre_evento, horario_reserva)

                                break

                        else:

                            nombre_evento = input("Ingrese el nombre del evento:\n")

                            reservas[folio] = {
                                "fecha": fecha_datetime.strftime("%d/%m/%Y"),
                                "sala": sala_id,
                                "horario": horario_reserva,
                                "usuario": user_id,
                                "evento": nombre_evento,
                            }

                            imprimir_confirmacion(folio, fecha_datetime.strftime("%d/%m/%Y"), sala_id,
                                                  usuarios[user_id], nombre_evento, horario_reserva)

                            break

                    else:

                        nombre_evento = input("Ingrese el nombre del evento:\n")

                        reservas[folio] = {
                            "fecha": fecha_datetime.strftime("%d/%m/%Y"),
                            "sala": sala_id,
                            "horario": horario_reserva,
                            "usuario": user_id,
                            "evento": nombre_evento,
                        }

                        imprimir_confirmacion(folio, fecha_datetime.strftime("%d/%m/%Y"), sala_id,
                                              usuarios[user_id], nombre_evento, horario_reserva)

                else:

                    print("Sala no registrada.")

            else:

                print("Se necesitan dos dias de anticipacion para reservar un evento.")
        else:

            print("Usuario no registrado.")

    elif opcion == "d":

        folio_mod = int(input("Ingrese el folio de la reserva:\n"))

        if folio_mod in reservas.keys():

            nombre_evento = input("Ingrese el nuevo nombre del evento:\n")

            reservas[folio_mod]["evento"] = nombre_evento

        else:

            print("Folio invalido")

    elif opcion == "e":

        imprimir_reporte()

    elif opcion == "f":
        break

    else:

        print("opcion no valida")
