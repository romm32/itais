#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Romina Garcia, Maximo Pirri.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import numpy as np
from gnuradio import gr
import math
from datetime import datetime, timedelta
import pmt

class potumbral(gr.sync_block):  
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, designator):  #¡¡¡ capaz hay que hacer algo distinto cuando tenemos un canal de cuando tenemos dos canales!!!
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='potumbral',   # will show up in GRC
            in_sig=[np.float32], # (np.complex64,10)],
            out_sig=[] #[(np.float32,2)] para probar, dado que tenemos una salida con dos valores
        )
        self.N = 100 #Cantidad de iteraciones del for correspondiente a 20ms
        self.subintervalos = 0
        self.N_muestras = []
        self.pow_4s = np.zeros(200)
        
        self.pow_minuto = [2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14] #Se inicializa el arreglo para que el umbral de -107dBm=2e-14
        
        self.arr_pow_actual = np.full(5, 2e-14) #Se inicializa el arreglo que determina la potencia actual con el promedio. Se toma un promedio movil del ultimo ms (5 muestras) iniciando con una potencia inicial igual al umbral minimo  
        
        self.umbral = 2e-14
        
        self.umb_y_pow_actual = np.zeros(2) #Se crea este arreglo que es lo que se le pasa al transmisor. Un umbral y una potencia actual en ese orden para que sepa interpretarlo.
        self.salida_db = np.zeros(2) #Se crea este arreglo que es lo que se le pasa al transmisor. Un umbral y una potencia actual en ese orden para que sepa interpretarlo.
        
        self.slots_per_minute = 2250
        self.slot_duration = 60/2250
        self.samples_per_slot = int(self.slot_duration*50000)
        
        self.pow_actual = 1
        self.umbral_actual = 1
        
        self.salida = np.zeros(2)

        self.pow_avg = 2e-7
        
        self.slot_actual = 0 #Variable que se utiliza para saber en qué slot del frame actual se está        
        self.contador_muestra = -10 #Variable que permite determinar qué muestra del slot actual se está procesando, se inicializa en -10 porque la primera vez se le suma 10.  
        
        self.intervalo_evaluado = [False, False, False, False, False]#, False, False, False, False, False, False] #Se define el arreglo que contendrá los últimos 11 intervalos de 100 microsegundos (0,1 ms). Esta es la cantidad de intervalos que entra en el rango donde se debe medir la potencia. Se toman intervalos de esa longitud pues es la longitud que se usa para calcular la potencia (la potencia es el promedio de los últimos 100 microsegundos).
        
        self.puedo_usar = 0 #Variable que determina si puede utilizarse o no el slot actual, inicializada con -1 (no se puede transmitir)
        
        self.salida_slot = [2, 2] #np.zeros(2) #Tupla usada para indicar si en e canal el slot actual puede usarse para transmitir o no
                
        self.slots_candidatos = np.full(10, -1) #Arreglo con los slots donde el transmisor desea transmitir
        
        self.slots_recibidos = []
        self.subint = 0
        
        self.ultimo_slot = -1
        self.cambio = False
        self.slots_en_ejecucion = 0
        self.slots_sensados = 0
        self.imprimir = False
        self.i = 0
        self.canal = designator
        self.unavez = True
        self.s_y_p_numero = 0
        self.s_y_p_dos = np.zeros(2)
        self.designator = designator
        self.portName_in = 'candidatos'
        self.message_port_register_in(pmt.intern(self.portName_in))
        self.set_msg_handler(pmt.intern("candidatos"), self.process_message)
        
        self.portName = 'slot_y_puedo'
        self.message_port_register_out(pmt.intern(self.portName))
        
    def process_message(self, message):
        # Retrieve message payload and save it to a variable
        self.slots_candidatos = pmt.to_python(message) # lista con los candidatos
        print("llegaron candidatos", self.designator, self.slots_candidatos)
        
    def work(self, input_items, output_items):
		
        if self.unavez:
        	print("inicializo potumbral")
        	self.unavez = False
        	
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = time_elapsed.total_seconds() * 1000
        slot_index = (milliseconds_elapsed)*self.slots_per_minute/60000 #Cantidad de slots desde que empezó el minuto.
		
        self.slot_actual = int(slot_index) #Se guarda el slot actual donde estamos parados
        self.contador_muestra = int((slot_index-self.slot_actual)*self.samples_per_slot) #Cantidad de tiempo que pasó desde que empezó el slot en cantidad de muestras. Es decir si 1 sot son 1333 muestras, se guarda cuantas muestras hay en 0.(algo) slots.
        
        # ahora es una entrada de message - self.slots_candidatos = np.real(input_items[1][0])

        if self.slot_actual != self.ultimo_slot:
                self.ultimo_slot = self.slot_actual
                self.cambio = True
                if self.imprimir:
                    self.slots_en_ejecucion = self.slots_en_ejecucion + len(input_items[0])/self.samples_per_slot
                    
                    #print(self.slots_candidatos, self.slot_actual)
                    
                    if self.contador_muestra > 41:
                        self.slots_sensados = self.slots_sensados + int((len(input_items[0]) - (self.samples_per_slot - self.contador_muestra))/self.samples_per_slot)
                        if (len(input_items[0]) - (self.samples_per_slot - self.contador_muestra))%self.samples_per_slot > 98:
                            self.slots_sensados = self.slots_sensados + 1
                    else:
                        self.slots_sensados = self.slots_sensados +int(len(input_items[0])/self.samples_per_slot)
                        if len(input_items[0])%self.samples_per_slot > 98:
                            self.slots_sensados = self.slots_sensados + 1
                    if np.abs(2249 - self.slot_actual) < 2:
                        print("ejecutados ", self.canal, self.slots_en_ejecucion)
                        print("sensados ", self.canal, self.slots_sensados)
                        self.slots_en_ejecucion = 0
                        self.slots_sensados = 0
		
        while self.i < len(input_items[0]) and (self.puedo_usar != 1):
            if self.slot_actual != self.ultimo_slot:
                self.ultimo_slot = self.slot_actual
                self.cambio = True
                
            self.contador_muestra += 10
            #muestra_actual = input_items[0][self.i]

            self.pow_actual = input_items[0][self.i]#np.abs(muestra_actual)**2 #Paso la muestra actual compleja a un real con la potencia del complejo. Esto implica que se tendrá una muestra de potencia cada 0,2ms (o 200 micro).
            if self.pow_actual == 0: #Caso de borde
                self.pow_actual = 1e-20

            self.umbral_actual = (10*math.log10(self.umbral/0.001)) + 10 #Se le suma 10dB al umbral, el umbral actual es el ultimo calculado que se actualiza cada 4s. 	
			
            self.salida_db[0] = self.umbral_actual 
            self.salida_db[1] = 10*math.log10(self.pow_actual/0.001)
            
            self.salida_db[1] = 0.9941*self.salida_db[1] + 6.893 
            
			
            self.N_muestras = np.append(self.N_muestras, self.pow_actual) #Se acumulan las 1000 muestras que se corresponde con 100 ejecuciones del while que acumula de a 10 muestras. Así se forman los 20ms, esto se acumula independientemente del calculo de la potencia actual del canal.
            self.N = self.N - 1
            if self.N == 0: #Si ya acumule la potencia de los ultimos 20 ms.
                self.pow_avg = np.mean(self.N_muestras) #Los 200 valores de potencia que se acumulan para formar los 4s es el promedio de los 20ms.
                self.N_muestras = []
                self.N = 100
                self.pow_4s[self.subintervalos] = self.pow_avg #Se acumulan los 200 valores de potencia para llegar a 4s.
                self.subintervalos += 1

            if self.subintervalos == 200: #Si completé los 200 subintervalos de 20ms tengo 4s y agarro el mínimo de eso.
                po_4 = np.min(self.pow_4s)
                #El umbral del canal se actualiza cada 4s y esto se hace tomando el minimo entre los ultimos 15 valores de 4s de potencia que se acumularon. En otras palabras, en el ultimo minuto se acumulan 15 muestras de potencia de 4s, se toma entonces el minimo de esas 15 como el nuevo valor de umbral. Para actualizar cuales son los ultimos 15 valores de 4s, se hace el mismo procedimiento con el for que con arr_pow_actual, o sea, se saca el ultimo elemento y se pone el nuevo en el inicio.
                self.pow_minuto.pop(-1)
                self.pow_minuto.insert(0, po_4)

                self.umbral = np.min(self.pow_minuto)
                if self.umbral < 2e-14: #Si la potencia es menor a -107dBm se pone en -107dBm.
                    self.umbral = 2e-14
                elif self.umbral > 1.9e-5: #Si la potencia es mayor a -17dBm se pone en -17dBm (porque se suma 10dB después).
                    self.umbral = 1.9e-5
                self.subintervalos = 0 
                self.subint = self.subint+1
                print("4s mas ", self.subint, self.canal, time_elapsed.total_seconds())
			
            if self.slot_actual in self.slots_candidatos and self.cambio: #Nos fijamos si estamos en un slot en donde se desee transmitir.
                if self.contador_muestra >= 41 and self.contador_muestra < 99: #Nos fijamos si estamos en una muestra donde se debe medir el canal para determinar si el slot está libre o en uso.
                    self.intervalo_evaluado.pop(-1)
                    self.intervalo_evaluado.insert(0, self.salida_db[1] < self.salida_db[0])
					
                elif self.contador_muestra >= 99 and self.contador_muestra <= 110: #Si ya se recorrieron todas las muestras donde se debe evaluar el slot, ya se actualizaron las 5 entradas del arreglo y se puede determinar si el slot está libre o no.
                    self.puedo_usar = int(np.sum(self.intervalo_evaluado) > 2) #Si 3 o más de las 5 entradas son True (suma más de 2), la potencia es menor al umbral en todo el tramo y se puede usar ese slot, está libre.

                    self.salida_slot[1] = self.puedo_usar #Se fija si el slot está libre o no en la salida.
                    self.salida_slot[0] = self.slot_actual #Se fija el numero de slot en la salida
                    PMT_msg = pmt.to_pmt(self.salida_slot)
                    self.message_port_pub(pmt.intern(self.portName), PMT_msg)
                    
                    print(self.canal, "u ", self.salida_db[0], "p", self.salida_db[1], "int", np.sum(self.intervalo_evaluado), "sal ", self.salida_slot)
                    
                	
            if self.contador_muestra + 10 >= self.samples_per_slot: #Si la muestra es la última muestra del slot, se debe aumentar en 1 el slot y poner la muestra actual en 0.
                self.contador_muestra = self.contador_muestra + 10 - self.samples_per_slot #Se inicializa en -10 o -9 o -8 o lo que corresponda porque en la siguiente ejecución del while se le suma 10 y en este caso de borde se iría al 8 o al 9 o al 10 y se saltearía algunos valores de muestras.
                self.ultimo_slot = self.slot_actual
                if self.slot_actual >= 2249: #Si estamos en la última muestra del último slot, en vez de aumentar en uno el slot actual, debemos volver a 0 el slot.
                    self.slot_actual = 0
                else:
                    self.slot_actual += 1
            self.i = self.i + 10		
	
        self.cambio = False
        self.puedo_usar = 0
        self.i = 0
        		
        return 16 #len(input_items[0])
        
        
        


