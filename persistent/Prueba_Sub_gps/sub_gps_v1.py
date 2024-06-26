"""
Bloque de prueba de Sub_GPS
"""

import numpy as np
from gnuradio import gr
import zmq

class sub_gps(gr.sync_block):

    def __init__(self):
        
        gr.sync_block.__init__(
            self,
            name='SUBGPS', 
            in_sig=[],
            out_sig=[(np.float32, 4), np.float32]
        )
        self.lim = 10
        self.arr = [0, 0, 0, 0]

    def work(self, input_items, output_items):
    	
    	context = zmq.Context()
    	subscriber = context.socket(zmq.SUB)
    	subscriber.connect("tcp://127.0.0.1:5600") 
    	subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
    	
    	msj = subscriber.recv_string()
    	data_dict = eval(msj)
    	
    	self.arr[0] = data_dict["long"]
    	self.arr[1] = data_dict["lat"]
    	self.arr[2] = data_dict["sog"]
    	self.arr[3] = data_dict["cog"]
    	
    	output_items[0][:] = self.arr
    	output_items[1][:] = data_dict["sog"]
    	
    	if self.lim > 0:
    		print("out0: ", output_items[0][:])
    		print("out1: ", output_items[1][:])
    		self.lim = self.lim-1
    		
    	return 100
