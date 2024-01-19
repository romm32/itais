#!/usr/bin/env python3

import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5605")


while True:

    arreglo = [1, 2, 3,4,5,6,7,8,9,10]
    
    socket.send(arreglo)

    print("messages sent", arreglo)
    time.sleep(3)

