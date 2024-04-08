"""
Bloque que recibe un arreglo de dimensión 10.
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block): 

    def __init__(self, example_param=1.0):  
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',  
            in_sig=[(np.complex64,10)],
            out_sig=[np.complex64]
        )

        self.example_param = example_param
        self.lim = 5
        self.arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def work(self, input_items, output_items):
        output_items = input_items[0]
        for i in range(2):
        	self.arr = np.real(input_items[0][0])

        if self.lim > 0:
        	print("sub: ", self.arr)
        	self.lim = self.lim - 1
        	
        return len(output_items)
        
        
        
        
