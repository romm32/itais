"""
Bloque utilizado para verificar el comportamiento de Potumbral. Aquí se envian arreglos de
dimensión 2 para comprobar la comunicación con arreglos de dos dimensiones. 
Este comportamiento se pretendía utilizar en Potumbral para mandar el slot y si es posible
transmitir en él.
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  

    def __init__(self, example_param=1.0): 
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',  
            in_sig=[],
            out_sig=[(np.complex64, 2)]
        )
        
        self.example_param = example_param
        self.lim = 5
        self.arr = [1, 2]

    def work(self, input_items, output_items):
        
        output_items[0][:] = self.arr
        if self.lim > 0:
                print("pub: ", self.arr)
                self.lim = self.lim-1
        return 2
