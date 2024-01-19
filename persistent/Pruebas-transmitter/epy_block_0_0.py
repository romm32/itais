"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import time
from datetime import datetime, timedelta


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Transmitter',   # will show up in GRC
            in_sig=[(np.complex64,2), (np.complex64,2), np.float32],
            out_sig=[(np.complex64,10), (np.complex64,10), np.float32]
        )
        self.inicio_18 = 0
        self.inicio_24 = 0
        self.slot_y_puedo = np.zeros(2)
        self.inicializando = True
        self.slots_per_minute = 2250
        self.transmitiendo = [False, False]
        self.mensaje24_a_transmitir = "A"
        self.primero_en_pedir = 0
        self.ultimo_canal = "B"
        self.prox_18 = -1
        self.prox_24 = -1
        self.mensaje = 0
        self.current_slot = -1
        self.candidatos_18 = np.full(10, -1)
        self.candidatos_24 = np.full(10, -1)
        self.candidatos_A = np.full(10, -1)
        self.candidatos_B = np.full(10, -1)
        self.diff = 400
        self.es_menor0 = False
        self.ultimo_slot = -1

    def slot_selection(NTT):
        selected = np.random.randint(NTT-187, NTT+187+1, size=10)
        selected = np.array(sorted(selected))
        if NTT-187 < 0:
            shift = 2250
            selected = (selected+shift)%2250
        elif NTT+187 > 2250:
            selected = selected%2250
        return(selected)
    
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        if self.ultimo_canal == "A": #Si el ultimo canal fue el A, vamos a transmitir en el B y tomamos la segunda entrada
            self.slot_y_puedo = input_items[1][0]
        else: #Si el ultimo canal fue el B, vamos a transmitir en el A y tomamos la primera entrada
            self.slot_y_puedo = input_items[0][0]
        if self.inicializando:
            print("inicializando")
            time.sleep(60)
            self.inicializando = False
            
            current_utc_time = datetime.utcnow()
            start_of_minute = current_utc_time.replace(second=0, microsecond=0)
            time_elapsed = current_utc_time - start_of_minute
            milliseconds_elapsed = time_elapsed.total_seconds() * 1000
            self.current_slot = int((milliseconds_elapsed)*self.slots_per_minute/60000) #Cantidad de slots desde que empezó el minuto.
            
            self.inicio_18 = self.current_slot
            self.inicio_24 = self.current_slot+10
            
            print("inicializo")
            print("empiezan temporizadores")
            print("slot ", self.current_slot)
            
            if input_items[2][0] > 2: #### verificar en qué unidad nos da la velocidad el gps
                self.prox_18 = (self.inicio_18 + 1125)%2250 # transmito cada 30 seg
            else:
                self.prox_18 = (self.inicio_18 + 2250*3) # transmito cada 3 min    ### ver mod 2250
            print("fijo prox ", self.prox_18, "ahora estoy ", self.current_slot)
            
            
            if self.mensaje24_a_transmitir == "A":
                self.prox_24 = (self.inicio_24 + 2250*5) ### ver modulo
            else:
                self.prox_24 = (self.inicio_24 + 2250)
            
            self.mensaje = 0
            output_items[2][:] = self.mensaje
        
        else:
            current_utc_time = datetime.utcnow()
            start_of_minute = current_utc_time.replace(second=0, microsecond=0)
            time_elapsed = current_utc_time - start_of_minute
            milliseconds_elapsed = time_elapsed.total_seconds() * 1000
            self.current_slot = int((milliseconds_elapsed)*self.slots_per_minute/60000) #Cantidad de slots desde que empezó el minuto.
            
            if not self.transmitiendo[0] and not self.transmitiendo[1]:
                self.mensaje = 0 ## no estoy pidiendo ningun mensaje a messages ahora
                output_items[2][:] = self.mensaje
                
                if self.current_slot == ((self.prox_18-self.diff)%2250) and (self.current_slot != self.inicio_18):
                    if self.prox_18-self.diff < 0:
                        self.es_menor0 = True
                    if self.es_menor0 or (self.current_slot == self.prox_18-self.diff):
                        self.candidatos_18 = [self.prox_18-5,self.prox_18-4,self.prox_18-3,self.prox_18-2,self.prox_18-1, self.prox_18,self.prox_18+1,self.prox_18+2,self.prox_18+3,self.prox_18+4]#slot_selection(self.prox_18)
                        self.transmitiendo[0] = True
                        print("transm 18", self.current_slot)
                        if self.primero_en_pedir == 0:
                            self.primero_en_pedir = 18
                            
                        if self.ultimo_canal == "B":
                            self.candidatos_A = self.candidatos_18
                            output_items[0][:] = self.candidatos_A
                        else:
                            self.candidatos_B = self.candidatos_18
                            output_items[1][:] = self.candidatos_B
                            
                    else:
                        self.prox_18 = self.prox_18 - 2250 # queda un minuto menos
                        
                if self.current_slot == ((self.prox_24-self.diff)%2250) and (self.current_slot != self.inicio_24):
                    if self.prox_24-self.diff < 0:
                        self.es_menor0 = True
                    if self.es_menor0 or (self.current_slot == self.prox_24-self.diff):
                        self.candidatos_24 = [self.prox_24-5,self.prox_24-4,self.prox_24-3,self.prox_24-2,self.prox_24-1, self.prox_24,self.prox_24+1,self.prox_24+2,self.prox_24+3,self.prox_24+4] #slot_selection(self.prox_24)
                        self.transmitiendo[1] = True
                        if self.primero_en_pedir == 0:
                            self.primero_en_pedir = 24
                            
                        if self.ultimo_canal == "B":
                            self.candidatos_A = self.candidatos_24
                            output_items[0][:] = self.candidatos_A
                        else:
                            self.candidatos_B = self.candidatos_24
                            output_items[1][:] = self.candidatos_B
                            
                    else:
                        self.prox_24 = self.prox_24 - 2250 # queda un minuto menos
                        
            else:
                if self.transmitiendo[0] and (np.real(self.slot_y_puedo[1]) == 1) and (np.real(self.slot_y_puedo[0]) in self.candidatos_18) and ((not self.slot_y_puedo[0] in self.candidatos_24) or (self.primero_en_pedir == 18)) and self.current_slot == self.slot_y_puedo[0]:
                
                    self.mensaje = 18 ### mensaje a mandar a messages
                    output_items[2][:] = self.mensaje
                    self.transmitiendo[0] = False
                    if self.transmitiendo[1]:
                        self.primero_en_pedir = 24
                    else:
                        self.primero_en_pedir = 0
                    self.inicio_18 = np.real(self.slot_y_puedo[0]) ### que deberia ser igual a current_slot
                    if input_items[2][0] > 2: #### verificar en qué unidad nos da la velocidad el gps
                        self.prox_18 = (self.inicio_18 + 1125)%2250 # transmito cada 30 seg
                    else:
                        self.prox_18 = (self.inicio_18 + 2250*3) # transmito cada 3 min    ### ver mod 2250
                    print("fijo prox ", self.prox_18, "ahora estoy ", self.current_slot)
                    
                    self.candidatos_18 = np.full(10, -1)
                    self.es_menor0 = False
                    
                    print(self.ultimo_canal, " reinicia 30s", self.current_slot)
                    #print("slot ", self.current_slot)
                    #print("slot y puedo", self.slot_y_puedo[0])
                    
                    self.slot_y_puedo = np.zeros(2)
                    
                    if self.ultimo_canal == "B": # si el ultimo canal era B, transmiti en A recien, entonces limpio esas variables y actualizo el ultimo canal
                        self.candidatos_A = np.full(10, -1)
                        output_items[0][:] = self.candidatos_A
                        self.ultimo_canal = "A"
                    else:
                        self.candidatos_B = np.full(10, -1)
                        output_items[1][:] = self.candidatos_B
                        self.ultimo_canal = "B"
                        
                elif self.transmitiendo[1] and self.slot_y_puedo[1] == 1 and (self.slot_y_puedo[0] in self.candidatos_24) and (not (self.slot_y_puedo[0] in self.candidatos_18) or (self.primero_en_pedir == 24)):
                
                    if self.mensaje24_a_transmitir == "A":
                        self.mensaje = 240 ### mensaje a mandar a messages, es el 24-0 que indica 24-A
                        output_items[2][:] = self.mensaje
                        self.mensaje24_a_transmitir = "B"
                        self.es_menor0 = False
                        print("Envio mensaje 24 A")
                        print("slot ", self.current_slot)
                    else:
                        self.mensaje = 241 ### mensaje a mandar a messages, es el 24-1 que indica 24-B
                        output_items[2][:] = self.mensaje
                        self.mensaje24_a_transmitir = "A"
                        self.es_menor0 = False
                        print("Envio mensaje 24 B")
                        print("slot ", self.current_slot)
                    self.transmitiendo[1] = False
                    self.prox_fijo24 = False
                    if self.transmitiendo[0]:
                        self.primero_en_pedir = 18
                    else:
                        self.primero_en_pedir = 0
                    self.inicio_24 = np.real(self.slot_y_puedo[0]) ### que deberia ser igual a current_slot
                    
                    if self.mensaje24_a_transmitir == "A":
                        self.prox_24 = (self.inicio_24 + 2250*5) ### ver modulo
                    else:
                        self.prox_24 = (self.inicio_24 + 2250)
                    
                    self.candidatos_24 = np.full(10, -1)
                    
                    if self.ultimo_canal == "B":
                        self.candidatos_A = np.full(10, -1)
                        output_items[0][:] = self.candidatos_A
                        self.ultimo_canal = "A"
                    else:
                        self.candidatos_B = np.full(10, -1)
                        output_items[1][:] = self.candidatos_B
                        self.ultimo_canal = "B"
                        
        output_items[0][:] = self.candidatos_A
        output_items[1][:] = self.candidatos_B
        output_items[2][:] = self.mensaje
        return len(output_items[0])
        
        

