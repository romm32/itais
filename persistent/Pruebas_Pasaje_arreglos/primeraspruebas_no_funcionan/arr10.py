"""
Bloque que genera y envía un arreglo de 10 valores.
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  
	def __init__(self, example_param=1.0): 
		gr.sync_block.__init__(
		self,
		name='Embedded Python Block',  
		in_sig=[np.complex64],
		out_sig=[(np.complex64, 1), (np.float32, 10)]
		)
		self.example_param = example_param
		self.arreglo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		self.limite = 10
		
	def work(self, input_items, output_items):
		output_items[0][:] = input_items[0] * 2
		output_items[1] = self.arreglo + np.ones(10)
		if self.limite > 0:
			print("rx mando arreglo ", output_items[1])
			self.limite = self.limite - 1
			
		return len(output_items[0])

