import server


class GameServer(server.Server):
    def __init__(self, socket_address, time_to_wait_for_clients, time_to_wait_for_move):
        self.time_to_wait = time_to_wait_for_clients
        self.time_to_wait_for_move = time_to_wait_for_move
        server.Server.__init__(self, socket_address=socket_address, number_of_clients=0)


