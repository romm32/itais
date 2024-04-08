"""
Bloque que imita el funcionamiento de una versión antigua de Potumbral.
"""

import numpy as np
from gnuradio import gr
import pmt
import zmq
import numpy as np
import math
from datetime import datetime, timedelta
import numpy as np


class blk(gr.sync_block):  
 
    def __init__(self, designator="A"):  #¡¡¡ capaz hay que hacer algo distinto cuando tenemos un canal de cuando tenemos dos canales!!!
        gr.sync_block.__init__(
            self,
            name='potumbral',   
            in_sig=[np.complex64],
            out_sig=[(np.complex64,1), (np.complex64,1), (np.float32,2)] 
        )
        self.N_A = 1000 # Cantidad de muestras correspondiente a 20ms
        self.subintervalos_A = 0
        self.N_muestras_A = []
        self.pow_4s_A = np.zeros(200)
        
        self.N_B = 1000 # Cantidad de muestras correspondiente a 20ms
        self.subintervalos_B = 0
        self.N_muestras_B = []
        self.pow_4s_B = np.zeros(200)
        
        self.pow_minuto_A = np.full(15, 2e-14) # Se inicializa el arreglo para que el umbral de -107dBm=2e-14
        self.pow_minuto_B = np.full(15, 2e-14) # Se inicializa el arreglo para que el umbral de -107dBm=2e-14 
        
        self.arr_pow_actual_A = np.full(5, 2e-14) # Se inicializa el arreglo que determina la potencia actual con el promedio. Se toma un promedio movil del ultimo ms (5 muestras) iniciando con una potencia inicial igual al umbral minimo  
        self.arr_pow_actual_B = np.full(5, 2e-14) # Se inicializa el arreglo que determina la potencia actual con el promedio. Se toma un promedio movil del ultimo ms (5 muestras) iniciando con una potencia inicial igual al umbral minimo  
        
        self.umbral_A = 2e-14
        self.umbral_B = 2e-14
        
        self.umb_y_pow_actual_A = np.zeros(2) # Se crea este arreglo que es lo que se le pasa al transmisor. Un umbral y una potencia actual en ese orden para que sepa interpretarlo.
        self.salida_db_A = np.zeros(2) # Se crea este arreglo que es lo que se le pasa al transmisor. Un umbral y una potencia actual en ese orden para que sepa interpretarlo.
        
        self.umb_y_pow_actual_B = np.zeros(2) # Se crea este arreglo que es lo que se le pasa al transmisor. Un umbral y una potencia actual en ese orden para que sepa interpretarlo.
        self.salida_db_B = np.zeros(2) # Se crea este arreglo que es lo que se le pasa al transmisor. Un umbral y una potencia actual en ese orden para que sepa interpretarlo.
        self.slots_per_minute = 2250
        self.slot_duration = 60/2250
        self.samples_per_slot = int(self.slot_duration*50000)
        
        
        self.designator = designator
        
        self.pow_actual_A = 1
        self.umbral_actual_A = 1
        
        self.pow_actual_B = 1
        self.umbral_actual_B = 1
        
        self.salida_A = np.zeros(2)
        self.salida_B = np.zeros(2)
        
        self.power_A = 2e-7
        self.power_B = 2e-7
        
        self.pow_avg_A = 2e-7
        self.pow_avg_B = 2e-7
        
        self.slot_actual_A = 0 # Variable que se utiliza para saber en qué slot del frame actual se está
        self.slot_actual_B = 0 # Variable que se utiliza para saber en qué slot del frame actual se está
        
        self.contador_muestra_A = 0 # Variable que permite determinar qué muestra del slot actual se está procesando  
        self.contador_muestra_B = 0 # Variable que permite determinar qué muestra del slot actual se está procesando
        
        self.intervalo_evaluado_A = np.full(11, False) # Se define el arreglo que contendrá los últimos 11 intervalos de 100 microsegundos (0,1 ms). Esta es la cantidad de intervalos que entra en el rango donde se debe medir la potencia. Se toman intervalos de esa longitud pues es la longitud que se usa para calcular la potencia (la potencia es el promedio de los últimos 100 microsegundos).
        self.intervalo_evaluado_B = np.full(11, False) # Se define el arreglo que contendrá los últimos 11 intervalos de 100 microsegundos (0,1 ms). Esta es la cantidad de intervalos que entra en el rango donde se debe medir la potencia. Se toman intervalos de esa longitud pues es la longitud que se usa para calcular la potencia (la potencia es el promedio de los últimos 100 microsegundos).
        
        self.puedo_usar_A = -1 # Variable que determina si puede utilizarse o no el slot actual, inicializada con -1 (no se puede transmitir)
        self.puedo_usar_B = -1 # Variable que determina si puede utilizarse o no el slot actual, inicializada con -1 (no se puede transmitir)
        
        self.salida_slot_A = np.zeros(2) # Tupla usada para indicar si en e canal el slot actual puede usarse para transmitir o no
        self.salida_slot_B = np.zeros(2) # Tupla usada para indicar si en e canal el slot actual puede usarse para transmitir o no
                
        self.slots_candidatos_A = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19] # Arreglo con los slots donde el transmisor desea transmitir
        self.slots_candidatos_B = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19] # Arreglo con los slots donde el transmisor desea transmitir
        
        self.slots_recibidos = []
        
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = time_elapsed.total_seconds() * 1000
        slot_index = (milliseconds_elapsed)*self.slots_per_minute/60000 # Cantidad de slots desde que empezó el minuto.
        
        if milliseconds_elapsed > 59750:
        	print(len(self.slots_recibidos))
        	self.slots_recibidos = []
        
        num_taps = len(input_items[0]) 
        
        if (self.designator == "A"):
        	self.slot_actual_A = int(slot_index) # Se guarda el slot actual donde estamos parados
        	self.slots_recibidos.append(self.slot_actual_A)
        	self.contador_muestra_A = int((slot_index-self.slot_actual_A)*self.samples_per_slot) # Cantidad de tiempo que pasó desde que empezó el slot en cantidad de muestras. Es decir si 1 sot son 1333 muestras, se guarda cuantas muestras hay en 0.(algo) slots.
        	for i in range(0, len(input_items[0])):
        		self.contador_muestra_A += 1
        		muestra_actual = input_items[0][i]
        		self.power_A = np.abs(muestra_actual)**2 # Paso la muestra actual compleja a un real con la potencia del complejo. Esto permite acumular las muestras por un periodo de tiempo arbitrario (que definimos como 0,1ms o 100 micro) y luego tomar un promedio para obtener la potencia atual del canal.
        		# Para tomar el promedio de la potencia actual en el canal se toma un "promedio movil". En el for se rotan los valores del arreglo un lugar para la derecha excepto el primero que se va a sobreescribir. Si por ejemplo en el arreglo teniamos arr=[1, 2, 3, 4] despues del for va a quedar arr=[1,1,2,3]. Después se sobreescribe el primer elemento y se vuelve a calcular el promedio.
        		
        		for j in range(len(self.arr_pow_actual_A) - 1, 0, -1): 
        			self.arr_pow_actual_A[j] = self.arr_pow_actual_A[j - 1]	
        		
        		self.arr_pow_actual_A[0] = self.power_A
        		self.pow_actual_A = np.mean(self.arr_pow_actual_A) # La potencia actual del canal es el promedio de la potencia del ultimo ms del canal
        		self.umbral_actual_A = (10*math.log10(self.umbral_A/0.001)) + 10 # Se le suma 10dB al umbral, el umbral actual es el ultimo calculado que se actualiza cada 4s. 
        		
        		self.umb_y_pow_actual_A[0] = self.umbral_actual_A
        		self.umb_y_pow_actual_A[1] = self.pow_actual_A
        		
        		self.salida_A = self.umb_y_pow_actual_A # Se setea el parametro que se utilizara como salida, se saca siempre un arreglo con 2 elementos, umbral y potencia actuales (en ese orden). 
        		self.salida_db_A[0] = self.umbral_actual_A #*
        		if self.pow_actual_A == 0:
        			self.pow_actual_A = 1e-20
        		
        		self.salida_db_A[1] = 10*math.log10(self.pow_actual_A/0.001) # preguntar si va en dbm o no
        		
        		self.N_muestras_A = np.append(self.N_muestras_A, self.power_A) # Se acumulan las 1000 muestras para formar los 20ms, esto se acumula independientemente del calculo de la potencia actual del canal.
        		self.N_A = self.N_A - 1
        		if self.N_A == 0: # Si ya acumule la potencia de los ultimos 20 ms.
        			self.pow_avg_A = np.mean(self.N_muestras_A) # Los 200 valores de potencia que se acumulan para formar los 4s es el promedio de los 20ms.
        			self.N_muestras_A = []
        			self.N_A = 1000
        			self.pow_4s_A[self.subintervalos_A] = self.pow_avg_A # Se acumulan los 200 valores de potencia para llegar a 4s.
        			self.subintervalos_A += 1
        			#print(self.subintervalos_A)
        		if self.subintervalos_A == 200: # Si completé los 200 subintervalos de 20ms tengo 4s y agarro el mínimo de eso.
        			po_4_A = np.min(self.pow_4s_A)
        			# El umbral del canal se actualiza cada 4s y esto se hace tomando el minimo entre los ultimos 15 valores de 4s de potencia que se acumularon. En otras palabras, en el ultimo minuto se acumulan 15 muestras de potencia de 4s, se toma entonces el minimo de esas 15 como el nuevo valor de umbral. Para actualizar cuales son los ultimos 15 valores de 4s, se hace el mismo procedimiento con el for que con arr_pow_actual, o sea, se shiftea todo el arreglo un lugar para la derecha excepto la primera posicion y se sobreescribe dicho valor.
        			for t in range(len(self.pow_minuto_A) - 1, 0, -1):
        				self.pow_minuto_A[t] = self.pow_minuto_A[t - 1]
        			self.pow_minuto_A[0] = po_4_A
        			self.umbral_A = np.min(self.pow_minuto_A)
        			if self.umbral_A < 2e-14: # Si la potencia es menor a -107dBm se pone en -107dBm.
        				self.umbral_A = 2e-14
        			elif self.umbral_A > 1.9e-5: # Si la potencia es mayor a -17dBm se pone en -17dBm (porque se suma 10dB después).
        				self.umbral_A = 1.9e-5
        			self.subintervalos_A = 0 
        		
        		if self.slot_actual_A in self.slots_candidatos_A: # Nos fijamos si estamos en un slot en donde se desee transmitir.
        			if self.contador_muestra_A >= 41 and self.contador_muestra_A < 99: # Nos fijamos si estamos en una muestra donde se debe medir el canal para determinar si el slot está libre o en uso.
        				for r in range(len(self.intervalo_evaluado_A) - 1, 0, -1):
        					self.intervalo_evaluado_A[r] = self.intervalo_evaluado_A[r - 1]
        				self.intervalo_evaluado_A[0] = self.salida_db_A[1] < self.salida_db_A[0]
        				
        			elif self.contador_muestra_A == 99: # Si ya se recorrieron todas las muestras donde se debe evaluar el slot, ya se actualizaron las 11 entradas del arreglo y se puede determinar si el slot está libre o no.
        				self.puedo_usar_A = np.sum(self.intervalo_evaluado_A) == 11 # Si las 11 entradas son True (suma 11), la potencia es menor al umbral en todo el tramo y se puede usar ese slot, está libre.
        				
        			elif self.contador_muestra_A == 120:
        				self.puedo_usar_A = -1
        			self.salida_slot_A[1] = self.puedo_usar_A # Se fija si el slot está libre o no en la salida.
        			self.salida_slot_A[0] = self.slot_actual_A # Se fija el numero de slot en la salida
        			
        		if self.contador_muestra_A == self.samples_per_slot: # Si la muestra es la última muestra del slot, se debe aumentar en 1 el slot y poner la muestra actual en 0.
        			self.contador_muestra_A = 0
        			if self.slot_actual_A == 2250: # Si estamos en la última muestra del último slot, en vez de aumentar en uno el slot actual, debemos volver a 0 el slot.
        				self.slot_actual_A = 0
        			else:
        				self.slot_actual_A += 1
        			self.slots_recibidos.append(self.slot_actual_A)
        				
			
        		output_items[0][i] = self.salida_db_A[0]
        		output_items[1][i] = self.salida_db_A[1]
        		output_items[2][i] = self.salida_slot_A
        
        
        
        if (self.designator == "B"):
        	self.slot_actual_B = int(slot_index) # Se guarda el slot actual donde estamos parados
        	self.contador_muestra_B = int((slot_index-self.slot_actual_B)*self.samples_per_slot) # Cantidad de tiempo que pasó desde que empezó el slot en cantidad de muestras. Es decir si 1 sot son 1333 muestras, se guarda cuantas muestras hay en 0.(algo) slots.
        	for i in range(0, len(input_items[0])):
        		self.contador_muestra_B += 1
        		muestra_actual = input_items[0][i]
        		self.power_B = np.abs(muestra_actual)**2 # Paso la muestra actual compleja a un real con la potencia del complejo. Esto permite acumular las muestras por un periodo de tiempo arbitrario (que definimos como 0,1ms o 100 micro) y luego tomar un promedio para obtener la potencia atual del canal.
        		# Para tomar el promedio de la potencia actual en el canal se toma un "promedio movil". En el for se rotan los valores del arreglo un lugar para la derecha excepto el primero que se va a sobreescribir. Si por ejemplo en el arreglo teniamos arr=[1, 2, 3, 4] despues del for va a quedar arr=[1,1,2,3]. Después se sobreescribe el primer elemento y se vuelve a calcular el promedio.
        		
        		for j in range(len(self.arr_pow_actual_B) - 1, 0, -1): 
        			self.arr_pow_actual_B[j] = self.arr_pow_actual_B[j - 1]	
        		
        		self.arr_pow_actual_B[0] = self.power_B
        		self.pow_actual_B = np.mean(self.arr_pow_actual_B) # La potencia actual del canal es el promedio de la potencia del ultimo ms del canal
        		self.umbral_actual_B = (10*math.log10(self.umbral_B/0.001)) + 10 # Se le suma 10dB al umbral, el umbral actual es el ultimo calculado que se actualiza cada 4s. 
        		
        		self.umb_y_pow_actual_B[0] = self.umbral_actual_B
        		self.umb_y_pow_actual_B[1] = self.pow_actual_B
        		
        		self.salida_B = self.umb_y_pow_actual_B # Se setea el parametro que se utilizara como salida, se saca siempre un arreglo con 2 elementos, umbral y potencia actuales (en ese orden). 
        		self.salida_db_B[0] = self.umbral_actual_B #*
        		if self.pow_actual_B == 0:
        			self.pow_actual_B = 1e-20
        		
        		self.salida_db_B[1] = 10*math.log10(self.pow_actual_B/0.001) # preguntar si va en dbm o no
        		
        		self.N_muestras_B = np.append(self.N_muestras_B, self.power_B) # Se acumulan las 1000 muestras para formar los 20ms, esto se acumula independientemente del calculo de la potencia actual del canal.
        		self.N_B = self.N_B - 1
        		if self.N_B == 0: # Si ya acumule la potencia de los ultimos 20 ms.
        			self.pow_avg_B = np.mean(self.N_muestras_B) # Los 200 valores de potencia que se acumulan para formar los 4s es el promedio de los 20ms.
        			self.N_muestras_B = []
        			self.N_B = 1000
        			self.pow_4s_B[self.subintervalos_B] = self.pow_avg_B # Se acumulan los 200 valores de potencia para llegar a 4s.
        			self.subintervalos_B += 1
        		if self.subintervalos_B == 200: # Si completé los 200 subintervalos de 20ms tengo 4s y agarro el mínimo de eso.
        			po_4_B = np.min(self.pow_4s_B)
        			# El umbral del canal se actualiza cada 4s y esto se hace tomando el minimo entre los ultimos 15 valores de 4s de potencia que se acumularon. En otras palabras, en el ultimo minuto se acumulan 15 muestras de potencia de 4s, se toma entonces el minimo de esas 15 como el nuevo valor de umbral. Para actualizar cuales son los ultimos 15 valores de 4s, se hace el mismo procedimiento con el for que con arr_pow_actual, o sea, se shiftea todo el arreglo un lugar para la derecha excepto la primera posicion y se sobreescribe dicho valor.
        			for t in range(len(self.pow_minuto_B) - 1, 0, -1):
        				self.pow_minuto_B[t] = self.pow_minuto_B[t - 1]
        			self.pow_minuto_B[0] = po_4_B
        			self.umbral_B = np.min(self.pow_minuto_B)
        			if self.umbral_B < 2e-14: # Si la potencia es menor a -107dBm se pone en -107dBm.
        				self.umbral_B = 2e-14
        			elif self.umbral_B > 1.9e-5: # Si la potencia es mayor a -17dBm se pone en -17dBm (porque se suma 10dB después).
        				self.umbral_B = 1.9e-5
        			self.subintervalos_B = 0 
        		
        		if self.slot_actual_B in self.slots_candidatos_B: # Nos fijamos si estamos en un slot en donde se desee transmitir.
        			if self.contador_muestra_B >= 41 and self.contador_muestra_B < 99: # Nos fijamos si estamos en una muestra donde se debe medir el canal para determinar si el slot está libre o en uso.
        				for r in range(len(self.intervalo_evaluado_B) - 1, 0, -1):
        					self.intervalo_evaluado_B[r] = self.intervalo_evaluado_B[r - 1]
        				self.intervalo_evaluado_B[0] = self.salida_db_B[1] < self.salida_db_B[0]
        				
        			elif self.contador_muestra_B == 99: # Si ya se recorrieron todas las muestras donde se debe evaluar el slot, ya se actualizaron las 11 entradas del arreglo y se puede determinar si el slot está libre o no.
        				self.puedo_usar_B = np.sum(self.intervalo_evaluado_B) == 11 # Si las 11 entradas son True (suma 11), la potencia es menor al umbral en todo el tramo y se puede usar ese slot, está libre.
        				
        			elif self.contador_muestra_B == 120:
        				self.puedo_usar_B = -1
        			self.salida_slot_B[1] = self.puedo_usar_B # Se fija si el slot está libre o no en la salida.
        			self.salida_slot_B[0] = self.slot_actual_B # Se fija el numero de slot en la salida
        			if self.contador_muestra_B == 99:
        				print("u ", self.salida_db_B[0], "ints ", self.intervalo_evaluado_B, "sal ", self.salida_slot_B)
        			
        		if self.contador_muestra_B == self.samples_per_slot: # Si la muestra es la última muestra del slot, se debe aumentar en 1 el slot y poner la muestra actual en 0.
        			self.contador_muestra_B = 0
        			if self.slot_actual_B == 2250: # Si estamos en la última muestra del último slot, en vez de aumentar en uno el slot actual, debemos volver a 0 el slot.
        				self.slot_actual_B = 0
        			else:
        				self.slot_actual_B += 1
        				
        		if self.contador_muestra_B == 0:
        			print("salida", self.salida_slot_B)
			
        		output_items[0][i] = self.salida_db_B[0]
        		output_items[1][i] = self.salida_db_B[1]
        		output_items[2][i] = self.salida_slot_B
        		
        return len(output_items[0]) 
        
        
        
