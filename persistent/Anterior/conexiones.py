#!/usr/bin/python3
# -*- coding: utf-8 -*-

# zmq_SUB_proc.py
# Author: Marc Lichtman

import zmq
import numpy as np
import time
import matplotlib.pyplot as plt

_debug = 0          # set to zero to turn off diagnostics

# create a REQ socket
_PROTOCOL = "tcp://"
_SERVER = "127.0.0.1"          # localhost
_REQ_PORT = ":50247"
_REQ_ADDR = _PROTOCOL + _SERVER + _REQ_PORT
if (_debug):
    print ("'zmq_REQ_REP_server' version 20056.1 connecting to:", _REQ_ADDR)
req_context = zmq.Context()
if (_debug):
    assert (req_context)
req_sock = req_context.socket (zmq.REQ)
if (_debug):
    assert (req_sock)
rc = req_sock.connect (_REQ_ADDR)
if (_debug):
    assert (rc == None)

# create a REP socket
_PROTOCOL = "tcp://"
_SERVER = "127.0.0.1"          # localhost
_REP_PORT = ":50246"
_REP_ADDR = _PROTOCOL + _SERVER + _REP_PORT
if (_debug):
    print ("'zmq_REQ_REP_server' version 20056.1 binding to:", _REP_ADDR)
rep_context = zmq.Context()
if (_debug):
    assert (rep_context)
rep_sock = rep_context.socket (zmq.REP)
if (_debug):
    assert (rep_sock)
rc = rep_sock.bind (_REP_ADDR)
if (_debug):
    assert (rc == None)


socket = req_sock

while True:
    print("1")
    print("2")
    msg = socket.recv() # grab the message
    print("3")
    print(len(msg)) # size of msg
    data = np.frombuffer(msg, dtype=np.complex64, count=-1) # make sure to use correct data type (complex64 or float32); '-1' means read all data in the buffer
    print(data[0:10])
# plt.plot(np.real(data))
# plt.plot(np.imag(data))
# plt.show()
    '''

while True:
    #  Wait for next request from client
    data = req_sock.recv()
    message = pmt.to_python(pmt.deserialize_str(data))
    print("Received request: %s" % message)

    output = message.upper()

    #  Send reply back to client
    rep_sock.send (pmt.serialize_str(pmt.to_pmt(output)))
'''
