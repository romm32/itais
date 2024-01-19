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
import struct
from datetime import datetime

debug = 0          # set to zero to turn off diagnostics

# Set up ZMQ SUB socket
context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5580")  # Connect to the same port as in your GNU Radio script
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5590")

timer1 = 0

etiqueta_esperada = 1

recibio = False
primera_vez = True

cant_muestras_recibidas = 0

try: 

	while timer1 < 20:
		timer1 = timer1 + 1

	if timer1 == 20:
		float_bytes = struct.pack('!f', 1)
		socket.send(float_bytes)
		#float_bytes = struct.pack('!f', 0)
		#socket.send(float_bytes)
		print("tx: envio pedido")
		timer1 = 0

	while not recibio:
		try:
			raw_message = subscriber.recv_string()
			recibio = True
			print("recibioTX")
			cant_muestras_recibidas += 1
		except:
			float_bytes = struct.pack('!f', 1)
			socket.send(float_bytes)
			#float_bytes = struct.pack('!f', 0)
			#socket.send(float_bytes)
			print("reenvio")
		

	try:
		while True:
			if not primera_vez:
				#print("tx: recibiendo")
				raw_message = subscriber.recv_string()
				#print("tx: recibio")
				cant_muestras_recibidas += 1

			else:
				primera_vez	= False
			#print(f"Received raw message: {raw_message}")
			topic, message = raw_message.split(' ', 1)
			
			# Se procesa el mensaje en función del topic del que viene.
			if topic == "valores_umbral_potencia":
				data_dict = eval(message)
				#print(f"Received threshold message: {data_dict}")
			#else:
				#print(f"Received message with unknown topic: {topic}")

			if cant_muestras_recibidas >= 500 and cant_muestras_recibidas < 510:
				if cant_muestras_recibidas == 500:
					# Get the current time
					current_time = datetime.now()
					# Format the current time as a string
					formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

					print("tx llego a 500", formatted_time)
	except KeyboardInterrupt:
		print("Received keyboard interrupt. Closing the socket.")
	finally:
		print("cerrando")
		print("muestras", cant_muestras_recibidas)
		subscriber.close()
		context.term()

except KeyboardInterrupt:
	pass
finally:
	socket.close()
	context.term()        	