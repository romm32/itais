#!/usr/bin/env python3

# Este script fue escrito para obtener información de posición desde el GPS. La información
# se enviará a través de socket a la función que quiera armar los mensajes NMEA a transmitir.

import serial
import pynmea2 
import zmq
import time

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
        #print(line)
    except serial.SerialException as e:
        print(f"Serial exception occurred: {e}")
        continue
    
    if line.startswith('$GPRMC'):
        try:
            # Se parsea con NMEA la línea leída, se generan las estructuras de datos
            # necesarias para la transmisión a través del socket, y se envía.
            packet = pynmea2.parse(line)
            #print(packet)
            latitude = packet.latitude
            longitude = packet.longitude
            speed = packet.spd_over_grnd
            if speed is None: # sometimes we don't have access to gps data
                speed_in_knots = 0
            else:    
                speed_in_knots = speed*1.94384
            course = packet.true_course
            if course is None:
                course = 0
            gps_time_str = packet.timestamp
            #gps_time_datetime = datetime.strptime(gps_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            utc_second = gps_time_str.second
			# Print the information
            #print(f"Latitude: {latitude}, Longitude: {longitude}, Speed: {speed_in_knots} knots, Course: {course}, UTC second: {utc_second}")
            dict = {"speed": speed_in_knots, "lon": longitude, "lat": latitude, "course": course, "UTC_sec": utc_second}
            socket.send_string(f"{dict}")


        except pynmea2.ParseError as e:
            print(f"Error parsing NMEA sentence: {e}")
            socket.close()
            context.term()
            ser.close()

    else:
        socket.send_string(f"{dict}")
        #print(f"Latitude: {latitude}, Longitude: {longitude}, Speed: {speed_in_knots} knots, Course: {course}, UTC second: {utc_second}")
    
    time.sleep(0.00001) # no cambia nada esto por ahora

        
        
