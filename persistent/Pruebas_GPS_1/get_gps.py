#!/usr/bin/env python3

# Versión antigua del script para obtener datos GPS.

import serial
import pynmea2 
import zmq

serial_port = '/dev/ttyACM0'
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5600")
from datetime import datetime


# Se definen dos topics, uno para cada tipo de info que se quiere mandar a otros scripts
#topic_utc = "UTC"
#topic_info = "info"

while True:
    # Se lee una línea o un dato desde el GPS
    line = ser.readline().decode('utf-8').strip()

    # Se verifica si la línea recibida es válida o no, viendo si tiene el
    # inicio NMEA necesario.
    if line.startswith('$GPRMC'):
        try:
            # Se parsea con NMEA la línea leída, se generan las estructuras de datos
            # necesarias para la transmisión a través del socket, y se envía.
            packet = pynmea2.parse(line)
            #print(packet.fields)
            latitude = packet.latitude
            longitude = packet.longitude
            speed = packet.spd_over_grnd
            if speed is None: # sometimes we don't have access to gps data
                speed_in_knots = 4
            else:    
                speed_in_knots = speed*1.94384
            course = packet.true_course
            gps_time_str = packet.timestamp
            #gps_time_datetime = datetime.strptime(gps_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            utc_second = gps_time_str.second
			# Print the information
            print(f"Latitude: {latitude}, Longitude: {longitude}, Speed: {speed} m/s, Course: {course}, UTC second: {utc_second}")
            dict = {"speed": speed_in_knots, "lon": longitude, "lat": latitude, "course": course, "UTC_sec": utc_second}
            socket.send_string(f"{dict}")


        except pynmea2.ParseError as e:
            print(f"Error parsing NMEA sentence: {e}")
            socket.close()
            context.term()
            ser.close()

        
        
