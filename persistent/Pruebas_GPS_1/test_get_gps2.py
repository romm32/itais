#!/usr/bin/env python3

# Este script fue una prueba intermedia para que el script get_gps funcionara.

import zmq
import time
import pynmea2

serial_port = '/dev/ttyUSB0'
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5570")

topic_info = "info"
topic_utc = "UTC"


while True:
    try:
        # Se crea info GPS falsa para probar.
        line = "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A"
        msg = pynmea2.parse(line)
        
        datos = {"long": msg.longitude, "lat": msg.latitude, "sog": msg.spd_over_grnd, "cog": msg.true_course}
        message_info = f"{topic_info} {datos}"
        message_utc = f"{topic_utc} {msg.timestamp}"

        # Se envían los mensajes
        socket.send_string(message_info)
        socket.send_string(message_utc)

        time.sleep(1)  # Se agrega un tiempo entre mensajes por las dudas.
    except KeyboardInterrupt:
        break

socket.close()
context.term()
