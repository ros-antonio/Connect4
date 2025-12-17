from unittest import TestCase
from services.game import Game
from domain.board import Board


class ServicesTest(TestCase):
    def setUp(self):
        self.__game = Game(difficulty='hard')

    def test_check_winner(self):
        self.__game.make_move(0)  # Red (Player = 1)
        self.__game.make_move(1)  # Yellow (Computer = -1)
        self.__game.make_move(0)  # Red
        self.__game.make_move(1)  # Yellow
        self.__game.make_move(0)  # Red
        self.__game.make_move(1)  # Yellow

        # Winning move
        self.__game.make_move(0)
        self.assertEqual(self.__game.check_winner(Board.PLAYER, 2, 0), True)

    def test_is_full(self):
        for i in range(6):
            for j in range(7):
                self.__game.make_move(j)
        self.assertEqual(self.__game.is_full(), True)

    def test_make_move(self):
        self.__game.make_move(0)
        self.assertEqual(self.__game.get_board()[5][0], Board.PLAYER)  # 1
        self.__game.make_move(1)
        self.assertEqual(self.__game.get_board()[5][1], Board.COMPUTER)  # -1

    def test_set_difficulty(self):
        # Test that setting difficulty doesn't crash
        self.__game.set_difficulty('easy')
        self.__game.set_difficulty('medium')
        self.__game.set_difficulty('hard')
        # Invalid input should be ignored (defaults to kept value)
        self.__game.set_difficulty('impossible')

    def test_computer_move_easy(self):
        # Easy mode just picks a random valid column.
        # We fill 6 columns, leaving only column 6 open.
        self.__game.set_difficulty('easy')

        for c in range(6):
            for _ in range(6):
                self.__game.make_move(c)

        # Now only column 6 is valid. Easy AI MUST pick it.
        self.__game.computer_move()
        self.assertEqual(self.__game.get_board()[5][6], Board.COMPUTER)  # -1

    def test_computer_move_medium_win(self):
        self.__game.set_difficulty('medium')

        # Setup: Yellow has 3 in a row horizontally
        self.__game.make_move(6) # Red (waster)
        self.__game.make_move(0) # Yellow
        self.__game.make_move(6) # Red
        self.__game.make_move(1) # Yellow
        self.__game.make_move(6) # Red
        self.__game.make_move(2) # Yellow
        self.__game.make_move(6) # Red (Turn passed to computer)

        # Medium AI should see the win at col 3
        self.__game.computer_move()
        self.assertEqual(self.__game.check_winner(Board.COMPUTER, 5, 3), True)  # -1

    def test_computer_move_medium_block(self):
        self.__game.set_difficulty('medium')

        # Setup: Red has 3 in a row, Yellow must block
        self.__game.make_move(0) # Red
        self.__game.make_move(6) # Yellow (waster)
        self.__game.make_move(1) # Red
        self.__game.make_move(6) # Yellow
        self.__game.make_move(2) # Red

        # Computer turn. Must block at col 3.
        self.__game.computer_move()
        self.assertEqual(self.__game.get_board()[5][3], Board.COMPUTER)  # -1

    def test_computer_move_medium_fallback(self):
        # If no win/block, it should just pick a random move (like easy)
        self.__game.set_difficulty('medium')
        self.__game.make_move(0) # Red

        self.__game.computer_move() # Yellow
        # Just check that a yellow piece exists somewhere
        board = self.__game.get_board()
        found = False
        for r in range(6):
            for c in range(7):
                if board[r][c] == Board.COMPUTER:  # -1
                    found = True
        self.assertTrue(found)

    def test_computer_move_hard_win(self):
        self.__game.set_difficulty('hard')
        # Set up a win for AI
        self.__game.make_move(1) # Red
        self.__game.make_move(0) # Yellow
        self.__game.make_move(1) # Red
        self.__game.make_move(0) # Yellow
        self.__game.make_move(1) # Red
        self.__game.make_move(0) # Yellow
        self.__game.make_move(6) # Red (Waste)

        self.__game.computer_move()
        self.assertEqual(self.__game.check_winner(Board.COMPUTER, 2, 0), True)  # -1

    def test_computer_move_hard_block(self):
        self.__game.set_difficulty('hard')
        # Setup threat for Red
        self.__game.make_move(1) # Red
        self.__game.make_move(6) # Yellow
        self.__game.make_move(1) # Red
        self.__game.make_move(4) # Yellow
        self.__game.make_move(1) # Red

        self.__game.computer_move()
        self.assertEqual(self.__game.get_board()[2][1], Board.COMPUTER)  # -1