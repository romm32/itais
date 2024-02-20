import gpsd
import time
from datetime import datetime
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5600")

def get_gps_data():
	# Connect to the local gpsd service (default host and port)
	gpsd.connect()

	try:
		# Get the latest data from the GPS
		packet = gpsd.get_current()
		# Check if the GPS data is valid
		if packet.mode >= 2:  # 2D or 3D fix
			# Extract relevant information
			latitude = packet.lat
			longitude = packet.lon
			speed_in_knots = packet.speed*1.94384
			course = packet.track
			gps_time_str = packet.time
			gps_time_datetime = datetime.strptime(gps_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")			
			utc_second = gps_time_datetime.second
			# Print the information
			print(f"Latitude: {latitude}, Longitude: {longitude}, Speed: {speed_in_nots}, Course: {course}, UTC second: {utc_second}")
			dict = {"speed": speed_in_knots, "lon": longitude, "lat": latitude, "course": course, "UTC_sec": utc_second}
			socket.send_string(f"{dict}")
		else:
			print("Waiting for a GPS fix...")

	except Exception as e:
		print(f"Error: {e}")
		socket.close()
		context.term()

if __name__ == "__main__":
	while True:
		get_gps_data()
		time.sleep(1)

