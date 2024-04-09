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
import zmq

class sub_gps(gr.sync_block):

    def __init__(self):
        
        gr.sync_block.__init__(
            self,
            name='sub_gps', 
            in_sig=[],
            out_sig=[(np.float32, 5), np.float32]
        )
        self.arr = [0, 0, 0, 0, 0]

    def work(self, input_items, output_items):
    	
    	context = zmq.Context()
    	socket = context.socket(zmq.SUB)
    	socket.setsockopt(zmq.RECONNECT_IVL, 1000)
    	socket.setsockopt_string(zmq.SUBSCRIBE, "")
    	socket.connect("tcp://127.0.0.1:5600")  # Se conecta al socket que está definido en el script get_gps.
												# Se realiza la conexión en cada ejecución del work porque
												# no se puede inicializar el socket en el init (GNU Radio no
												# lo permite).  	
    	msj = socket.recv_string()
    	data_dict = eval(msj)
    	
    	self.arr[0] = data_dict["speed"]
    	self.arr[1] = data_dict["lon"]
    	self.arr[2] = data_dict["lat"]
    	self.arr[3] = data_dict["course"]
    	self.arr[4] = data_dict["UTC_sec"]
    	    	
    	output_items[0][:] = self.arr # velocidad, longitud, latitud, curso, ts second
    	output_items[1][:] = data_dict["speed"] # velocidad
    		
    	return 100
