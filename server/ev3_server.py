#!/usr/bin/env python3

import socket
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D

HOST = "0.0.0.0"
PORT = 12348

motor_traccion  = LargeMotor(OUTPUT_A)
motor_direccion = MediumMotor(OUTPUT_D)

print("[EV3 Server] Motores inicializados.")
print("[EV3 Server] Escuchando en {}:{}...".format(HOST, PORT))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print("[EV3 Server] Esperando conexion de la Raspberry Pi...")

    conn, addr = server.accept()
    print("[EV3 Server] Conectado desde {}".format(addr))

    with conn:
        buffer = ""

        while True:
            try:
                data = conn.recv(1024).decode("utf-8")

                if not data:
                    print("[EV3 Server] Conexion cerrada por la RPi.")
                    break

                buffer += data

                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    linea = linea.strip()

                    if not linea:
                        continue

                    partes = linea.split(",")
                    if len(partes) != 2:
                        print("[EV3 Server] Formato invalido: {}".format(linea))
                        continue

                    vel_pct = float(partes[0])
                    dir_deg = float(partes[1])

                    print("[EV3 Server] cmd -> vel: {:.1f}%  dir: {:.1f}deg".format(vel_pct, dir_deg))

                    if abs(vel_pct) < 1.0:
                        motor_traccion.stop()
                    else:
                        motor_traccion.run_forever(speed_sp=int(vel_pct * 10))

                    motor_direccion.run_to_abs_pos(
                        position_sp=int(dir_deg),
                        speed_sp=200,
                        stop_action="hold"
                    )

                    pos_counts = motor_traccion.position
                    vel_actual = motor_traccion.speed / 10.0
                    dir_actual = motor_direccion.position

                    respuesta = "{},{},{}\n".format(pos_counts, vel_actual, dir_actual)
                    conn.sendall(respuesta.encode("utf-8"))

                    print("[EV3 Server] state -> pos: {}  vel: {:.1f}  dir: {}".format(pos_counts, vel_actual, dir_actual))

            except (ConnectionResetError, BrokenPipeError):
                print("[EV3 Server] Conexion interrumpida.")
                break

            except Exception as e:
                print("[EV3 Server] Error: {}".format(e))
                break

    motor_traccion.stop()
    motor_direccion.stop()
    print("[EV3 Server] Motores detenidos. Servidor cerrado.")
