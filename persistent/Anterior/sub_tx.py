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
import argparse
import sys

_debug = 0          # set to zero to turn off diagnostics


parser = argparse.ArgumentParser(description='Designador del canal')
parser.add_argument('designator', type = str)
args = parser.parse_args()

# Access the values of parameters using args.param1
if args.designator is not None and (args.designator == "A" or args.designator == "B") :
	designator = args.designator
	print('designator', designator)
else:
	sys.exit("Termina el script porque el designator no se fijó o se le asignó un valor distinto de A y B")


if designator == "A": #Se seleccionó el canal A

	# Set up ZMQ SUB socket
	context = zmq.Context()
	socket = context.socket(zmq.SUB)
	socket.connect("tcp://localhost:5555")  # Connect to the same port as in your GNU Radio script
	socket.setsockopt_string(zmq.SUBSCRIBE, "")
	
	context2 = zmq.Context()
	socket2 = context2.socket(zmq.SUB)
	socket2.connect("tcp://localhost:5556")  # Connect to the same port as in your GNU Radio script
	socket2.setsockopt_string(zmq.SUBSCRIBE, "")

	#contador = 0

	with open("taps_A_umbral.txt", "wb") as file:
		with open("taps_A_potencia.txt", "wb") as file2:
			try:
				while True:
				    #contador += 1
				    print('hello_A')
				    # Receive data from ZMQ socket
				    data = socket.recv()
				    data2 = socket2.recv()
				    #print('middletop_A')
				    # Convert bytes to a NumPy array of complex samples
				    taps_A = np.frombuffer(data, dtype=np.complex64)
				    taps_A_2 = np.frombuffer(data2, dtype=np.complex64)
				    print("umbral_A: ", taps_A)
				    print("potencia_A: ", taps_A_2)
				    # Write the taps to the file
				    file.write(taps_A.tobytes())
				    file2.write(taps_A_2.tobytes())
				    #print('goodbye_A')
				    
			except KeyboardInterrupt:
				pass
		socket2.close()
		context2.term()

	# Clean up the ZMQ context
	socket.close()
	context.term()

if designator == "B": #Se seleccionó el canal B

	# Set up ZMQ SUB socket
	context = zmq.Context()
	socket = context.socket(zmq.SUB)
	socket.connect("tcp://localhost:5557")  # Connect to the same port as in your GNU Radio script
	socket.setsockopt_string(zmq.SUBSCRIBE, "")
	
	context2 = zmq.Context()
	socket2 = context2.socket(zmq.SUB)
	socket2.connect("tcp://localhost:5558")  # Connect to the same port as in your GNU Radio script
	socket2.setsockopt_string(zmq.SUBSCRIBE, "")

	#contador = 0

	with open("taps_B_umbral.txt", "wb") as file:
		with open("taps_B_potencia.txt", "wb") as file2:
			try:
				while True:
				    #contador += 1
				    print('hello_B')
				    # Receive data from ZMQ socket
				    data = socket.recv()
				    data2 = socket2.recv()
				    #print('middletop_B')
				    # Convert bytes to a NumPy array of complex samples
				    taps_B = np.frombuffer(data, dtype=np.complex64)
				    taps_B_2 = np.frombuffer(data2, dtype=np.complex64)
				    print("umbral_B: ", taps_B)
				    print("potencia_B: ", taps_B_2)
				    # Write the taps to the file
				    file.write(taps_B.tobytes())
				    file2.write(taps_B_2.tobytes())
				    #print('goodbye_B')
				    
			except KeyboardInterrupt:
				pass
		socket2.close()
		context2.term()

	# Clean up the ZMQ context
	socket.close()
	context.term()




