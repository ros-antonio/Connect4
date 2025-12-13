from unittest import TestCase
from services.game import Game


class ServicesTest(TestCase):
    def setUp(self):
        self.__game = Game()

    def test_check_winner(self):
        # Create a vertical win for Red in column 0
        self.__game.make_move(0) # Red (Row 5)
        self.__game.make_move(1) # Yellow
        self.__game.make_move(0) # Red (Row 4)
        self.__game.make_move(1) # Yellow
        self.__game.make_move(0) # Red (Row 3)
        self.__game.make_move(1) # Yellow

        # The winning move: Red in Column 0, Row 2
        self.__game.make_move(0)

        # We manually verify if the game detects the win at (Row 2, Column 0)
        self.assertEqual(self.__game.check_winner('\U0001F534', 2, 0), True)

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
        # Set up a board where computer (Yellow) can win
        self.__game.make_move(1) # Red
        self.__game.make_move(0) # Yellow
        self.__game.make_move(1) # Red
        self.__game.make_move(0) # Yellow
        self.__game.make_move(1) # Red
        self.__game.make_move(0) # Yellow
        self.__game.make_move(6) # Red (Waste a move)

        # Computer should see the win in col 0, row 2
        self.__game.computer_move()
        self.assertEqual(self.__game.check_winner('\U0001F7E1', 2, 0), True)

    def test_computer_move_block(self):
        # Set up a threat for Red
        self.__game.make_move(1) # Red
        self.__game.make_move(6) # Yellow
        self.__game.make_move(1) # Red
        self.__game.make_move(4) # Yellow
        self.__game.make_move(1) # Red

        # Computer should block Red by playing in Column 1 (Row 2)
        self.__game.computer_move()
        self.assertEqual(self.__game.get_board()[2][1], '\U0001F7E1')