#!/usr/bin/env python3

import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE, "")
socket.setsockopt(zmq.RECONNECT_IVL, 1000)
socket.connect("tcp://127.0.0.1:5600")

while True:
	raw_message = socket.recv_string()
	print(f"{raw_message}")
	time.sleep(1)
