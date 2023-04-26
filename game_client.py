import client


class GameClient(client.Client):
    def __init__(self, socket_adress):
        self.position = (None, None)
        client.Client.__init__(self, socket_adress)

    def play_game(self):
        self.connect()
