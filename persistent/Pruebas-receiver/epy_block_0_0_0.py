"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from datetime import datetime, timedelta
import zmq

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[(np.float32)],
            out_sig=[(np.float32)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        self.lim = 5
        self.arr = 0
        self.dict = {"slot": 3, "puedo": 3}
        self.slots_per_minute = 2250
        self.unavez = True
        
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.setsockopt(zmq.RECONNECT_IVL, 1000)
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        socket.connect("tcp://127.0.0.1:5600")  # Connect to the same port as in your GNU Radio script

    def work(self, input_items, output_items):
    
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = time_elapsed.total_seconds() * 1000
        slot_index = (milliseconds_elapsed)*self.slots_per_minute/60000 #Cantidad de slots desde que empezó el minuto.
        
        msj = socket.recv_string()
        
        if self.unavez:
            print("recibio")
            self.unavez = False
        data_dict = eval(msj)
        
        self.arr = data_dict["slot"]
        if int(slot_index)%100 == 0:
            print(self.arr, int(slot_index))
        
        output_items[0][0] = self.arr
        
        return 2
