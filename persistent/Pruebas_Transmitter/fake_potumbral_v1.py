"""
Bloque que simula el comportamiento de potumbral para probar el bloque transmitter.
En este bloque se reciben los 10 slots candidatos y se envía que se puede transmitir en el
sexto slot de esos candidatos. 
"""

import numpy as np
from gnuradio import gr
from datetime import datetime, timedelta


class blk(gr.sync_block):  

    def __init__(self, example_param=1.0):  
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   
            in_sig=[(np.complex64,10)],
            out_sig=[(np.complex64,2)]
        )

        self.example_param = example_param
        self.lim = 20
        self.arr = np.full(10, -1)
        self.aux = []
        self.arreglo = [-1, 0]
        self.unavez = True
        self.current_slot = -10
        self.slots_per_minute = 2250
        self.slot = -1
        self.once = True

    def work(self, input_items, output_items):
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = time_elapsed.total_seconds() * 1000
        self.current_slot = int((milliseconds_elapsed)*self.slots_per_minute/60000) #Cantidad de slots desde que empezó el minuto.
        
        self.arr = np.real(input_items[0][0])
        
        if (np.all(self.arr != -1)) and self.unavez:
            self.aux = self.arr
            self.slot = self.current_slot
            self.unavez = False
        
        if (np.all(self.arr != -1)) and self.current_slot == self.arr[5]: # and self.lim > 0:
            self.slot = self.arr[5]
            self.arreglo = [self.slot, 1]
            output_items[0][:] = self.arreglo
            self.once = False
            print("mando medidas A")
            
        if self.current_slot > self.slot+500:
            #self.lim = 20
            self.unavez = True
            #self.once = True
            self.slot = self.current_slot
            self.arreglo = [-1, 0]
            output_items[0][:] = self.arreglo 


        output_items[0][:] = self.arreglo

        return len(output_items)
        
        
