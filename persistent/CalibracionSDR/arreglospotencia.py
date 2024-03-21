

"""
Bloque que implementa un mecanismo análogo a "Potumbral"
para el cálculo de la potencia de las muestras.
"""

import numpy as np
from gnuradio import gr
import math
# Bloque de Python utilizado al momento de calibrar el SDR con el analizador de espectros.


class blk(gr.sync_block): 
	def __init__(self, designator="B"): 
		gr.sync_block.__init__(self,name='Embedded Python Block',in_sig=[np.complex64],out_sig=[np.complex64])
		self.designator = designator
		self.arr_pow_actual = np.full(50, 2e-14)
		self.power = 2e-7
		self.prommovil = 0
		self.pow_db = 0
		self.contador = 0
		self.sumador = 0
		self.pow_actual = 1
		self.i = 0
		self.N = 100 #Cantidad de iteraciones del for correspondiente a 20ms
		self.subintervalos = 0
		self.N_muestras = []
		self.pow_4s = np.zeros(200)
		
		self.pow_minuto = [2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14, 2e-14] #Se inicializa el arreglo para que el umbral de -107dBm=2e-14
		
		self.arr_pow_actual = np.full(5, 2e-14) #Se inicializa el arreglo que determina la potencia actual con el promedio. Se toma un promedio movil del ultimo ms (5 muestras) iniciando con una potencia inicial igual al umbral minimo  
		
		self.umbral = 2e-14
		
		self.umb_y_pow_actual = np.zeros(2) #Se crea este arreglo que es lo que se le pasa al transmisor. Un umbral y una potencia actual en ese orden para que sepa interpretarlo.
		self.salida_db = np.zeros(2) #Se crea este arreglo que es lo que se le pasa al transmisor. Un umbral y una potencia actual en ese orden para que sepa interpretarlo.
		
		self.umbral_actual = 1
		
		self.salida = np.zeros(2)

		self.pow_avg = 2e-7
		
		self.subint = 0
		


	def work(self, input_items, output_items):
		if self.designator == "B":
			self.i = 0
			while self.i < len(input_items[0]):
				self.pow_actual = np.abs(input_items[0][self.i])**2
				self.pow_actual = 10*math.log10(self.pow_actual)
				self.pow_actual = 0.9941*self.pow_actual -12.99
				if self.pow_actual == 0: #Caso de borde
					self.pow_actual = 1e-20
				
				self.umbral_actual = (10*math.log10(self.umbral/0.001)) + 10 #Se le suma 10dB al umbral, el umbral actual es el ultimo calculado que se actualiza cada 4s.
				self.salida_db[0] = self.umbral_actual
				self.salida_db[1] = self.pow_actual #10*math.log10(self.pow_actual/0.001)
				#self.salida_db[1] = 0.9941*self.salida_db[1] + 6.893 - 20
				self.N_muestras = np.append(self.N_muestras, self.pow_actual)
				
				self.N = self.N - 1
				if self.N == 0: #Si ya acumule la potencia de los ultimos 20 ms.
					self.pow_avg = np.mean(self.N_muestras) #Los 200 valores de potencia que se acumulan para formar los 4s es el promedio de los 20ms.
					self.N_muestras = []
					self.N = 100
					self.pow_4s[self.subintervalos] = self.pow_avg #Se acumulan los 200 valores de potencia para llegar a 4s.
					self.subintervalos += 1
					
				if self.subintervalos == 200: #Si completé los 200 subintervalos de 20ms tengo 4s y agarro el mínimo de eso.
					po_4 = np.min(self.pow_4s)
					self.pow_minuto.pop(-1)
					self.pow_minuto.insert(0, po_4)
					self.umbral = np.min(self.pow_minuto)
					if self.umbral < 2e-14: #Si la potencia es menor a -107dBm se pone en -107dBm.
						self.umbral = 2e-14
					
					elif self.umbral > 1.9e-5: #Si la potencia es mayor a -17dBm se pone en -17dBm (porque se suma 10dB después).
						self.umbral = 1.9e-5
					
					self.subintervalos = 0
					self.subint = self.subint+1
					
				self.i = self.i + 10
				self.contador = self.contador + 1
				if self.contador > 4000000 and self.contador < 4000050:
					print("umbral: ", self.salida_db[0], "potencia: ", self.salida_db[1])
			#else:
			#	print("potencia: ", self.salida_db[1])
				
		    	
		return 256
