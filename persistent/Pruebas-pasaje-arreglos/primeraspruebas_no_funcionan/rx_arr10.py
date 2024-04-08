"""
Bloque que recibe arreglos de 10 dimensiones y verifica que le llegó el arreglo esperado.
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  
    def __init__(self, example_param=1.0): 
    	
    	gr.sync_block.__init__(
        self,
        name='Embedded Python Block',  
        in_sig=[(np.float32, 10)],
        out_sig=[]
    )
    	self.example_param = example_param
    	self.limite = 10
    
    def work(self, input_items, output_items):
    	if all(input_items[0][0] == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]):
    		print("si")
    		self.limite = self.limite - 1
    	return len(input_items[0])
