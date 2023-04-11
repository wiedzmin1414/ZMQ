# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 13:13:50 2023

@author: lpolakie
"""

import zmq
import random

#  Prepare our context and sockets
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5789")

x = random.randint(1, 10)
y = random.randint(1, 10)

message = f"{x},{y}"

print(f"Send request {message}")
socket.send_string(message)
print("Wait for answer from the server")
message_rep = socket.recv()
answer = message_rep == b"1"
print(f"Received reply: {answer}")