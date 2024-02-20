"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        self.lim = 6000
        self.primera18 = True
        self.primera240 = True
        self.primera241 = True

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        if (18 in input_items[0] or 240 in input_items[0] or 241 in input_items[0]) and self.lim >0:
            if 18 in input_items[0] and self.primera18:
                print("llego 18")
                self.primera18 = False
            elif 240 in input_items[0] and self.primera240:
                print("llego 240")
                self.primera240 = False
            
            elif 241 in input_items[0] and self.primera241:
                print("llego 241")
                self.primera241 = False
            self.lim -= 1
            
        if self.lim == 0:
            self.lim = 3000
            self.primera18 = True
            self.primera240 = True
            self.primera241 = True

        return 2
        
        
        
        
        
        
        
