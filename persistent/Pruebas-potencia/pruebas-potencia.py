#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pmt
import zmq
import numpy as np
import math


# Se inicializa un socket para subscribirse a las muestras del canal.
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555") 
socket.setsockopt_string(zmq.SUBSCRIBE, "")

# El procesamiento de este bloque estaba en las primeras versiones de los bloques. No es correcto al final del proyecto.

N = 4 ##Cantidad de muestras correspondiente a 20ms REVISAR CUANTOS TAPS EQUIVALE A 0,5ms.
subintervalos = 0
N_muestras = []
pow_20ms = np.zeros(200)

pow_minuto = np.full(15, 2e-14) # Se inicializa el arreglo para que el umbral de -107dBm=2e-14 


umbral = 2e-14

# Como se precisa medir en un intervalo de un poco más de 1,1ms para determiar si se puede transmitir o no, se debe tomará un intervalo que este completamente dentro de eso. Para esto, se toman intervalos de 0,5ms y habrá al menos 1 completamente contenido dentro. FALTA VER CÓMO SABER CUÁL ESE ESE INTERVALO COMPLETAMENTE CONTENIDO. SI SE PUEDE DETERMINAR CUÁNDO ARRACA UN SLOT, BASTARÁ CON INDICAR CON UNA ETIQUETA EN CADA INTERVALO. 

# Como los intervalos que tomamos son de 0,5ms, debemos acumular 40 de estos para tener los 20ms deseados de los cuales se acumulará 200. 

umb_y_pow_actual = np.zeros(2) #S e crea este arreglo que es lo que se le pasa al transmisor. Un umbral y una potencia actual en ese orden para que sepa interpretarlo. 

with open("umbral_y_pow_actual.txt", "wb") as file:
    try:
        while True:
            print('hello')
            data = socket.recv()
            print('middletop')
            taps = np.frombuffer(data, dtype=np.complex64)
            power = np.abs(taps)**2 # Paso el arreglo de numeros complejos a un arreglo que tiene en cada posicion la potencia del complejo que tenia antes. Esto me permite tomar un promedio y obtener la potencia atual del canal. También lo agregamos en un arreglo hasta tener los 20ms que queremos.
            
            pow_actual = np.mean(power)
            umbral_actual = (10*math.log10(umbral)) + 10 # Se le suma 10dB al umbral 
            
            umb_y_pow_actual[0] = umbral_actual
            umb_y_pow_actual[1] = pow_actual
            
            file.write(umb_y_pow_actual)
            
            umb_y_pow_actual = np.zeros(2)
            
            N_muestras = np.append(N_muestras, power)
            N = N - 1
            if N == 0: 
            	pow_avg = np.mean(N_muestras)
            	N_muestras = []
            	N = 4 #40!!!
            	pow_20ms[subintervalos] = pow_avg
            	subintervalos += 1
            if subintervalos == 200: # Si completé los 200 subintervalos de 20ms tengo 4s y agarro el mínimo de eso.
            	pow_4s = np.min(pow_20ms)
            	for i in range(len(pow_minuto) - 1, 0, -1):
            		pow_minuto[i] = pow_minuto[i - 1]
            	pow_minuto[0] = pow_4s
            	umbral = np.min(pow_minuto)
            	if umbral < 2e-14: # Si la potencia es menor a 30dB se pone en 30dB EN VERDAD TIENE QUE CHEQUAERSE CON LOS -107dBm y también que no sea mayor a -7dBm o algo así.
            		umbral = 2e-14
            	elif umbral > 1.9e-4:
            		umbral = 1.9e-4
            	subintervalos = 0 
            print('chau')
    except KeyboardInterrupt:
        pass


socket.close()
context.term()

