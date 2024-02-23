"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
from datetime import datetime, timedelta

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        self.portName = 'msg_out'
        self.message_port_register_out(pmt.intern(self.portName))
        self.counter = 0
        self.lim = 10
        self.current_slot = -1
        self.slots_per_minute = 2250

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = time_elapsed.total_seconds() * 1000
        self.current_slot = int((milliseconds_elapsed)*self.slots_per_minute/60000) #Cantidad de slots desde que empezó el minuto.
        
        if int(time_elapsed.total_seconds())%5 == 0:
            self.counter = self.counter + 1
            PMT_msg = pmt.to_pmt(np.full(2, self.counter).tolist())
            self.message_port_pub(pmt.intern(self.portName), PMT_msg)
            print("enviado ", self.counter, time_elapsed.total_seconds())
        
        output_items[0][:] = input_items[0] * 2
        
        return len(output_items[0])
