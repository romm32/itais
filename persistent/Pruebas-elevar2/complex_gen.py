"""
Bloque que genera como salida un complejo.
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  
    """Bloque que genera como salida un complejo."""

    def __init__(self, example_param=1.0): 
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block', 
            in_sig=[],
            out_sig=[np.complex64]
        )
        
        self.example_param = example_param

    def work(self, input_items, output_items):
        output_items[0][:] = 3 + 5j 
        return 1 
