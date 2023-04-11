# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 13:14:40 2023

@author: lpolakie
"""

import zmq

def get_adress_and_cord_from_message(message):
    byte_adress = message[0]
    byte_corrds = message[2]
    str_corrds = byte_corrds.decode("utf-8")
    x, y = str_corrds.split(',')
    corrds = (int(x), int(y))
    return byte_adress, corrds

# Prepare our context and sockets
context = zmq.Context()
frontend = context.socket(zmq.ROUTER)
frontend.bind("tcp://*:5789")

requests = {}

# Switch messages between sockets
number_of_clients = 2
number_of_requests = 0

while number_of_requests < number_of_clients:
        message = frontend.recv_multipart()
        print(f"Receive message: {message}")
        adress, corrds = get_adress_and_cord_from_message(message)
        
        number_of_requests += 1
        if corrds not in requests:
            requests[corrds] = [adress]
        else:
            requests[corrds].append(adress)
        #frontend.send_multipart(message)
        
for corrds, adresses in requests.items():
    for adress in adresses:
        is_request_unique = b'1' if len(adresses) == 1 else b'0'
        
        message = [adress, b"", is_request_unique]
        frontend.send_multipart(message)
        

    
