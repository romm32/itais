"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        self.contador = 0
        self.inicio = 41
        self.final = 99

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        for i in range(0, len(input_items[0])):
        	self.contador = self.contador + 1
        	if self.inicio <= i and i <= self.final:
        		#tag_value = 42 
        		value = pmt.intern("42")
        		tag_offset = i
        		key = pmt.intern("sensando")
        		#tag_key =  "sensando"
        		self.add_item_tag(0, # Write to output port 0
                          tag_offset, # Index of the tag in absolute terms
                          key, # Key of the tag
                          value) # Value of the tag 
        	if self.contador == 1356:
        		self.contador = 0
        output_items[0][:] = input_items[0]
        return len(output_items[0])
