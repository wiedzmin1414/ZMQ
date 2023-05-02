import server
import time


class GameServer(server.Server):
    def __init__(self, socket_address, time_to_wait_for_clients, time_to_wait_for_move):
        self.time_to_wait_for_clients = time_to_wait_for_clients
        self.time_to_wait_for_move = time_to_wait_for_move
        server.Server.__init__(self, socket_address=socket_address, number_of_clients=0)

    def wait_for_clients_connection(self):
        time.sleep(self.time_to_wait_for_clients)

    def wait_for_clients_requests(self):
        time.sleep(self.time_to_wait_for_move)

    def establish_connection_with_clients(self):
        flag = True

        while flag:
            message = self.socket.recv_multipart()
            print(message)
