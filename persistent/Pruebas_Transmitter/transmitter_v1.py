"""
Primera versión del bloque transmitter. Recibe un arrgelo de 2 posiciones que indica si
se puede transmitir o no en el slot considerado (slot que debía estar dentro de los 
candidatos). También recibe un entero que será la velocidad medida por el GPS. Según esta 
velocidad se fijará el siguiente slot donde transmitir. 
En este bloque se envían los 10 slots candidatos como arreglo. Ese arreglo lo recibía 
Potumbral. También se enviaba un entero a messages con el tipo de mensaje que debía
enviarse.
"""

import numpy as np
from gnuradio import gr
import time
from datetime import datetime, timedelta


class blk(gr.sync_block):

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Transmitter',
            in_sig=[(np.complex64,2), np.float32],
            out_sig=[(np.complex64,10), np.float32]
        )
        self.inicio_18 = 0
        self.inicio_24 = 0
        self.slot_y_puedo = np.zeros(2)
        self.inicializando = True
        self.slots_per_minute = 2250
        self.transmitiendo = [False, False]
        self.mensaje24_a_transmitir = "A"
        self.primero_en_pedir = 0
        self.prox_18 = -1
        self.prox_24 = -1
        self.mensaje = 0
        self.current_slot = -1
        self.candidatos_18 = np.full(10, -1)
        self.candidatos_24 = np.full(10, -1)
        self.candidatos = np.full(10, -1)
        self.diff = 400
        self.es_menor0 = False
        self.ultimo_slot = -1
        self.cambio = False

    def slot_selection(self, NTT):
        selected = np.random.randint(NTT-187, NTT+187+1, size=10)
        selected = np.array(sorted(selected))
        if NTT-187 < 0:
            shift = 2250
            selected = (selected+shift)%2250
        elif NTT+187 > 2250:
            selected = selected%2250
        return(selected)
    
    def work(self, input_items, output_items):
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
            self.inicio_24 = self.current_slot
            self.ultimo_slot = self.current_slot
            
            print("inicializo")
            print("empiezan temporizadores")
            print("slot ", self.current_slot)
            
            if input_items[1][0] > 2:
                self.prox_18 = (self.inicio_18 + 1125)%2250 # transmito cada 30 seg
            else:
                self.prox_18 = (self.inicio_18 + 2250*2) # transmito cada 3 min, ver abajo explicacion de por que solo sumo 2 mins
            print("fijo prox 18", self.prox_18, "ahora es ", self.current_slot)
            
            
            if self.mensaje24_a_transmitir == "A":
                self.prox_24 = (self.inicio_24 + 2250*5) ### esto se transmite cada 6 minutos. lo que pasa es que nosotros
                                                         ### vamos restando en cada minuto que pasa. despues de que pasen 5 minutos,
                                                         ### va a ser necesario otro minuto entero para transmitir, asi que esto esta
                                                         ### bien asi
                print("fijo prox 240", self.prox_24, "ahora es ", self.current_slot)                                           
            else:
                self.prox_24 = (self.inicio_24) #  + 2250) ### nosotros vamos restando de a 2250 slots. si ahora ponemos inicio+2250,
                                                        ### indicando que tenemos que transmitir en un minuto, cuando pase el minuto
                                                        ### voy a restar 2250, pero espero otro minuto entero para transmitir, y esto esta
                                                        ### mal. por eso solo inicio_24 (ese slot, pero del siguiente minuto)
                print("fijo prox 241", self.prox_24, "ahora es ", self.current_slot)
            
            self.mensaje = 0
            output_items[1][:] = self.mensaje
        
        else:
            current_utc_time = datetime.utcnow()
            start_of_minute = current_utc_time.replace(second=0, microsecond=0)
            time_elapsed = current_utc_time - start_of_minute
            milliseconds_elapsed = time_elapsed.total_seconds() * 1000
            self.current_slot = int((milliseconds_elapsed)*self.slots_per_minute/60000) #Cantidad de slots desde que empezó el minuto.
            
            if self.current_slot != self.ultimo_slot:
                self.ultimo_slot = self.current_slot
                self.cambio = True
            
            self.mensaje = 0 ## no estoy pidiendo ningun mensaje a messages ahora
            output_items[1][:] = self.mensaje
            
            if self.prox_18 >= 2250 and self.current_slot == (self.prox_18%2250) and self.cambio:
                self.prox_18 = self.prox_18 - 2250
                print("queda un minuto menos 18")
                 
            elif (not self.transmitiendo[0]): ### en un elif porque sino podría ser que resto 2250 y después se hacen cosas con el número resultante.
                
                if self.current_slot == ((self.prox_18-self.diff)%2250): ### and (self.current_slot != self.inicio_18):
                ### ver que esto si no podemos analizar todos los slots, es un problema. porque capaz nunca miro el slot prox_18-diff
                
                    if self.prox_18-self.diff < 0:
                        self.es_menor0 = True
                    if self.es_menor0 or (self.current_slot == self.prox_18-self.diff):
                        self.candidatos_18 = self.slot_selection(self.prox_18) #[self.prox_18-5,self.prox_18-4,self.prox_18-3,self.prox_18-2,self.prox_18-1, self.prox_18,self.prox_18+1,self.prox_18+2,self.prox_18+3,self.prox_18+4]#
                        self.transmitiendo[0] = True
                        print("transmitiendo 18", self.current_slot)
                        if self.primero_en_pedir == 0:
                            self.primero_en_pedir = 18
                            
                        self.candidatos = self.candidatos_18
                        output_items[0][:] = self.candidatos
                        self.es_menor0 = False

            if self.prox_24 >= 2250 and self.current_slot == (self.prox_24%2250) and self.cambio:
                self.prox_24 = self.prox_24 - 2250       
                print("queda un minuto menos 24") 

            elif not self.transmitiendo[1]:
                        
                if self.current_slot == (self.prox_24-self.diff)%2250: ### and (self.current_slot != self.inicio_24): ### ver segunda condicion
                    if self.prox_24-self.diff < 0:
                        self.es_menor0 = True
                    if self.es_menor0 or (self.current_slot == self.prox_24-self.diff):
                        self.candidatos_24 = self.slot_selection(self.prox_24) #[self.prox_24-5,self.prox_24-4,self.prox_24-3,self.prox_24-2,self.prox_24-1, self.prox_24,self.prox_24+1,self.prox_24+2,self.prox_24+3,self.prox_24+4] #
                        self.transmitiendo[1] = True
                        print("transmitiendo 24", self.current_slot)
                        if self.primero_en_pedir == 0:
                            self.primero_en_pedir = 24
                        
                        self.candidatos = self.candidatos_24
                        output_items[0][:] = self.candidatos
                        self.es_menor0 = False
                        
            
            if self.transmitiendo[0] and (np.real(self.slot_y_puedo[0]) in self.candidatos_18) and (np.real(self.slot_y_puedo[1]) == 1) and ((not self.slot_y_puedo[0] in self.candidatos_24) or (self.primero_en_pedir == 18)) and self.current_slot == self.slot_y_puedo[0]:
                
                self.mensaje = 18 ### mensaje a mandar a messages
                output_items[1][:] = self.mensaje
                self.transmitiendo[0] = False
                if self.transmitiendo[1]:
                    self.primero_en_pedir = 24
                else:
                    self.primero_en_pedir = 0
                   
                self.inicio_18 = np.real(self.slot_y_puedo[0]) ### que deberia ser igual a current_slot
                    
                if input_items[1][0] > 2: #### verificar en qué unidad nos da la velocidad el gps
                    self.prox_18 = (self.inicio_18 + 1125)%2250 # transmito cada 30 seg
                else:
                    self.prox_18 = (self.inicio_18 + 2250*2) # transmito cada 3 min    ### ver mod 2250
                print("fijo prox ", self.prox_18, "ahora es ", self.current_slot)
                    
                self.candidatos_18 = np.full(10, -1)
                    
                print("reinicia 30s", self.current_slot)
                #print("slot ", self.current_slot)
                #print("slot y puedo", self.slot_y_puedo[0])
                
                self.slot_y_puedo = np.zeros(2)
                    
                self.candidatos = np.full(10, -1)
                output_items[0][:] = self.candidatos
                    
                    
                
                        
            if self.transmitiendo[1] and (self.slot_y_puedo[0] in self.candidatos_24) and np.real(self.slot_y_puedo[1]) == 1 and (not (self.slot_y_puedo[0] in self.candidatos_18) or (self.primero_en_pedir == 24)) and self.current_slot == self.slot_y_puedo[0]:
                
                if self.mensaje24_a_transmitir == "A":
                    self.mensaje = 240 ### mensaje a mandar a messages, es el 24-0 que indica 24-A
                    output_items[1][:] = self.mensaje
                    self.mensaje24_a_transmitir = "B"
                        
                    print("Envio mensaje 24 A")
                    print("slot ", self.current_slot)
                else:
                    self.mensaje = 241 ### mensaje a mandar a messages, es el 24-1 que indica 24-B
                    output_items[1][:] = self.mensaje
                    self.mensaje24_a_transmitir = "A"
                        
                    print("Envio mensaje 24 B")
                    print("slot ", self.current_slot)
                self.transmitiendo[1] = False
                    
                if self.transmitiendo[0]:
                    self.primero_en_pedir = 18
                else:
                    self.primero_en_pedir = 0
                self.inicio_24 = np.real(self.slot_y_puedo[0]) ### que deberia ser igual a current_slot
                    
                if self.mensaje24_a_transmitir == "A":
                    self.prox_24 = (self.inicio_24 + 2250*5) ### ver modulo
                else:
                    self.prox_24 = (self.inicio_24)
                    
                self.candidatos_24 = np.full(10, -1)
                    
                self.candidatos = np.full(10, -1)
                output_items[0][:] = self.candidatos
                    
        
            self.cambio = False
        output_items[0][:] = self.candidatos
        output_items[1][:] = self.mensaje
        return len(output_items[0])
        
        

