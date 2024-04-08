#!/usr/bin/env python3

# Este script fue hecho para probar que el FTDI (el conversor USB-UART) funcionara bien.
# Lo que se hace es conectar el pin de transmisión del FTDI con su propio pin de recepción.
# Así, se envía uno o más caracteres por el pin de TX, y se verifica que se reciben esos 
# mismos caracteres a través del pin RX.

import serial
import time
# Se agregan las siguientes dos líneas porque tuvimos algunos problemas con 
# Python encontrando los módulos/paquetes que precisábamos.
import sys
sys.path.append('/home/mpirri/.local/lib/python3.8/site-packages')

# Se fija el puerto serial a utilizar, que se verificó con lsusb (comando
# a ejecutar en la terminal, enchufando y desenchufando el FTDI para ver cuál es
# su "nombre"), y el baud rate.
serial_port = '/dev/ttyUSB0' 
baud_rate = 9600 

# Se utiliza la librería serial de Python para abrir una conexión serial.
ser = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    # Se envían varios caracteres.
    ser.write(b'A')
    ser.write(b'B')
    ser.write(b'C')

    # Se espera un tiempo corto por las dudas.
    time.sleep(0.1)

    # Se lee e imprime un dato desde el dispositivo.
    received_data = ser.read(1)
    print("Received data:", received_data.decode('utf-8'))
    
    # Se repite el proceso para ver si se recibe también el segundo caracter enviado.
    time.sleep(0.1)
    received_data = ser.read(1)
    print("Received data:", received_data.decode('utf-8'))

finally:
    # Se cierra la conexión serial.
    ser.close()

