import server
import time
import gameBoard


def get_address_and_request_from_message(message):
    byte_address = message[0]
    byte_request = message[2]
    str_request = byte_request.decode("utf-8")
    return byte_address, str_request


class GameServer(server.Server):
    def __init__(self, socket_address, time_to_wait_for_clients=30, time_to_wait_for_request=5, board_size=(10, 10)):
        self.time_to_wait_for_clients = time_to_wait_for_clients
        self.time_to_wait_for_request = time_to_wait_for_request
        self.board = gameBoard.GameBoard(*board_size)
        server.Server.__init__(self, socket_address=socket_address, number_of_clients=0)
        self.requests = {}
        self.connected_clients = []

    def return_number_of_clients(self):
        return self.board.number_of_players

    def wait_for_clients_connection(self):
        time.sleep(self.time_to_wait_for_clients)

    def wait_for_clients_requests(self):
        time.sleep(self.time_to_wait_for_request)

    def process_requests_and_answer(self):
        result_of_requests_processing = self.board.process_request(self.requests)
        for address, answer in result_of_requests_processing.items():
            self.send_multipart(address, answer)

    def add_client(self, address):
        self.board.add_client(address)

    def recv_multipart(self):
        return self.socket.recv_multipart()

    def send_multipart(self, address, message):
        message_to_send = [address, b"", str(message).encode('UTF-8')]
        self.socket.send_multipart(message_to_send)

    def poll_messages(self, timeout=10):
        return self.socket.poll(timeout=timeout)

    def establish_connections_with_clients(self):
        max_players = self.board.max_players
        while self.poll_messages(timeout=10):
            message = self.recv_multipart()
            address, text = get_address_and_request_from_message(message)
            if self.number_of_clients < max_players:
                self.add_client(address)
                self.number_of_clients += 1
                self.send_multipart(address, "Let's play a game")
                self.connected_clients.append(address)
            else:
                self.send_multipart(address, "Sorry, there are too much players")

    def collect_requests_from_clients(self):
        requests = {}
        while self.poll_messages(timeout=10):
            message = self.recv_multipart()
            address, request = get_address_and_request_from_message(message)
            if address in self.connected_clients:
                requests[address] = request
            else:
                self.send_multipart(address, 'You are not playing a game!')
        self.requests = requests

    def run(self, printing_positions=False):
        print("Waiting for connections")
        self.bind()
        self.wait_for_clients_connection()
        self.establish_connections_with_clients()
        flag = True
        while flag:
            if printing_positions:
                for client, position in self.board.clients_positions.items():
                    print(f"{client} is on position {position}")
            try:
                print("Waiting for new requests")
                self.wait_for_clients_requests()
                self.collect_requests_from_clients()
                self.process_requests_and_answer()
            except KeyboardInterrupt:
                print("Server successfully down")
                self.close_connection()
                flag = False


if __name__ == "__main__":
    server = GameServer("tcp://*:5793", 10, 3)
    server.run(printing_positions=True)
