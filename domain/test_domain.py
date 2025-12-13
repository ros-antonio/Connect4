from unittest import TestCase
from domain.board import Board
from exceptions import InvalidMove


class DomainTest(TestCase):
    def setUp(self):
        self.__board = Board()

    def test_place_piece(self):
        self.__board.place_piece(0, 'X')
        new_board = [[' ' for _ in range(7)] for _ in range(6)]
        new_board[5][0] = 'X'
        self.assertEqual(self.__board.get_board(), new_board)

    def test_place_piece_out_of_bounds(self):
        try:
            self.__board.place_piece(7, 'X')
            assert False
        except InvalidMove:
            assert True

    def test_place_piece_column_full(self):
        for _ in range(6):
            self.__board.place_piece(0, 'X')
        try:
            self.__board.place_piece(0, 'X')
            assert False
        except InvalidMove:
            assert True

    def test_remove_piece(self):
        self.__board.place_piece(0, 'X')
        self.__board.remove_piece(0)
        new_board = [[' ' for _ in range(7)] for _ in range(6)]
        self.assertEqual(self.__board.get_board(), new_board)
