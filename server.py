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

class Server:
    def __init__(self, socket_adress, number_of_clients):
        # Prepare our context and sockets
        self.socket_adress = socket_adress
        context = zmq.Context()
        self.socket = context.socket(zmq.ROUTER)
        self.socket.bind(self.socket_adress)
        self.requests = {}
        self.number_of_clients = number_of_clients
    
    def run(self):
        print("Server has been turned on")
        for i in range(self.number_of_clients):
                message = self.socket.recv_multipart()
                print(f"Receive message: {message}")
                adress, coordination = get_adress_and_cord_from_message(message)
                if coordination not in self.requests:
                    self.requests[coordination] = [adress]
                else:
                    self.requests[coordination].append(adress)
        print("All requests were collected")
        # Answer for each requests
        for coordination, adresses in self.requests.items():
            for adress in adresses:
                is_request_unique = bytes([True]) if len(adresses) == 1 else bytes([False])
                message = [adress, b"", is_request_unique]
                self.socket.send_multipart(message)
        
        print("Server has been turned off")
        
if __name__ == "__main__":
    server = Server("tcp://*:5799", number_of_clients=2)
    server.run()
