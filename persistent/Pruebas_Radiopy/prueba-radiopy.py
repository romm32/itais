#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pmt
import zmq
import numpy as np


# Se inicializa un socket TCP para recibir muestras de radio.py
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555") 
socket.setsockopt_string(zmq.SUBSCRIBE, "")
i = 0

with open("taps.txt", "wb") as file:
    try:
        while True:
            print('hello')
            data = socket.recv()
            print('middletop')
            taps = np.frombuffer(data, dtype=np.complex64)
            print('middle')
            if (i < 8):
            	file.write(taps)
            	i += 1
            print('goodbye')
    except KeyboardInterrupt:
        pass

socket.close()
context.term()
