import gpsd
import time
from datetime import datetime
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5600")

def get_gps_data():
	# En la Raspberry Pi es necesario conectarse al proceso gpsd, que es el que tiene
	# el "control" sobre el módulo GPS conectado. Eso se debe a que está configurado
	# el servidor NTP chrony.
	gpsd.connect()

	try:
		# Se obtienen datos del GPS. Si se tiene suficiente confianza en la info (2D o 3D fix),
		# se extrae la información y se envía al socket que se recibe en Sub_GPS. 
		packet = gpsd.get_current()
		if packet.mode >= 2:  # 2D or 3D fix
			latitude = packet.lat
			longitude = packet.lon
			speed_in_knots = packet.hspeed
			course = packet.track
			utc_time = packet.get_time()
			utc_second = utc_time.second
			
			dict = {"speed": speed_in_knots, "lon": longitude, "lat": latitude, "course": course, "UTC_sec": utc_second}
			socket.send_string(f"{dict}")
		else:
			dict = {"speed": 0, "lon": 0, "lat": 0, "course": 0, "UTC_sec": 0}
			socket.send_string(f"{dict}")

	except Exception as e:
		print(f"Error: {e}")
		socket.close()
		context.term()

if __name__ == "__main__":
	# La idea es pedirle datos muchas veces por segundo. Esto evita que el flowgraph de GNU Radio
	# encuentre un cuello de botella debido a este script.
	while True:
		get_gps_data()
		time.sleep(0.00001)

