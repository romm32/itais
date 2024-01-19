"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from datetime import datetime, timedelta


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[(np.complex64,10)],
            out_sig=[(np.complex64,2)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        self.lim = 20
        self.arr = np.full(10, -1)
        self.aux = []
        self.arreglo = [-1, 0]
        self.unavez = True
        self.current_slot = -10
        self.slots_per_minute = 2250
        self.slot = -1
        self.once = True

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = time_elapsed.total_seconds() * 1000
        self.current_slot = int((milliseconds_elapsed)*self.slots_per_minute/60000) #Cantidad de slots desde que empezó el minuto.
        
        self.arr = np.real(input_items[0][0])
        
        if np.sum(self.arr) != -10 and self.unavez:
            self.aux = self.arr
            self.slot = self.current_slot
            self.unavez = False
            print("recibi candidatos en ", self.current_slot)
        
        else:
            if np.sum(self.arr) != -10 and self.current_slot in self.aux and self.once: # and self.lim > 0:
            	self.slot = self.current_slot
            	self.arreglo = [self.slot, 1]
            	output_items[0][:] = self.arreglo
            	#self.lim -= 1
            	self.once = False
        if self.current_slot > self.slot+500:
            #self.lim = 20
            self.unavez = True
            self.once = True
            self.arreglo = [-1, 0]
            output_items[0][:] = self.arreglo
                #print("slot y puedo A ", self.arreglo) 
                


        output_items[0][:] = self.arreglo

        return len(output_items)
        
        
        
