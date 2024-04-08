#!/usr/bin/env python3

# Este script fue escrito para poder correr el transmisor incluso si no se cuenta con un
# módulo GPS disponible.

import zmq
import time


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5600")
from datetime import datetime


latitude = 0
longitude = 0
speed = 0
speed_in_knots = 0
course = 0
gps_time_str = 0
utc_second = 0
dict = {"speed": speed_in_knots, "lon": longitude, "lat": latitude, "course": course, "UTC_sec": utc_second}


while True:
    latitude = -34.90328
    longitude = -56.18816
    speed_in_knots = 3 
    course = 3

    current_utc_time = datetime.utcnow()
    start_of_minute = current_utc_time.replace(second=0, microsecond=0)
    time_elapsed = current_utc_time - start_of_minute
    utc_second = time_elapsed.total_seconds()
            
    dict = {"speed": speed_in_knots, "lon": longitude, "lat": latitude, "course": course, "UTC_sec": utc_second}
    socket.send_string(f"{dict}")

    time.sleep(0.00001) 

        
        
