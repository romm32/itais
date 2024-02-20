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
            in_sig=[np.float32],
            out_sig=[(np.complex64,10)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.NTT = 700
        self.candidatos = np.full(10, -1)
        self.slot_y_puedo = [2, 2]
        self.current_slot = -1
        self.slots_per_minute = 2250
        self.inicios = 500
        self.cambio = False
        self.ultimo_slot = -1
        self.primeravez = True
        self.ultimavez = True
        self.s_y_p_numero = 0

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = time_elapsed.total_seconds() * 1000
        self.current_slot = int((milliseconds_elapsed)*self.slots_per_minute/60000) #Cantidad de slots desde que empezó el minuto.
        
        self.s_y_p_numero = int(input_items[0][0])

        if len(str(self.s_y_p_numero)) != 1:
            self.slot_y_puedo[0] = int(str(self.s_y_p_numero)[0:len(str(self.s_y_p_numero))-1])
        else:
            self.slot_y_puedo[0] = 0
        self.slot_y_puedo[1] = int(str(self.s_y_p_numero)[-1]) # slot y puedo
        
        if self.current_slot != self.ultimo_slot:
            self.ultimo_slot = self.current_slot
            self.cambio = True
            #print(input_items[0][0])
            #print("s_y_p", self.slot_y_puedo)
            if self.current_slot in self.candidatos and self.slot_y_puedo[0] == self.current_slot:
                print("s_y_p", self.slot_y_puedo)
                #print(np.count_nonzero(self.slot_y_puedo[0]))
                

        if self.slot_y_puedo[1] == 1 and self.slot_y_puedo[0] in self.candidatos and self.cambio:
            print(self.slot_y_puedo, "A")
        
        elif self.slot_y_puedo[1] == 3 and self.primeravez:
            print("inicializando")
            self.primeravez = False
        elif self.slot_y_puedo[1] != 3 and self.ultimavez:
            print("inicializo")
            self.ultimavez = False
        
        if (self.current_slot - self.inicios)%2250 <= 200:
            self.NTT = self.inicios
            self.inicios = (self.inicios + 1125)%2250 
            self.candidatos = np.array(sorted(np.random.randint(self.NTT-187, self.NTT+187+1, size=10)))
            print(self.candidatos, "A")

            
        self.cambio = False
        output_items[0][:] = self.candidatos
        

        return 16
        
 
