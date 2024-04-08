#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pmt
import zmq
import numpy as np

# Se inicializa un socket
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")  # Debe ser el mismo puerto utilizado en GNU Radio.
socket.setsockopt_string(zmq.SUBSCRIBE, "")
i = 

with open("tapsfrombuffer.txt", "wb") as file:
    try:
        while True:
            print('hello')
            data = socket.recv()
            print('middletop')
            taps = np.frombuffer(data, dtype=np.complex64)
            print('middle')
            if (i < 8):
            	print('goodbye')
            	# Se escriben las taps en el archivo creado.
            	file.write(taps)
            	print(np.size(taps))
            	i += 1
    except KeyboardInterrupt:
        pass

socket.close()
context.term()

