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
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        self.arr_pow_actual = np.full(50, 2e-14)
        self.power = 2e-7
        self.prommovil = 0

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        #print(f"se recibieron {len(input_items[0])} muestras")
        for i in range(0, len(input_items[0])):
        	muestra_actual = input_items[0][i]
        	self.power = np.abs(muestra_actual)**2 
        	self.prommovil = self.prommovil*1000/1001+(1/1001)*self.power
        	#if i % 1000 == 0:
        	#	print(self.prommovil)
        	for i in range(len(self.arr_pow_actual) - 1, 0, -1): 
        		self.arr_pow_actual[i] = self.arr_pow_actual[i - 1]	
        		self.arr_pow_actual[0] = self.power
        		self.pow_actual = np.mean(self.arr_pow_actual)
        	#if i % 1000 == 0:
        #		print("potencia: ", self.pow_actual)
        #print("potencia: ", self.pow_actual)
        		
        output_items[0][:]= self.pow_actual
        return 5000
