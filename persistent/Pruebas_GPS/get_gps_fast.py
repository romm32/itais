#!/usr/bin/env python3

# Este script fue escrito para obtener información de posición desde el GPS. La información
# se enviará a través de socket a la función que quiera armar los mensajes NMEA a transmitir.
# Puede utilizarse cuando el módulo GPS está conectado por USB.

import serial
import pynmea2 
import zmq
import time

# Puede ser que haya problemas con esta línea dentro del Docker. Se tienen dos fuentes de error:
# 1. Cambió el nombre del dispositivo. Puede ser ttyACM0, ttyACM1 o ttyS0. Para saber cuál es,
# es posible ejecutar cat /dev/[nombre] y ver cuál de los tres funciona.
# 2. No se tienen permisos sobre el dispositivo (esto podría afectar la prueba 1.). Ejecutar el siguiente
# comando: sudo chmod 666 /dev/[nombre]

serial_port = '/dev/ttyACM1'
ser = serial.Serial(serial_port, baudrate=9600, timeout=0.00001)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5600")
from datetime import datetime


latitude = 0
longitude = 0
speed = 0
speed_in_knots = 0
course = 0
gps_time_str = 0
utc_second = 0
dict = {"speed": speed_in_knots, "lon": longitude, "lat": latitude, "course": course, "UTC_sec": utc_second}


while True:
    try:
    # Se lee una línea o un dato desde el GPS
        line = ser.readline().decode('utf-8').strip()
    except serial.SerialException as e:
        print(f"Serial exception occurred: {e}")
        continue
    
    if line.startswith('$GPRMC'):
        try:
            # Se parsea con NMEA la línea leída, se generan las estructuras de datos
            # necesarias para la transmisión a través del socket, y se envía.
            packet = pynmea2.parse(line)

            latitude = packet.latitude
            longitude = packet.longitude
            speed = packet.spd_over_grnd
            if speed is None: # A veces no tenemos datos de velocidad
                speed_in_knots = 0
            else:    
                speed_in_knots = speed*1.94384 # La velocidad viene en m/s
            course = packet.true_course
            if course is None:
                course = 0
            gps_time_str = packet.timestamp
            utc_second = gps_time_str.second
            dict = {"speed": speed_in_knots, "lon": longitude, "lat": latitude, "course": course, "UTC_sec": utc_second}
            socket.send_string(f"{dict}")

        except pynmea2.ParseError as e:
            print(f"Error parsing NMEA sentence: {e}")
            socket.close()
            context.term()
            ser.close()

    else:
        socket.send_string(f"{dict}")
    
    time.sleep(0.00001) 
        
        
