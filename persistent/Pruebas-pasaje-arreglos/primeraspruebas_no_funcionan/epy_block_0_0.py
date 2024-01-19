"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
	def __init__(self, example_param=1.0):  # only default arguments here
		gr.sync_block.__init__(
		self,
		name='Embedded Python Block',   # will show up in G
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

