import unittest
import gameBoard
from unittest.mock import Mock


class TestPosition(unittest.TestCase):
    def test_copy(self):
        position = gameBoard.Position(5, 5)
        position_copy = position.copy()
        position_copy.move('w')
        self.assertEqual(position.y, 5)
        self.assertEqual(position_copy.y, 4)

    def test_position_move_up_when_move_is_available(self):
        position = gameBoard.Position(5, 5)
        position.move_up()
        self.assertEqual(position.x, 5)
        self.assertEqual(position.y, 4)

    def test_position_move_down_when_move_is_available(self):
        position = gameBoard.Position(5, 5)
        position.move_down()
        self.assertEqual(position.x, 5)
        self.assertEqual(position.y, 6)

    def test_position_move_left_when_move_is_available(self):
        position = gameBoard.Position(5, 5)
        position.move_left()
        self.assertEqual(position.x, 4)
        self.assertEqual(position.y, 5)

    def test_position_move_right_when_move_is_available(self):
        position = gameBoard.Position(5, 5)
        position.move_right()
        self.assertEqual(position.x, 6)
        self.assertEqual(position.y, 5)

    def test_eq_operator(self):
        position1 = gameBoard.Position(5, 5)
        position2 = gameBoard.Position(5, 5)
        self.assertEqual(position1, position2)

    def test_in_operator_on_list(self):
        position = gameBoard.Position(5, 5)
        list_of_position = [gameBoard.Position(5, 5), gameBoard.Position(4, 5)]
        self.assertTrue(position in list_of_position)

    def test_return_neighboring_positions(self):
        position = gameBoard.Position(5, 5)
        list_of_neighboring_positions = position.return_neighboring_positions()
        output_positions = [gameBoard.Position(4, 4), gameBoard.Position(4, 5), gameBoard.Position(4, 6),
                            gameBoard.Position(5, 4),                           gameBoard.Position(5, 6),
                            gameBoard.Position(6, 4), gameBoard.Position(6, 5), gameBoard.Position(6, 6)]
        self.assertEqual(len(list_of_neighboring_positions), len(output_positions))
        for pos in list_of_neighboring_positions:
            self.assertTrue(pos in output_positions)

    def test_is_neighbor_when_points_are_neighbors(self):
        position1 = gameBoard.Position(5, 5)
        position2 = gameBoard.Position(5, 5)
        self.assertTrue(position1.is_neighbor(position2))
        position1 = gameBoard.Position(5, 5)
        position2 = gameBoard.Position(5, 6)
        self.assertTrue(position1.is_neighbor(position2))
        position1 = gameBoard.Position(4, 6)
        position2 = gameBoard.Position(5, 5)
        self.assertTrue(position1.is_neighbor(position2))

    def test_is_neighbor_when_points_are_not_neighbors(self):
        position1 = gameBoard.Position(5, 5)
        position2 = gameBoard.Position(5, 3)
        self.assertFalse(position1.is_neighbor(position2))
        position1 = gameBoard.Position(5, 5)
        position2 = gameBoard.Position(3, 3)
        self.assertFalse(position1.is_neighbor(position2))
        position1 = gameBoard.Position(4, 8)
        position2 = gameBoard.Position(2, 8)
        self.assertFalse(position1.is_neighbor(position2))
        position1 = gameBoard.Position(0, 0)
        position2 = gameBoard.Position(1, 2)
        self.assertFalse(position1.is_neighbor(position2))


