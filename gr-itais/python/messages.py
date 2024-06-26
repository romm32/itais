#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 Romina Garcia, Maximo Pirri.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np
from gnuradio import gr
import pmt
from datetime import datetime, timedelta
from gnuradio import eng_notation
from gnuradio.filter import window
from gnuradio import digital
from gnuradio import fft
from gnuradio import blocks
from gnuradio import analog
from math import pi
import itais
import time

class messages(gr.sync_block):  

    def __init__(self, vessel_length = 8, vessel_beam = 4, vessel_name = "ROMA", vessel_type = 30):  
        gr.sync_block.__init__(
            self,
            name='messages', 
            in_sig=[(np.float32, 5)],
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
        
        self.mmsi = 123456789 # Default. tiene que tener 9 dígitos
        self.payload = ""
        
        self.slots_per_minute = 2250
        self.slot_duration = 60/2250
        self.samples_per_slot = int(self.slot_duration*50000)
        
        self.portName_in = 'Msg'
        self.message_port_register_in(pmt.intern(self.portName_in))
        self.set_msg_handler(pmt.intern("Msg"), self.process_message)
        
        self.mensaje24A = 00000000
        self.mensaje24B = 00000000
        
        self.once = True
        self.payload_ceros = '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        
        
    def process_message(self, message):
        # Se obtiene información a través del puerto de tipo mensaje. 
        self.message = pmt.to_python(message) 
    
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
        _type = '{0:b}'.format(18).rjust(6,'0') # 18
        _repeat = "00"	#repeat (directive to an AIS transceiver that this message should be rebroadcast.)
        _mmsi = '{0:b}'.format(__mmsi).rjust(30,'0') # 30 bits (247320162)
        _reserved = '0'*8
        _speed = '{0:b}'.format(int(round(__speed*10))).rjust(10,'0')	# Speed over ground is in 0.1-knot resolution from 0 to 102 knots. value 1023 indicates speed is not available, value 1022 indicates 102.2 knots or higher.
        _accurancy = '0' # > 10m
        
        (_long, _lat) = self.compute_long_lat(__long, __lat)
        
        _course = '{0:b}'.format(int(round(__course*10))).rjust(12,'0') # 0.1 resolution. Course over ground will be 3600 (0xE10) if that data is not available.
        _true_heading = '1'*9	# 511 (N/A)
        _ts = '{0:b}'.format(__ts).rjust(6,'0') # Second of UTC timestamp.
        
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
        # '11100000000000000110' : Radio status
        
        return _type+_repeat+_mmsi+_reserved+_speed+_accurancy+_long+_lat+_course+_true_heading+_ts+_flags+_rstatus
        
    def encode_24(self, __mmsi, __part, __vname="NAN", __callsign="NAN", __vsize1="8", __vsize2="4", __vtype=50):
        _type = '{0:b}'.format(24).rjust(6,'0') # 24
        _repeat = "00" # repeat (directive to an AIS transceiver that this message should be rebroadcast.)
        _mmsi = '{0:b}'.format(__mmsi).rjust(30,'0') # 30 bits (247320162)
        if __part == "A":
            _part = "00"
            _vname = self.encode_string(__vname)
            _padding = '0'*(156-6-2-30-2-len(_vname))		# 160 bits per RFC -> 4 bits padding added in Build_Frame_imple.cc
            return _type+_repeat+_mmsi+_part+_vname+_padding
        
        else:
            _part = "01"
            _vtype = '{0:b}'.format(__vtype).rjust(8,'0')   #30 = fishing
            _vendorID = "0"*42 #vendor ID
            
            _tmp = self.encode_string(__callsign)
            _callsign = _tmp + "0"*(42-len(_tmp)) #7 six-bit characters
            
            _hl=int(__vsize1)/2 # AIS antenna in the middle of the boat
            _hw=int(__vsize2)/2
            _half_length='{0:b}'.format(int(_hl)).rjust(9,'0')
            _half_width='{0:b}'.format(int(_hw)).rjust(6,'0')
            
            return _type+_repeat+_mmsi+_part+_vtype+_vendorID+_callsign+_half_length+_half_length+_half_width+_half_width+"000000"
        
    def work(self, input_items, output_items):
        self.speed = input_items[0][0][0]
        self.long = input_items[0][0][1]
        self.lat = input_items[0][0][2]
        self.course = input_items[0][0][3]
        self.ts = input_items[0][0][4]
        
        current_utc_time = datetime.utcnow()
        start_of_minute = current_utc_time.replace(second=0, microsecond=0)
        time_elapsed = current_utc_time - start_of_minute
        milliseconds_elapsed = time_elapsed.total_seconds() * 1000
        slot_index = (milliseconds_elapsed)*self.slots_per_minute/60000 # Cantidad de slots desde que empezó el minuto.
        
        if (self.once):
            self.once = False
            self.mensaje24A = self.encode_24(int(self.mmsi), "A", self.vessel_name)
            self.mensaje24B = self.encode_24(int(self.mmsi), "B", self.vessel_name, "@@@@@@@", str(self.vessel_length), str(self.vessel_beam), int(self.vessel_type))
        
        if (self.message == 18):
            if self.speed == 0 and self.long == 0 and self.lat == 0 and self.course == 0: # Si no tenemos datos de GPS 
            										     # válidos, no mandamos nada
                print("Se descartó mensaje por falta de GPS fix")
                self.message = 0
                
            else:
                self. payload = self.encode_18(int(self.mmsi), float(self.speed), float(self.long), float(self.lat), float(self.course), int(self.ts))
                PMT_msg = pmt.to_pmt(self.payload)
                self.message_port_pub(pmt.intern(self.portName), PMT_msg)
                self.message = 50
                print("mando 18")
            
        elif (self.message == 240):
            if self.speed == 0 and self.long == 0 and self.lat == 0 and self.course == 0: # Si no tenemos datos de GPS 
            										     # válidos, no mandamos nada
                print("Se descartó mensaje por falta de GPS fix")
                self.message = 0
                
            else:
                self.payload = self.mensaje24A 
                PMT_msg = pmt.to_pmt(self.payload)
                self.message_port_pub(pmt.intern(self.portName), PMT_msg)
                self.message = 50
                print("mando 240")
            
        elif (self.message == 241):
            if self.speed == 0 and self.long == 0 and self.lat == 0 and self.course == 0: # Si no tenemos datos de GPS 
            										     # válidos, no mandamos nada
                print("Se descartó mensaje por falta de GPS fix")
                self.message = 0
                
            else:
                self.payload = self.mensaje24B
                PMT_msg = pmt.to_pmt(self.payload)
                self.message_port_pub(pmt.intern(self.portName), PMT_msg)
                self.message = 50
                print("mando 241")
        
        elif (self.message == 50): # Envío de mensaje Dummy
        	PMT_msg = pmt.to_pmt(self.payload_ceros)
        	self.message_port_pub(pmt.intern(self.portName), PMT_msg)
        	self.message = 0
        	print("mando 0")      
        
        return (256)
        
        
        
        
        
        
        
        
        
