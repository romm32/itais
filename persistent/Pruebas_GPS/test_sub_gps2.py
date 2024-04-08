#!/usr/bin/env python3

# Este script fue una prueba intermedia para que el script sub_gps funcionara.

import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Se subscribe a todos los topics,
                                             # y eventualmente se filtran los de interés.
socket.setsockopt(zmq.RECONNECT_IVL, 500)  # Se reinicia la conexión cada 500 ms
socket.connect("tcp://127.0.0.1:5570")

try:
    while True:
        # Se recibe el mensaje y se separa la info en nombre de topic y datos.
        raw_message = socket.recv_string()
        print(f"Received raw message: {raw_message}")
        topic, message = raw_message.split(' ', 1)

        # En función del topic recibido se definen los mensajes a imprimir.
        if topic == "info":
            # Se usa el método eval para pasar de string a diccionario de nuevo
            data_dict = eval(message)
            print(f"Received info message: {data_dict}")
        elif topic == "UTC":
            print(f"Received UTC message: {message}")
        else:
            print(f"Received message with unknown topic: {topic}")

except KeyboardInterrupt:
    print("Received keyboard interrupt. Closing the socket.")
finally:
    socket.close()
    context.term()