class TestBoardGame(unittest.TestCase):
    def test_of_comp_max_players_numbers(self):
        board = gameBoard.GameBoard(10, 10)
        self.assertEqual(board.max_players, 9)
        board = gameBoard.GameBoard(12, 10)
        self.assertEqual(board.max_players, 12)
        board = gameBoard.GameBoard(5, 10)
        self.assertEqual(board.max_players, 3)
        board = gameBoard.GameBoard(100, 100)
        self.assertEqual(board.max_players, 33*33)

    def test_is_position_in_board_when_position_is_in_the_middle_of_the_board(self):
        board = gameBoard.GameBoard(10, 10)
        position = gameBoard.Position(5, 5)
        self.assertTrue(board.is_position_in_board(position))
        position = gameBoard.Position(4, 7)
        self.assertTrue(board.is_position_in_board(position))
        position = gameBoard.Position(8, 2)
        self.assertTrue(board.is_position_in_board(position))

    def test_is_position_in_board_when_position_is_on_the_edge_of_the_board(self):
        board = gameBoard.GameBoard(10, 10)
        position = gameBoard.Position(0, 9)
        self.assertTrue(board.is_position_in_board(position))
        position = gameBoard.Position(0, 0)
        self.assertTrue(board.is_position_in_board(position))
        position = gameBoard.Position(9, 9)
        self.assertTrue(board.is_position_in_board(position))
        position = gameBoard.Position(9, 0)
        self.assertTrue(board.is_position_in_board(position))
        position = gameBoard.Position(0, 5)
        self.assertTrue(board.is_position_in_board(position))
        position = gameBoard.Position(5, 9)
        self.assertTrue(board.is_position_in_board(position))

    def test_is_position_in_board_when_position_is_out_of_the_board(self):
        board = gameBoard.GameBoard(10, 10)
        position = gameBoard.Position(0, 10)
        self.assertFalse(board.is_position_in_board(position))
        position = gameBoard.Position(10, 0)
        self.assertFalse(board.is_position_in_board(position))
        position = gameBoard.Position(-3, 9)
        self.assertFalse(board.is_position_in_board(position))
        position = gameBoard.Position(9, 110)
        self.assertFalse(board.is_position_in_board(position))
        position = gameBoard.Position(2, 15)
        self.assertFalse(board.is_position_in_board(position))
        position = gameBoard.Position(5, -9)
        self.assertFalse(board.is_position_in_board(position))

    def test_add_exactly_one_client(self):
        board = gameBoard.GameBoard(10, 10)
        client_name = "client1"
        board.add_client(client_name)
        client_position = board.get_client_position(client_name)
        self.assertTrue(board.is_position_in_board(client_position))
        self.assertEqual(len(board.not_available_positions_to_spawn), 9)

    def test_add_exactly_two_clients(self):
        board = gameBoard.GameBoard(10, 10)
        client_name1 = "client1"
        client_name2 = "client2"
        board.add_client(client_name1)
        client_position1 = board.get_client_position(client_name1)
        self.assertTrue(board.is_position_in_board(client_position1))
        self.assertEqual(len(board.not_available_positions_to_spawn), 9)
        board.add_client(client_name2)
        client_position2 = board.get_client_position(client_name2)
        self.assertTrue(board.is_position_in_board(client_position2))
        self.assertEqual(len(board.not_available_positions_to_spawn), 18)
        self.assertFalse(client_position1.is_neighbor(client_position2))

    def test_add_two_client_when_second_one_is_requesting_to_be_next_to_first_one(self):
        # first client will take position (2,2), second client will try to
        # take positions (2,2) and (2,3), and after that he will get (5,5)
        gameBoard.random.randint = Mock(side_effect=[2, 2, 2, 2, 2, 3, 5, 5])

        board = gameBoard.GameBoard(10, 10)
        client_name1 = "client1"
        client_name2 = "client2"
        board.add_client(client_name1)
        client_position1 = board.get_client_position(client_name1)
        self.assertEqual(client_position1.x, 2)
        self.assertEqual(client_position1.y, 2)
        board.add_client(client_name2)
        client_position2 = board.get_client_position(client_name2)
        self.assertEqual(client_position2.x, 5)
        self.assertEqual(client_position2.y, 5)

    def test_try_to_add_10_clients_to_board_7x7_max_players_is_equals_to_4(self):
        board = gameBoard.GameBoard(7, 7)
        gameBoard.random.randint = Mock(side_effect=[0, 0, 2, 2, 2, 4, 2, 6, 4, 0, 4, 2, 4, 4, 4, 6, 6, 0, 6, 2])
        clients = [f"client{number}" for number in range(10)]
        for client in clients:
            board.add_client(client)
        self.assertEqual(board.number_of_players, 4)

    def test_process_requests_with_one_clients_when_moves_are_legal(self):
        gameBoard.random.randint = Mock(side_effect=[2, 2])
        board = gameBoard.GameBoard(10, 10)
        client = "client1"
        board.add_client(client)
        request = {"client1": 's'}
        for i in range(5):
            board.process_request(request)
            position = board.get_client_position(client)
            self.assertEqual(position.y, 3+i)

    def test_process_requests_with_one_clients_hitting_wall_going_up_on_board(self):
        gameBoard.random.randint = Mock(side_effect=[2, 3])
        board = gameBoard.GameBoard(10, 10)
        client = "client1"
        board.add_client(client)
        request = {"client1": 'w'}
        for i in range(5):
            board.process_request(request)
            position = board.get_client_position(client)
            self.assertEqual(position.y, max(0, 2-i))

    def test_process_requests_with_one_clients_hitting_wall_going_left_on_board(self):
        gameBoard.random.randint = Mock(side_effect=[4, 3])
        board = gameBoard.GameBoard(10, 10)
        client = "client1"
        board.add_client(client)
        request = {"client1": 'a'}
        for i in range(5):
            board.process_request(request)
            position = board.get_client_position(client)
            self.assertEqual(position.x, max(0, 3-i))

    def test_process_requests_with_two_clients_when_they_try_to_go_to_the_same_position_vertically(self):
        gameBoard.random.randint = Mock(side_effect=[2, 2, 2, 6])

        board = gameBoard.GameBoard(10, 10)
        client1 = "client1"
        client2 = "client2"
        board.add_client(client1)
        board.add_client(client2)
        request = {client1: 's', client2: 'w'}
        for i in range(5):
            board.process_request(request)
            client1_position = board.get_client_position(client1)
            client2_position = board.get_client_position(client2)
            # print(f"Client1: {client1_position}; client2: {client2_position}")
            self.assertEqual(client1_position.y, 3)
            self.assertEqual(client2_position.y, 5)

    def test_process_requests_with_two_clients_when_they_try_to_go_to_the_same_position_horizontally(self):
        gameBoard.random.randint = Mock(side_effect=[2, 2, 6, 2])

        board = gameBoard.GameBoard(10, 10)
        client1 = "client1"
        client2 = "client2"
        board.add_client(client1)
        board.add_client(client2)
        request = {client1: 'r', client2: 'l'}
        for i in range(5):
            board.process_request(request)
            client1_position = board.get_client_position(client1)
            client2_position = board.get_client_position(client2)
            # print(f"Client1: {client1_position}; client2: {client2_position}")
            self.assertEqual(client1_position.x, 3)
            self.assertEqual(client2_position.x, 5)

    def test_process_requests_with_two_clients_when_they_try_to_go_to_the_same_position_diagonally(self):
        gameBoard.random.randint = Mock(side_effect=[4, 4, 6, 6])

        board = gameBoard.GameBoard(10, 10)
        client1 = "client1"
        client2 = "client2"
        board.add_client(client1)
        board.add_client(client2)
        request = {client1: 'r', client2: 'w'}
        for i in range(5):
            board.process_request(request)
            client1_position = board.get_client_position(client1)
            client2_position = board.get_client_position(client2)
            # print(f"Client1: {client1_position}; client2: {client2_position}")
            self.assertEqual(client1_position.x, 5)
            self.assertEqual(client2_position.y, 5)

    def test_process_request_check_if_output_is_ok_when_client_hit_wall(self):
        gameBoard.random.randint = Mock(side_effect=[4, 5])
        board = gameBoard.GameBoard(10, 10)
        client = "client1"
        board.add_client(client)
        request = {client: 'w'}
        for i in range(10):
            process_output = board.process_request(request)
            output = process_output[client]
            client1_position = board.get_client_position(client)
            # print(f"Client1: {client1_position}")
            expected_output = 'ok' if i < 5 else 'nok'
            # print(f"iteration {i}, process_output should be equal {expected_output}, real value: {output}")
            self.assertEqual(output, expected_output)

    def test_process_request_when_four_clients_hits_the_wall(self):
        gameBoard.random.randint = Mock(side_effect=[0, 0, 0, 9, 9, 0, 9, 9])
        board = gameBoard.GameBoard(10, 10)
        clients = [f"client{number}" for number in range(4)]
        for client in clients:
            board.add_client(client)
        requests = {'client0': 'w',
                    'client1': 'l',
                    'client2': 'r',
                    'client3': 's'}
        for i in range(5):
            board.process_request(requests)
            self.assertEqual(board.get_client_position('client0').x, 0)
            self.assertEqual(board.get_client_position('client0').y, 0)
            self.assertEqual(board.get_client_position('client1').x, 0)
            self.assertEqual(board.get_client_position('client1').y, 9)
            self.assertEqual(board.get_client_position('client2').x, 9)
            self.assertEqual(board.get_client_position('client2').y, 0)
            self.assertEqual(board.get_client_position('client3').x, 9)
            self.assertEqual(board.get_client_position('client3').y, 9)

    def test_returning_position_for_one_client(self):
        gameBoard.random.randint = Mock(side_effect=[4, 5])
        board = gameBoard.GameBoard(10, 10)
        client = 'client'
        board.add_client(client)
        client_position = board.get_positions(client)
        expected_position = gameBoard.Position(4, 5)
        self.assertIn(expected_position, client_position)

    def test_returning_position_for_three_client(self):
        gameBoard.random.randint = Mock(side_effect=[4, 5, 2, 1, 3, 7])
        board = gameBoard.GameBoard(10, 10)
        clients = [f'client{number}' for number in range(3)]
        for client in clients:
            board.add_client(client)
        positions = board.get_positions('client0')
        client_position = positions[0]
        other_positions = positions[1:]
        client_expected_position = gameBoard.Position(4, 5)
        other_expected_positions = [gameBoard.Position(2, 1), gameBoard.Position(3, 7)]
        self.assertEqual(client_expected_position, client_position)
        self.assertCountEqual(other_positions, other_expected_positions)

    def test_process_requests_when_there_is_one_client_and_he_requests_for_positions(self):
        gameBoard.random.randint = Mock(side_effect=[6, 7])
        board = gameBoard.GameBoard(10, 10)
        client = 'client'
        board.add_client(client)
        requests = {client: 'p'}
        output = board.process_request(requests)
        expected_output = [gameBoard.Position(6, 7)]
        self.assertEqual(expected_output, output[client])

    def test_process_requests_when_there_are_3_clients_and_everyone_request_for_positions(self):
        gameBoard.random.randint = Mock(side_effect=[4, 5, 2, 1, 3, 7])
        board = gameBoard.GameBoard(10, 10)
        clients = [f'client{number}' for number in range(3)]
        requests = {}
        for client in clients:
            board.add_client(client)
            requests[client] = 'p'
        output = board.process_request(requests)
        expected_output = [gameBoard.Position(4, 5), gameBoard.Position(2, 1), gameBoard.Position(3, 7)]
        for number, client in enumerate(clients):
            client_output = output[client]
            self.assertEqual(client_output[0], expected_output[number])
            other_positions = expected_output[:number] + expected_output[number+1:]
            self.assertCountEqual(client_output[1:], other_positions)
