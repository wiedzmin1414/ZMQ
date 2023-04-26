# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 13:14:40 2023

@author: lpolakie
"""

import zmq


def get_address_and_coords_from_message(message):
    byte_address = message[0]
    byte_coordinates = message[2]
    str_coordinates = byte_coordinates.decode("utf-8")
    x, y = str_coordinates.split(',')
    coordinates = (int(x), int(y))
    return byte_address, coordinates


class Server:
    def __init__(self, socket_address, number_of_clients):
        # Prepare our context and sockets
        self.socket_address = socket_address
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.requests = {}
        self.number_of_clients = number_of_clients

    def bind(self):
        self.socket.bind(self.socket_address)

    def run(self):
        self.bind()
        print("Server has been turned on")
        for i in range(self.number_of_clients):
            message = self.socket.recv_multipart()
            print(f"Receive message: {message}")
            address, coordinates = get_address_and_coords_from_message(message)
            if coordinates not in self.requests:
                self.requests[coordinates] = [address]
            else:
                self.requests[coordinates].append(address)
        print("All requests were collected")
        # Answer for each requests
        for coordinates, addresses in self.requests.items():
            for address in addresses:
                is_request_unique = bytes([True]) if len(addresses) == 1 else bytes([False])
                message = [address, b"", is_request_unique]
                self.socket.send_multipart(message)

        print("Server has been turned off")

    def close_connection(self):
        self.socket.close()
        self.context.term()


if __name__ == "__main__":
    server = Server("tcp://*:5799", number_of_clients=3)
    server.run()
