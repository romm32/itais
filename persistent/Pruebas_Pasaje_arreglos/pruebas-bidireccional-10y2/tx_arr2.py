"""
Bloque que genera y envía un arreglo de dimensión 2.
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self, example_param=1.0):  
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   
            in_sig=[],
            out_sig=[(np.float32, 2)]
        )
        
        self.example_param = example_param
        self.lim = 5
        self.arr = np.full(2, 33)

    def work(self, input_items, output_items):
        output_items[0][0] = self.arr
        if self.lim > 0:
                print("pub: ", self.arr)
                print(output_items)
                self.lim = self.lim-1
        return 2
