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

class selector_itais(gr.sync_block):
    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.canal = "A"
        self.portName_in = 'canal'
        self.message_port_register_in(pmt.intern(self.portName_in))
        self.set_msg_handler(pmt.intern("canal"), self.process_message)

    def process_message(self, message):
        # Retrieve message payload and save it to a variable
        self.canal = pmt.to_python(message) # lista con los candidatos
        print("transmitiendo en ", self.canal)

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        if self.canal == "A":
            output_items[0][:] = input_items[0]
        elif self.canal == "B":
            output_items[0][:] = input_items[1]
            
        return len(output_items[0])
