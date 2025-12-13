from unittest import TestCase
from services.game import Game


class ServicesTest(TestCase):
    def setUp(self):
        self.__game = Game()

    def test_check_winner(self):
        self.__game.make_move(0)
        self.__game.make_move(1)
        self.__game.make_move(0)
        self.__game.make_move(1)
        self.__game.make_move(0)
        self.__game.make_move(1)
        self.__game.make_move(0)
        self.assertEqual(self.__game.check_winner('\U0001F534'), True)

    def test_is_full(self):
        for i in range(6):
            for j in range(7):
                self.__game.make_move(j)
        self.assertEqual(self.__game.is_full(), True)

    def test_make_move(self):
        self.__game.make_move(0)
        self.assertEqual(self.__game.get_board()[5][0], '\U0001F534')
        self.__game.make_move(1)
        self.assertEqual(self.__game.get_board()[5][1], '\U0001F7E1')

    def test_computer_move_win(self):
        self.__game.make_move(1)
        self.__game.make_move(0)
        self.__game.make_move(1)
        self.__game.make_move(0)
        self.__game.make_move(1)
        self.__game.make_move(0)
        self.__game.make_move(6)
        self.__game.computer_move()
        self.assertEqual(self.__game.check_winner('\U0001F7E1'), True)

    def test_computer_move_block(self):
        self.__game.make_move(1)
        self.__game.make_move(6)
        self.__game.make_move(1)
        self.__game.make_move(4)
        self.__game.make_move(1)
        self.__game.computer_move()
        self.assertEqual(self.__game.get_board()[2][1], '\U0001F7E1')
