from unittest import TestCase
from domain.board import Board
from exceptions import InvalidMove


class DomainTest(TestCase):
    def setUp(self):
        self.__board = Board()

    def test_place_piece(self):
        self.__board.place_piece(0, Board.PLAYER)

        new_board = [[Board.EMPTY for _ in range(7)] for _ in range(6)]
        new_board[5][0] = Board.PLAYER

        self.assertEqual(self.__board.get_board(), new_board)

    def test_place_piece_out_of_bounds(self):
        with self.assertRaises(InvalidMove):
            self.__board.place_piece(7, Board.PLAYER)

    def test_place_piece_column_full(self):
        for _ in range(6):
            self.__board.place_piece(0, Board.PLAYER)

        with self.assertRaises(InvalidMove):
            self.__board.place_piece(0, Board.PLAYER)

    def test_remove_piece(self):
        self.__board.place_piece(0, Board.PLAYER)
        self.__board.remove_piece(0)

        new_board = [[Board.EMPTY for _ in range(7)] for _ in range(6)]
        self.assertEqual(self.__board.get_board(), new_board)