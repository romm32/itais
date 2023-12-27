#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# zmq_REQ_REP_server.py

# This server program capitalizes received strings and returns them.
# NOTES:
#   1) To comply with the GNU Radio view, messages are received on the REQ socket and sent on the REP socket.
#   2) The REQ and REP messages must be on separate port numbers.

import pmt
import zmq
import numpy as np
import struct

_debug = 0          # set to zero to turn off diagnostics

# Set up ZMQ SUB socket
context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5555")  # Connect to the same port as in your GNU Radio script
subscriber.setsockopt_string(zmq.SUBSCRIBE, "muestra")

#contador = 0

with open("taps.txt", "wb") as file:
    try:
        while True:
        	print("hello")
        	topic, message_bytes = subscriber.recv_multipart()
        	print("middletop")
        	message = np.frombuffer(message_bytes, dtype=np.complex64)
        	print("middle")
        	real_part, imag_part, tag_value = message
        	complex_sample = complex(real_part, imag_part)
        	print("complex_sample", complex_sample)
        	print("tag", tag_value)
        	
    except KeyboardInterrupt:
        pass

# Clean up the ZMQ context
subscriber.close()
context.term()
