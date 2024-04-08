#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pmt
import zmq
import numpy as np


# Se inicializa un socket
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555") # Debe ser la misma IP:puerto que se utilice en el flowgraph
socket.setsockopt_string(zmq.SUBSCRIBE, "")


with open("taps.txt", "wb") as file:
    try:
        while True:
            # Se reciben datos, se interpretan como complejos y se imprimen en el archiov taps creado.
            # Se tienen varios prints para debug.
            print('hello')
            data = socket.recv()
            print('middletop')
            taps = np.frombuffer(data, dtype=np.complex64)
            print('middle')
            file.write(taps.tobytes())
            print('goodbye')
    except KeyboardInterrupt:
        pass

socket.close()
context.term()
