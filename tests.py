# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:34:17 2023

@author: lpolakie
"""

import server
import unittest

class Test_get_adress_and_cord_from_message(unittest.TestCase):
    def setUp(self):
        self.message = [b'\x00\x00\x00\x12\xdb', b'', b'7,8']
        
    def test_get_adress_and_cord_from_message(self):
        adress, corrds = server.get_adress_and_cord_from_message(self.message)
        self.assertEqual(adress, b'\x00\x00\x00\x12\xdb')
        self.assertEqual(corrds, (7,8))
        
class zmq_double():
    ROUTER = None
    
    def Context(self):
        messages_to_send = [
                            [b'\x00\x80\x00\x16I', b'', b'6,9'], 
                            [b'\x00\x80\x00\x16J', b'', b'6,9'], 
                            [b'\x00\x80\x00\x16J', b'', b'1,2'], 
                            [b'\x00\x80\x00\x16K', b'', b'3,4'], 
                            [b'\x00\x80\x00\x16L', b'', b'5,6'],
                            ]
        self.messages_to_send = iter(messages_to_send)
        self.sended_messages = []
        return self
    
    def socket(self, socket_type):
        return self
    
    def bind(self, adress):
        pass
    
    def recv_multipart(self):
        return next(self.messages_to_send)
        
    def send_multipart(self, message):
        self.sended_messages.append(message)
        
    
class TestServer(unittest.TestCase):
    def setUp(self):
        server.zmq = zmq_double()
        self.expected_sended_messages = [
                                [b'\x00\x80\x00\x16I', b'', bytes([False])], 
                                [b'\x00\x80\x00\x16J', b'', bytes([False])], 
                                [b'\x00\x80\x00\x16J', b'', bytes([True])], 
                                [b'\x00\x80\x00\x16K', b'', bytes([True])], 
                                [b'\x00\x80\x00\x16L', b'', bytes([True])]
                                ]
    def test_processing_requests_by_server(self):
        my_server = server.Server("tcp://*:5799", number_of_clients=5)
        my_server.run()
        self.assertCountEqual(my_server.socket.sended_messages, self.expected_sended_messages)
