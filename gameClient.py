import client


def get_input_from_keyboard(statement="Type your move\n"):
    keyboard_input = input(statement)
    return keyboard_input[0]


class GameClient(client.Client):
    def __init__(self, socket_address):
        client.Client.__init__(self, socket_address)

    def establish_connection(self):
        self.connect()
        self.socket.send_string("Time for game")
        print(self.socket.recv())

    def send_request_and_wait_for_answer(self, request):
        self.socket.send_string(request)
        print(self.socket.recv())

    def play_game(self):
        self.establish_connection()
        request = None
        while request != 'k':
            request = get_input_from_keyboard()
            self.send_request_and_wait_for_answer(request)
        self.close_connection()


if __name__ == "__main__":
    client = GameClient("tcp://localhost:5793")
    client.connect()
    while True:
        keyb = get_input_from_keyboard()
        client.send_request_and_wait_for_answer(keyb)
