import gameServer
import gameClient
import unittest
from unittest.mock import Mock


class TestGameServer(unittest.TestCase):
    def test_get_address_and_requests_from_message(self):
        message = [b'address', b'', b'r']
        address, message = gameServer.get_address_and_request_from_message(message)
        expected_address, expected_message = b'address', 'r'
        self.assertEqual(address, expected_address)
        self.assertEqual(message, expected_message)

    def test_establish_connections_with_clients_when_3_clients_try_to_connect_to_board_10x10(self):
        server = gameServer.GameServer('blabla')
        requests = [
            [b'address1', b'', b'Time for game'],
            [b'address2', b'', b'Time for game'],
            [b'address3', b'', b'Time for game'],
        ]
        server.recv_multipart = Mock(side_effect=requests)
        server.poll = Mock(side_effect=[1, 1, 1, 0])
        server.wait_for_clients_connection = Mock()
        server.send_multipart = Mock()
        server.establish_connections_with_clients()

        self.assertEqual(server.number_of_clients, 3)
        server.close_connection()

    def test_establish_connections_with_clients_when_10_clients_try_to_connect_to_board_6x6(self):
        server = gameServer.GameServer('blabla', board_size=(6, 6))
        requests = [
            [b'address1', b'', b'Time for game'],
            [b'address2', b'', b'Time for game'],
            [b'address3', b'', b'Time for game'],
            [b'address4', b'', b'Time for game'],
            [b'address5', b'', b'Time for game'],
            [b'address6', b'', b'Time for game'],
            [b'address7', b'', b'Time for game'],
            [b'address8', b'', b'Time for game'],
            [b'address9', b'', b'Time for game'],
            [b'address10', b'', b'Time for game'],
        ]
        server.recv_multipart = Mock(side_effect=requests)
        server.poll = Mock(side_effect=[1]*10 + [0])

        server.wait_for_clients_connection = Mock()
        server.send_multipart = Mock()
        server.establish_connections_with_clients()

        self.assertEqual(server.number_of_clients, 4)
        server.close_connection()

    def test_collect_request(self):
        server = gameServer.GameServer('blabla', board_size=(6, 6))
        requests = [
            [b'address1', b'', b'r'],
            [b'address2', b'', b'w'],
            [b'address3', b'', b'd'],
        ]
        server.recv_multipart = Mock(side_effect=requests*2)  # this Mock and the next one has to have double output
        server.poll = Mock(side_effect=[1, 1, 1, 0]*2)        # because it will be used to add clients too
        server.wait_for_clients_connection = Mock()
        server.wait_for_clients_requests = Mock
        server.send_multipart = Mock()
        server.collect_requests_from_clients()
        expected_requests = {
            b'address1': 'r',
            b'address2': 'w',
            b'address3': 'd'
        }
        server_requests = server.requests
        self.assertDictEqual(expected_requests, server_requests)
        server.close_connection()


class TestGameClient(unittest.TestCase):
    def test_get_input_from_keyboard_when_input_contain_exactly_one_sign(self):
        gameClient.input = Mock(side_effect=['p'])
        keyboard_input = gameClient.get_input_from_keyboard()
        expected_input = 'p'
        self.assertEqual(expected_input, keyboard_input)

    def test_get_input_from_keyboard_when_input_contain_exactly_two_sign(self):
        gameClient.input = Mock(side_effect=['pr'])
        keyboard_input = gameClient.get_input_from_keyboard()
        expected_input = 'p'
        self.assertEqual(expected_input, keyboard_input)
