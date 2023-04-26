import game_server
import game_client
import unittest
from unittest.mock import Mock


class TestGameServer(unittest.TestCase):
    def setUp(self):
        pass  # ToDo add mocks

    def tearDown(self):
        self.server.close_connection()

    def test_start_server_and_wait_30_second_for_one_client(self):
        self.server = game_server.GameServer('blabla', 30, 5)
        self.server.wait_for_clients_connection()
        self.server.establish_connection_with_clients()


class TestGameClient(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        self.client.close_connection()

    def test_client_init(self):
        self.client = game_client.GameClient('dummy_socket')
        self.client.connect = Mock()
