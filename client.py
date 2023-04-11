# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 13:13:50 2023

@author: lpolakie
"""

import zmq
import random

class Client:
    def __init__(self, socket_adress):
        #  Prepare our context and sockets
        self.socket_adress = socket_adress
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(self.socket_adress)
        
    def send_message_and_wait_for_answer(self):

        x = random.randint(1, 10)
        y = random.randint(1, 10)
        
        message = f"{x},{y}"
        
        print(f"Send request {message}")
        self.socket.send_string(message)
        print("Waiting for a response from the server")
        message_rep = self.socket.recv()
        answer = message_rep == bytes([True])
        print(f"Response received: {answer}")
        

if __name__ == "__main__":
    client = Client("tcp://localhost:5799")
    client.send_message_and_wait_for_answer()