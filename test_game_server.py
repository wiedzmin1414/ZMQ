import game_server
import unittest


class TestGameServer(unittest.TestCase):
    def setUp(self):
        pass  # ToDo add mocks

    def tearDown(self):
        self.server.close_connection()

    def test_start_server_and_wait_30_second_for_clients(self):
        self.server = game_server.GameServer('blabla', 30, 5)
