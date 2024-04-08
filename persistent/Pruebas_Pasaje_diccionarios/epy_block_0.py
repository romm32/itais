"""
Bloque que se subscribe a un socket TCP desde el cual se recibirá información GPS.
"""

import numpy as np
from gnuradio import gr
import zmq

class blk(gr.sync_block):  

    def __init__(self, example_param=1.0): 
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',
            out_sig=[np.complex64]
        )

        self.example_param = example_param

    def work(self, input_items, output_items):
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.connect("tcp://127.0.0.1:5600")  
        subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
        msj = subscriber.recv_string()
        print(msj)
        
        return 100
