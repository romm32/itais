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

_debug = 0          # set to zero to turn off diagnostics

'''
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

# Create the REQ socket sink block
req_context = zmq.Context()
req_sock = req_context.socket(zmq.REQ)
req_sock.connect('tcp://127.0.0.1:50247')

# ... Loop for sending requests ...

# Send a request to the GR-Block
request = b"Request from client"  # Modify this message as needed
req_sock.send(request)

# Receive the reply from the GR-Block
reply = req_sock.recv()

while True:
    print('hello world')
    #  Wait for next request from client
    data = req_sock.recv()
    #message = pmt.to_python(pmt.deserialize_str(data))
    #data = np.frombuffer(msg, dtype=np.complex64, count=-1) # make sure to use correct data type (complex64 or float32); '-1' means read all data in the buffer
    #print(data[0:10])
    #print("Received request: %s" % message)

    #output = message.upper()
    print('goodbye world')
    
    reply = b"Reply from server"
    req_sock.send(reply)
    
    
import zmq
'''

'''
# create a REP socket
_PROTOCOL = "tcp://"
_SERVER = "127.0.0.1"          # localhost
_REP_PORT = ":50247"
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


req_context = zmq.Context()
req_sock = req_context.socket(zmq.REQ)
req_sock.connect('tcp://127.0.0.1:50247')
'''

        


# Set up ZMQ SUB socket
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")  # Connect to the same port as in your GNU Radio script
socket.setsockopt_string(zmq.SUBSCRIBE, "")

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
            # Write the taps to the file
            file.write(taps.tobytes())
            print('goodbye')
    except KeyboardInterrupt:
        pass

# Clean up the ZMQ context
socket.close()
context.term()



