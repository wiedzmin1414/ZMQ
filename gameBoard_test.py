import unittest
import gameBoard


class TestPosition(unittest.TestCase):
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
