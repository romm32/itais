#!/usr/bin/env python3

# Este script fue escrito para obtener información de posición desde el GPS. La información
# se enviará a través de socket a la función que quiera armar los mensajes NMEA a transmitir.
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all topics
socket.setsockopt(zmq.RECONNECT_IVL, 1000)  # Reconnect every 1 second
socket.connect("tcp://127.0.0.1:5570")

topic_utc = "UTC"
topic_info = "info"

try:
    while True:
        raw_message = socket.recv_string()
        print(f"Received raw message: {raw_message}")
        topic, message = raw_message.split(' ', 1)

        # Se procesa el mensaje en función del topic del que viene.
        if topic == "UTC":
            print(f"Received UTC message: {message}")
        elif topic == "info":
            # Se utiliza el método eval para evaluar el string como un diccionario
            data_dict = eval(message)
            print(f"Received info message: {data_dict}")
        else:
            print(f"Received message with unknown topic: {topic}")
except KeyboardInterrupt:
    print("Received keyboard interrupt. Closing the socket.")
finally:
    socket.close()
    context.term()