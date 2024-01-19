#!/usr/bin/env python3

# Este script fue escrito para verificar que se puede acceder a información de GPS con
# la conexión establecida. 

import serial
import pynmea2 

serial_port = '/dev/ttyUSB0'
ser = serial.Serial(serial_port, baudrate=9600, timeout=1)

while True:
    # Se lee una línea o un dato desde el GPS
    line = ser.readline().decode('utf-8').strip()

    # Se verifica si la línea recibida es válida o no, viendo si tiene el
    # inicio NMEA necesario.
    if line.startswith('$GPRMC'): # Inicialmente pedía
        # un mensaje GPGSA, pero ese no me da informacion de speed over ground, por ej.
        try:
            # Se parsea con NMEA la línea leída, y luego se imprime.
            msg = pynmea2.parse(line)
            print(msg)
            
            #print(msg.fields)
            # (('Timestamp', 'timestamp', <function timestamp at 0x7f337c870c10>), 
            # ('Status', 'status'), ('Latitude', 'lat'), ('Latitude Direction', 'lat_dir'),
            # ('Longitude', 'lon'), ('Longitude Direction', 'lon_dir'), 
            # ('Speed Over Ground', 'spd_over_grnd', <class 'float'>), 
            # ('True Course', 'true_course', <class 'float'>), 
            # ('Datestamp', 'datestamp', <function datestamp at 0x7f337c870ca0>), 
            # ('Magnetic Variation', 'mag_variation'), ('Magnetic Variation Direction', 
            # 'mag_var_dir'))

        except pynmea2.ParseError as e:
            print(f"Error parsing NMEA sentence: {e}")