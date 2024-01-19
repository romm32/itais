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
            in_sig=[(np.complex64,10)],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        self.lim = 5
        self.arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items = input_items[0]
        for i in range(2):
        	self.arr = np.real(input_items[0][0])

        if self.lim > 0:
                print("sub: ", self.arr)
                self.lim = self.lim - 1

        return len(output_items)
