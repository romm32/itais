#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# zmq_REQ_REP_server.py


import pmt
import zmq
import numpy as np

_debug = 0          # set to zero to turn off diagnostics

# Set up ZMQ SUB socket
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")  # Connect to the same port as in your GNU Radio script
socket.setsockopt_string(zmq.SUBSCRIBE, "")
i = 0

with open("taps.txt", "wb") as file:
    try:
        while True:
            print('hello')
            # Receive data from ZMQ socket
            data = socket.recv()
            print('middletop')
            # Convert bytes to a NumPy array of complex samples
            taps = np.frombuffer(data, dtype=np.complex64)
            print('middle')
            if (i < 8):
            	# Write the taps to the file
            	#file.write(taps.tobytes())
            	file.write(taps)
            	i += 1
            print('goodbye')
    except KeyboardInterrupt:
        pass

# Clean up the ZMQ context
socket.close()
context.term()