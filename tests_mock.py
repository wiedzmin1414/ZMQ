# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:34:17 2023

@author: lpolakie
"""

import server
import unittest
import client
from unittest.mock import Mock


class Test_get_address_and_coordinates_from_message(unittest.TestCase):
    def setUp(self):
        self.message = [b'\x00\x00\x00\x12\xdb', b'', b'7,8']

    def test_get_address_and_coordinates_from_message(self):
        address, coordinates = server.get_address_and_coords_from_message(self.message)
        self.assertEqual(address, b'\x00\x00\x00\x12\xdb')
        self.assertEqual(coordinates, (7, 8))


class TestServer(unittest.TestCase):
    def setUp(self):
        messages_to_send = [
            [b'\x00\x80\x00\x16I', b'', b'6,9'],
            [b'\x00\x80\x00\x16J', b'', b'6,9'],
            [b'\x00\x80\x00\x16J', b'', b'1,2'],
            [b'\x00\x80\x00\x16K', b'', b'3,4'],
            [b'\x00\x80\x00\x16L', b'', b'5,6'],
        ]
        number_of_clients = len(messages_to_send)
        self.server = server.Server('localhost', number_of_clients=number_of_clients)
        self.server.bind = Mock()
        self.server.socket.recv_multipart = Mock(side_effect=messages_to_send)
        self.server.socket.send_multipart = Mock()

        self.expected_sent_messages = [
            [b'\x00\x80\x00\x16I', b'', bytes([False])],
            [b'\x00\x80\x00\x16J', b'', bytes([False])],
            [b'\x00\x80\x00\x16J', b'', bytes([True])],
            [b'\x00\x80\x00\x16K', b'', bytes([True])],
            [b'\x00\x80\x00\x16L', b'', bytes([True])]
        ]

    def tearDown(self):
        self.server.socket.close()
        self.server.context.term()

    def test_processing_requests_by_server(self):
        self.server.run()
        args_list = self.server.socket.send_multipart.call_args_list
        expected_result = [unittest.mock.call(i) for i in self.expected_sent_messages]
        self.assertCountEqual(args_list, expected_result)


class TestClientUniqueRequest(unittest.TestCase):
    def setUp(self):
        message_to_recv = bytes([True])
        self.client = client.Client("tcp://localhost:5799")
        self.client.socket.send_string = Mock()
        self.client.socket.recv = Mock(return_value=message_to_recv)

    def tearDown(self):
        self.client.socket.close()
        self.client.context.term()

    def test_processing_response_by_client(self):
        self.client.send_message_and_wait_for_response()
        self.assertNotEqual(self.client.response, None)
        self.assertTrue(self.client.response)


class TestClientNotUniqueRequest(unittest.TestCase):
    def setUp(self):
        message_to_recv = bytes([False])
        self.client = client.Client("tcp://localhost:5799")
        self.client.socket.send_string = Mock()
        self.client.socket.recv = Mock(return_value=message_to_recv)

    def tearDown(self):
        self.client.socket.close()
        self.client.context.term()

    def test_processing_response_by_client(self):
        self.client.send_message_and_wait_for_response()
        self.assertNotEqual(self.client.response, None)
        self.assertFalse(self.client.response)
