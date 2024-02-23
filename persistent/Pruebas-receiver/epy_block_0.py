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
import time

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
        self.portName = 'msg_in'
        self.message_port_register_in(pmt.intern(self.portName))
        self.set_msg_handler(pmt.intern("msg_in"), self.process_message)
        self.lim = 10
        self.time_elapsed = -1
        self.variable = [-1, -1]
        
    def process_message(self, message):
        # Retrieve message payload and save it to a variable
        self.variable = pmt.to_python(message)
        print("llego ", self.variable, self.time_elapsed.total_seconds())

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        self.time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = self.time_elapsed.total_seconds() * 1000
        
        #if int(self.time_elapsed.total_seconds())%5 == 0:
        #    print(self.variable, self.time_elapsed.total_seconds())
        #    time.sleep(0.5)
        
        output_items[0][:] = input_items[0] * 2
        
        return len(output_items[0])
