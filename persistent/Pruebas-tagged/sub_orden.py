#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zmq

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5599")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

try:
    while True:
        msg = subscriber.recv()
        print(msg)

except KeyboardInterrupt:
    subscriber.close()
    context.term()