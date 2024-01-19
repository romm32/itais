"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import zmq
import struct
from datetime import datetime

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64, np.float32],
            out_sig=[np.complex64]
        )
        #context = zmq.Context() # no es posible definir el socket arriba del todo, y definirlo una sola vez. gnu radio no funciona.
        #socket = context.socket(zmq.PUB)
        #socket.bind("tcp://127.0.0.1:5580")
        
        self.topic = "valores_umbral_potencia"
        
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
        
        self.contador = 1
        self.inicio = 41
        self.final = 99
        self.cant_muestras_enviadas = 0
        
        self.rangoinf = False
        self.rangosup = False
        self.recibi = False

    def work(self, input_items, output_items):
    	in_buf = input_items[0]
    	out_buf = output_items[0]
    	
    	# subscriptor para cuando el transmisor avisa que necesita las muestras.
    	#context = zmq.Context()
    	#subscriber = context.socket(zmq.SUB)
    	#subscriber.connect("tcp://127.0.0.1:5590")  # Connect to the same port as in your GNU Radio script
    	#subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
    	
    	#msj = subscriber.recv_string()
    	#print("esperando mensaje")
    	msj = input_items[1][0]
    	msj = struct.unpack('!f', msj)[0]
    	#print("msg: ", msj)
    	if msj == 1:
    		self.recibi = True
    		#print("llego mensaje, enviando")
    		#print("len input items0:", len(input_items[0]))
    		#print("len input items1:", len(input_items[1]))
    	
    	
    	if self.recibi:
    		#print("recibi len input items0:", len(input_items[0]))
    		#print("recibi len input items1:", len(input_items[1]))
    	
    		context = zmq.Context()
    		socket = context.socket(zmq.PUB)
    		socket.bind("tcp://127.0.0.1:5580")

    		
    		for i in range(0, len(input_items[0])):
    			
    			if 41 <= self.contador and self.contador <= 99 and ((not self.rangoinf) or (not self.rangosup)):
    				if self.contador == 41:
    					self.rangoinf = True
    				if self.contador == 99:
    					self.rangosup = True
    				datos = {"num_muestra": self.contador, "umbral": in_buf[0], "potencia_actual": in_buf[0]*2}
    				message_info = f"{self.topic} {datos}"#.encode('utf-8')
    				socket.send_string(message_info)
    				self.cant_muestras_enviadas += 1
    				#print("enviada muestra: ", self.contador)
    			self.contador = self.contador + 1
    			if self.contador == 1356:
    				self.contador = 1
    				self.rangoinf = False
    				self.rangosup = False
    				self.recibi = False
    			if self.cant_muestras_enviadas >= 500 and self.cant_muestras_enviadas < 510:
    				if self.cant_muestras_enviadas == 500:
    					current_time = datetime.now()
    					formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    					print("rx llego a 500", formatted_time)
    					
	    	
	    		

	    	socket.close()
	    	context.term()
	    	#print("cerrando socket")
	    	
    	output_items[0][:] = input_items[0]
    	#self.set_output_multiple(100)
    	return 100
        
        
        
        
        
        
        
        
        
        
        
