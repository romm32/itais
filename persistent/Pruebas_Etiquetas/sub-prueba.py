#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Archivo que pretendía ser la subscripción a lo enviado por el esquema de GNU Radio.

import pmt
import zmq
import numpy as np
import struct
from datetime import datetime

debug = 0         

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5580")
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
			
			#Se procesa el mensaje en función del topic del que viene.
			if topic == "valores_umbral_potencia":
				data_dict = eval(message)
				#print(f"Received threshold message: {data_dict}")
			#else:
				#print(f"Received message with unknown topic: {topic}")

			if cant_muestras_recibidas >= 500 and cant_muestras_recibidas < 510:
				if cant_muestras_recibidas == 500:
					current_time = datetime.now()
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