"""
Bloque que recibe un valor en un puerto de mensaje y lo imprime.
"""

import numpy as np
from gnuradio import gr
import pmt
from datetime import datetime, timedelta
import time

class blk(gr.sync_block):  

    def __init__(self, example_param=1.0): 
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',  
            in_sig=[np.float32],
            out_sig=[np.float32]
        )

        self.example_param = example_param
        self.portName = 'msg_in'
        self.message_port_register_in(pmt.intern(self.portName))
        self.set_msg_handler(pmt.intern("msg_in"), self.process_message)
        self.lim = 10
        self.time_elapsed = -1
        self.variable = [-1, -1]
        
    def process_message(self, message):
        self.variable = pmt.to_python(message)
        print("llego ", self.variable, self.time_elapsed.total_seconds())

    def work(self, input_items, output_items):
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        self.time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = self.time_elapsed.total_seconds() * 1000
        
        output_items[0][:] = input_items[0] * 2
        
        return len(output_items[0])
