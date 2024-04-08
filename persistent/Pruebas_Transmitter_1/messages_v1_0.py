"""
Versión antigua del bloque messages. Espera recibir un flujo de enteros en su entrada desde transmitter.
Esta versión no cuneta con salida porque se planeaba utilizar sockets para su comunicación.
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  
    def __init__(self, example_param=1.0): 
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',  
            in_sig=[np.float32],
            out_sig=[]
        )
        
        self.example_param = example_param
        self.lim = 6000
        self.primera18 = True
        self.primera240 = True
        self.primera241 = True

    def work(self, input_items, output_items):
        if (18 in input_items[0] or 240 in input_items[0] or 241 in input_items[0]) and self.lim >0:
            if 18 in input_items[0] and self.primera18:
                print("llego 18")
                self.primera18 = False
            elif 240 in input_items[0] and self.primera240:
                print("llego 240")
                self.primera240 = False
            
            elif 241 in input_items[0] and self.primera241:
                print("llego 241")
                self.primera241 = False
            self.lim -= 1
            
        if self.lim == 0:
            self.lim = 3000
            self.primera18 = True
            self.primera240 = True
            self.primera241 = True

        return 2
        
        
        
        
        
        
        
