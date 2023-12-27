#!/usr/bin/env python3
import zmq

# Create a ZMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.SUB)

# Set the ZMQ socket to subscribe to the same address as the ZMQ Pub block
socket.connect("tcp://127.0.0.1:5555")

# Subscribe to the message (use the same message name you configured in ZMQ Pub)
socket.setsockopt_string(zmq.SUBSCRIBE, "mensaje")

try:
    while True:
        print("Antes de .rcv")
        # Receive the message
        message = socket.recv()
        print("Despues de .rcv")
	
        # Process the received data as needed
        

        # Do something with the received data

except KeyboardInterrupt:
    pass
    
except zmq.ZMQError as e:
    print("ZMQ Error:", e)
except Exception as e:
    print("Error:", e)

# Clean up the ZMQ socket and context when done
socket.close()
context.term()

