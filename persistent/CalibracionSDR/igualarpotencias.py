"""
Bloque que implementa un mecanismo 
para el cálculo de la potencia de las muestras.
"""

import numpy as np
from gnuradio import gr

# Bloque de Python utilizado inicialmente para calibrar el SDR con el analizador de espectros.


class blk(gr.sync_block): 

    def __init__(self, designator): 
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block', 
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.designator = designator
        self.arr_pow_actual = np.full(50, 2e-14)
        self.power = 2e-7
        self.prommovil = 0
        self.pow_db = 0
        self.contador = 0
        self.sumador = 0
        self.pow_actual = 1

    def work(self, input_items, output_items):
        if self.designator == "B":

        	for i in range(0, len(input_items[0])):
        		muestra_actual = input_items[0][i]
        		self.power = np.abs(muestra_actual)**2 
        		self.prommovil = self.prommovil*1000/1001+(1/1001)*self.power
        		for i in range(len(self.arr_pow_actual) - 1, 0, -1): 
        			self.arr_pow_actual[i] = self.arr_pow_actual[i - 1]	
        			
        		self.arr_pow_actual[0] = self.power
        		self.pow_actual = np.mean(self.arr_pow_actual)
        		self.sumador = self.sumador + 10*np.log10(self.pow_actual)
        		self.contador = self.contador + 1
        		
        	if self.contador > 4000000:
        		promedio = self.sumador/self.contador
        		print("promedio: ", promedio)
        	else:
        		self.pow_db = 10*np.log10(self.pow_actual)
        		print("potencia: ", self.pow_db)
        		
        return 5000
