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
        in_sig=[(np.float32, 10)],
        out_sig=[]
    )
    # if an attribute with the same name as a parameter is found,
    # a callback is registered (properties work, too).
    	self.example_param = example_param
    	self.limite = 10
    
    def work(self, input_items, output_items):
    	if all(input_items[0][0] == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]):
    		print("si")
    		self.limite = self.limite - 1
    	return len(input_items[0])
