#!/usr/bin/env python3

# Este script fue escrito para obtener información de posición desde el GPS. La información
# se enviará a través de socket a la función que quiera armar los mensajes NMEA a transmitir.

import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5600")

# Se definen dos topics, uno para cada tipo de info que se quiere mandar a otros scripts
topic_utc = "UTC"
topic_info = "info"

while True:
    try:
        datos = {"long": 1, "lat": 2, "sog": 3, "cog": 4} 
        message_info = f"{datos}"
        socket.send_string(message_info)
        print("messages sent", message_info)
        time.sleep(5)
        
    
    except KeyboardInterrupt:
        socket.close()
        context.term()