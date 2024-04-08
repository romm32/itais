"""
Bloque que imita el funcionamiento de una versión inicial de Transmitter.
"""

import numpy as np
from gnuradio import gr
from datetime import datetime, timedelta


class blk(gr.sync_block): 

    def __init__(self, example_param=1.0):
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',  
            in_sig=[(np.float32, 2)],
            out_sig=[(np.complex64,10)]
        )

        self.NTT = 700
        self.candidatos = np.full(10, -1)
        self.slot_y_puedo = np.zeros(10) #[2, 2]
        self.current_slot = -1
        self.slots_per_minute = 2250
        self.inicios = 500
        self.cambio = False
        self.ultimo_slot = -1
        self.primeravez = True
        self.ultimavez = True
        self.s_y_p_numero = 0

    def work(self, input_items, output_items):
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = time_elapsed.total_seconds() * 1000
        self.current_slot = int((milliseconds_elapsed)*self.slots_per_minute/60000) # Cantidad de slots desde que empezó el minuto.
        
        self.slot_y_puedo = input_items[0][0]
        
        if self.current_slot != self.ultimo_slot:
            self.ultimo_slot = self.current_slot
            self.cambio = True
            #print(input_items[0])
            #print("s_y_p", self.slot_y_puedo)
            if self.current_slot in self.candidatos:
                print("B", self.current_slot, input_items[0])

        if self.slot_y_puedo[1] == 1 and self.slot_y_puedo[0] in self.candidatos and self.cambio:
            print(self.slot_y_puedo, "B")
        
        elif self.slot_y_puedo[1] == 3 and self.primeravez:
            print("inicializando")
            self.primeravez = False
        elif self.slot_y_puedo[1] != 3 and self.ultimavez:
            print("inicializo")
            self.ultimavez = False
        
        if (self.inicios - self.current_slot)%2250 <= 200:
            self.NTT = self.inicios
            self.inicios = (self.inicios + 1125)%2250 
            self.candidatos = np.array(sorted(np.random.randint(self.NTT-187, self.NTT+187+1, size=10)))
            print(self.candidatos, "B", self.current_slot)

            
        self.cambio = False
        output_items[0][:] = self.candidatos
        

        return 16
        
 
