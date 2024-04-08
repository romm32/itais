"""
Bloque que calcula la potencia de las muestras de entrada de forma análoga a Potumbral
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  
    """Bloque que calcula la potencia de las muestras de entrada de forma análoga a Potumbral"""

    def __init__(self, example_param=1.0): 
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block', 
            in_sig=[np.complex64],
            out_sig=[np.float32]
        )
        
        self.example_param = example_param

    def work(self, input_items, output_items):
        output_items[0][:] = np.abs(input_items[0])**2
        return len(output_items[0])
