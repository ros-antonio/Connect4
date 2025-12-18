from unittest import TestCase
from services.game import Game
from domain.board import Board

class ServicesTest(TestCase):
    def setUp(self):
        # Initialize with 'hard' to load the C++ engine by default
        self.__game = Game(difficulty='hard')

    def test_check_winner_vertical(self):
        """Test a vertical win (Red/Player)."""
        # Create a vertical stack for Player 1
        self.__game.make_move(0)  # Red
        self.__game.make_move(1)  # Yellow
        self.__game.make_move(0)  # Red
        self.__game.make_move(1)  # Yellow
        self.__game.make_move(0)  # Red
        self.__game.make_move(1)  # Yellow

        # Winning move
        self.__game.make_move(0)

        # Check if Player (1) won at row 2, col 0 (or wherever the top is)
        # Note: We check generic 'True' for win or specific player ID
        self.assertTrue(self.__game.check_winner(Board.PLAYER, 0, 0) or
                        self.__game.check_winner(Board.PLAYER, 3, 0))

    def test_is_full(self):
        """Test board fullness check."""
        for col in range(7):
            for _ in range(6):
                self.__game.make_move(col)
        self.assertTrue(self.__game.is_full())

    def test_make_move_updates_state(self):
        """Test that Python and C++ states stay synced."""
        self.__game.make_move(0) # Player
        # Board coordinates usually [row][col].
        # Assuming row 5 is bottom (standard matrix mapping) or row 0 is bottom.
        # We check that *some* piece landed in col 0.
        board = self.__game.get_board()

        # Check bottom-most or top-most row depending on your implementation
        piece_found = False
        for r in range(6):
            if board[r][0] == Board.PLAYER:
                piece_found = True
                break
        self.assertTrue(piece_found, "Player piece not found in column 0")

    def test_set_difficulty_all_levels(self):
        """Test that all 4 difficulties are accepted now."""
        # These should all work without error
        self.__game.set_difficulty('easy')
        self.__game.set_difficulty('medium')
        self.__game.set_difficulty('hard')

        # This is the NEW feature: Impossible should now be accepted
        try:
            self.__game.set_difficulty('impossible')
        except Exception as e:
            self.fail(f"Setting difficulty to 'impossible' raised an exception: {e}")

    def test_ai_easy_validity(self):
        """Test Easy AI (Random) always picks a valid column."""
        self.__game.set_difficulty('easy')

        # Fill first 6 columns completely
        for c in range(6):
            for _ in range(6):
                self.__game.make_move(c)

        # Only column 6 is open. Easy AI MUST pick it.
        self.__game.computer_move()

        board = self.__game.get_board()
        # Check that a Computer piece (-1) exists in the last column
        found_in_last_col = any(board[r][6] == Board.COMPUTER for r in range(6))
        self.assertTrue(found_in_last_col)

    def test_ai_medium_block(self):
        """Test Medium AI (Heuristic) blocks a simple win."""
        self.__game.set_difficulty('medium')

        # Setup: Red has 3 horizontal. Yellow MUST block.
        # R R R _
        self.__game.make_move(0) # Red
        self.__game.make_move(6) # Yellow (waste)
        self.__game.make_move(1) # Red
        self.__game.make_move(6) # Yellow (waste)
        self.__game.make_move(2) # Red

        # Computer turn
        self.__game.computer_move()

        # Check if Computer placed at col 3 (Blocking the win)
        board = self.__game.get_board()
        # Find the piece in col 3
        found_block = any(board[r][3] == Board.COMPUTER for r in range(6))
        self.assertTrue(found_block, "Medium AI failed to block immediate threat")

    def test_ai_hard_win_cpp(self):
        """Test Hard AI (C++ Engine) takes a winning move."""
        self.__game.set_difficulty('hard')

        # Setup vertical win opportunity for AI
        # P C
        # P C
        # P C
        # _ _
        for _ in range(3):
            self.__game.make_move(0) # Player (Col 0)
            self.__game.make_move(1) # Computer (Col 1)

        # Waste a player move so Computer can win
        self.__game.make_move(2)

        # Computer should place in Col 1 to win
        self.__game.computer_move()

        # Check winner
        # Note: We check if the game *detects* a winner immediately
        # We assume check_winner returns true if the last move won
        is_winner = False
        # Scan for 4 vertical in col 1
        board = self.__game.get_board()
        consecutive = 0
        for r in range(6):
            if board[r][1] == Board.COMPUTER:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive == 4:
                is_winner = True

        self.assertTrue(is_winner, "Hard AI (C++) missed a vertical win")

    def test_ai_impossible_response(self):
        """Test that Impossible AI (C++ Depth 9) actually returns a move."""
        self.__game.set_difficulty('impossible')

        # Make a move
        self.__game.make_move(3)

        # Ask C++ for a move (this might take 0.5s - 1s)
        self.__game.computer_move()

        # Just assert that the piece count increased
        board = self.__game.get_board()
        piece_count = sum(row.count(Board.COMPUTER) for row in board)
        self.assertEqual(piece_count, 1, "Impossible AI did not make a move")