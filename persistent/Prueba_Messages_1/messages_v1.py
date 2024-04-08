"""
Primera versión del bloque "Messages". Es la que fue probada en esta prueba.
No es idéntica a la versión final. Se toma código del proyecto "gr-aistx".
"""

import numpy as np
from gnuradio import gr
import pmt
from datetime import datetime, timedelta

class blk(gr.sync_block): 
    """Primera versión del bloque "Messages"."""

    def __init__(self, vessel_length = 18, vessel_beam = 14, vessel_name = "ROMA", vessel_type = 30):  
        gr.sync_block.__init__(
            self,
            name='Messages',   
            in_sig=[np.float32, (np.float32, 5)],
            out_sig=[]
        )
        self.vessel_length = vessel_length
        self.vessel_beam = vessel_beam
        self.vessel_name = vessel_name
        self.vessel_type = vessel_type
        
        self.portName = 'bits_Out'
        self.message_port_register_out(pmt.intern(self.portName))
        
        self.message = -1
        
        self.speed = -1
        self.long = -1
        self.lat = -1
        self.course = -1
        self.ts = -1
        
        self.mmsi = 247320162 # Default. tiene que tener 9 dígitos
        self.payload = ""
        
        self.slots_per_minute = 2250
        self.slot_duration = 60/2250
        self.samples_per_slot = int(self.slot_duration*50000)
        
        self.primera18 = True
        self.primera240 = True
        self.primera241 = True
        
        self.slot_transmitido18 = -1
        self.slot_transmitido240 = -1
        self.slot_transmitido241 = -1
        
    def encode_string(self, string):
        vocabolary = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^- !\"#$%&'()*+,-./0123456789:;<=>?"
        encoded_string = ""
        for c in string.upper():
            index = vocabolary.find(c)
            encoded_string += '{0:b}'.format(index).rjust(6,'0')
        return encoded_string
   
    def compute_long_lat (self, __long, __lat):
        _long = '{0:b}'.format(int(round(__long*600000)) & 0b1111111111111111111111111111).rjust(28,'0')
        _lat =  '{0:b}'.format(int(round(__lat*600000))  & 0b111111111111111111111111111).rjust(27,'0')
        return (_long, _lat)
        
    def encode_18(self, __mmsi, __speed, __long, __lat, __course, __ts):
        _type = '{0:b}'.format(18).rjust(6,'0') 
        _repeat = "00"	
        _mmsi = '{0:b}'.format(__mmsi).rjust(30,'0') 
        _reserved = '0'*8
        _speed = '{0:b}'.format(int(round(__speed*10))).rjust(10,'0')	
        _accurancy = '0'
        
        (_long, _lat) = self.compute_long_lat(__long, __lat)
        
        _course = '{0:b}'.format(int(round(__course*10))).rjust(12,'0') 
        _true_heading = '1'*9
        _ts = '{0:b}'.format(__ts).rjust(6,'0') 
        
        _flags = '001000000'
        # '00': Regional reserved
        # '1':  CS mode (carrier sense Class B)
        # '0' Display flag
        # '0': DSC
        # '0': Band Flag
        # '0': M22 Flag
        # '0': Assigned 0 -> Autonomous mode
        # '0': Raim flag
        
        _rstatus = '11100000000000000110'
        
        return _type+_repeat+_mmsi+_reserved+_speed+_accurancy+_long+_lat+_course+_true_heading+_ts+_flags+_rstatus
        
    def encode_24(self, __mmsi, __part, __vname="NAN", __callsign="NAN", __vsize1="18", __vsize2="14", __vtype=50):
        _type = '{0:b}'.format(24).rjust(6,'0') 
        _repeat = "00" 
        _mmsi = '{0:b}'.format(__mmsi).rjust(30,'0')
        if __part == "A":
            _part = "00"
            _vname = self.encode_string(__vname)
            _padding = '0'*(156-6-2-30-2-len(_vname))
            return _type+_repeat+_mmsi+_part+_vname+_padding
        
        else:
            _part = "01"
            _vtype = '{0:b}'.format(__vtype).rjust(8,'0') 
            _vendorID = "0"*42
            
            _tmp = self.encode_string(__callsign)
            _callsign = _tmp + "0"*(42-len(_tmp)) 
            
            _hl=int(__vsize1)/2 
            _hw=int(__vsize2)/2
            _half_length='{0:b}'.format(int(_hl)).rjust(9,'0')
            _half_width='{0:b}'.format(int(_hw)).rjust(6,'0')
            
            return _type+_repeat+_mmsi+_part+_vtype+_vendorID+_callsign+_half_length+_half_length+_half_width+_half_width+"000000"
        
    def work(self, input_items, output_items):
        self.message = input_items[0][0]
        self.speed = input_items[1][0][0]
        self.long = input_items[1][0][1]
        self.lat = input_items[1][0][2]
        self.course = input_items[1][0][3]
        self.ts = input_items[1][0][4]
        
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = time_elapsed.total_seconds() * 1000
        slot_index = (milliseconds_elapsed)*self.slots_per_minute/60000 # Cantidad de slots desde que empezó el minuto.
        
        if (self.message == 18 and self.primera18):
            self. payload = self.encode_18(int(self.mmsi), float(self.speed), float(self.long), float(self.lat), float(self.course), int(self.ts))
            PMT_msg = pmt.to_pmt(self.payload)
            self.message_port_pub(pmt.intern(self.portName), PMT_msg)
            self.primera18 = False
            self.slot_transmitido18 = int(slot_index)
            
        elif (self.message == 240 and self.primera240):
            self.payload = self.encode_24(int(self.mmsi), "A", self.vessel_name)
            PMT_msg = pmt.to_pmt(self.payload)
            self.message_port_pub(pmt.intern(self.portName), PMT_msg)
            self.primera240 = False
            self.slot_transmitido240 = int(slot_index)
            
        elif (self.message == 241 and self.primera241):
            self.payload = self.encode_24(int(self.mmsi), "B", self.vessel_name, "@@@@@@@", str(self.vessel_length), str(self.vessel_beam), int(self.vessel_type))
            PMT_msg = pmt.to_pmt(self.payload)
            self.message_port_pub(pmt.intern(self.portName), PMT_msg)
            self.primera241 = False
            self.slot_transmitido241 = int(slot_index)
            
        if (np.abs(self.slot_transmitido18 - int(slot_index)) > 100):
            self.primera18 = True
            
        if (np.abs(self.slot_transmitido240 - int(slot_index)) > 100):
            self.primera240 = True
            
        if (np.abs(self.slot_transmitido241 - int(slot_index)) > 100):
            self.primera241 = True
            
        return (300)
        
        
        
        
        
        
        
        
        
