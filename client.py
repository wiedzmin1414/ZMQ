# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 13:13:50 2023

@author: lpolakie
"""

import zmq
import random


class Client:
    def __init__(self, socket_address):
        #  Prepare our context and sockets
        self.socket_address = socket_address
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.response = None

    def connect(self):
        self.socket.connect(self.socket_address)

    def send_message_and_wait_for_response(self):
        self.connect()
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        
        message = f"{x},{y}"
        
        print(f"Send request {message}")
        self.socket.send_string(message)
        print("Waiting for a response from the server")
        message_rep = self.socket.recv()
        self.response = message_rep == bytes([True])
        print(f"Response received: {self.response}")

    def close_connection(self):
        self.socket.close()
        self.context.term()
        

if __name__ == "__main__":
    client = Client("tcp://localhost:5799")
    client.send_message_and_wait_for_response()
