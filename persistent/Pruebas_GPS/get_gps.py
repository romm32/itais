#!/usr/bin/env python3

# Este script fue escrito para obtener información de posición desde el GPS. La información
# se enviará a través de socket a la función que quiera armar los mensajes NMEA a transmitir.

import serial
import pynmea2 
import zmq

serial_port = '/dev/ttyUSB0'
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5570")

# Se definen dos topics, uno para cada tipo de info que se quiere mandar a otros scripts
topic_utc = "UTC"
topic_info = "info"

while True:
    # Se lee una línea o un dato desde el GPS
    line = ser.readline().decode('utf-8').strip()

    # Se verifica si la línea recibida es válida o no, viendo si tiene el
    # inicio NMEA necesario.
    if line.startswith('$GPRMC'):
        try:
            # Se parsea con NMEA la línea leída, se generan las estructuras de datos
            # necesarias para la transmisión a través del socket, y se envía.
            msg = pynmea2.parse(line)
            datos = {"long": msg.longitude, "lat": msg.latitude, "sog": msg.spd_over_grnd, "cog": msg.true_course} 
            message_info = f"{topic_info} {datos}"
            message_utc = f"{topic_utc} {msg.timestamp}"
            
            socket.send_string(message_info)
            socket.send_string(message_utc)

            print("messages sent", message_info)
            print("messages sent", message_utc)

        except pynmea2.ParseError as e:
            print(f"Error parsing NMEA sentence: {e}")
            socket.close()
            context.term()
            ser.close()

        
        
