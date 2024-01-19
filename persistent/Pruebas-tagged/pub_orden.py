#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5599")


try:
    while True:
        for i in 'abcdefghi':
            socket.send_string(i)
except KeyboardInterrupt:
    pass

socket.close()
context.term()