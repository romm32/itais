"""
Bloque que imprime las dos entradas que recibe cinco veces.
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Bloque que imprime las dos entradas que recibe cinco veces."""

    def __init__(self, example_param=1.0):  
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',  
            in_sig=[np.float32, np.float32],
            out_sig=[]
        )

        self.example_param = example_param
        self.lim = 5

    def work(self, input_items, output_items):
        if self.lim > 0:
            print("in0 ", input_items[0][:])
            print("in1 ", input_items[1][:])
            self.lim = self.lim - 1
        return 2
