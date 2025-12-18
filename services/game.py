from random import choice
import connect4_core

from domain.board import Board
from exceptions import InvalidMove


class Game:
    """
    Manages the core logic of the Connect Four game.
    Handles turn management, move validation, win detection, and the AI opponent.
    """

    def __init__(self, difficulty='hard'):
        """
        Initializes the game with a board, players, and difficulty level.

        :param difficulty: The initial difficulty level for the AI ('easy', 'medium', 'hard', 'impossible').
                           Defaults to 'hard' if an invalid value is provided.
        """
        self.__board = Board()
        # Initialize C++ core
        self.__cpp_engine = connect4_core.Connect4Core()
        # Constants for player representation (using Board constants)
        self.PLAYER_KEY = Board.PLAYER  # 1 (red)
        self.COMPUTER_KEY = Board.COMPUTER  # -1 (yellow)
        self.__current_player = self.PLAYER_KEY
        # Ensure valid difficulty, default to 'hard' if invalid
        self.__difficulty = difficulty if difficulty in ['easy', 'medium', 'hard', 'impossible'] else 'hard'
        # for AI last move tracking
        self.__last_move = None

    def set_difficulty(self, level):
        """
        Updates the difficulty level of the AI. Can be called anytime during the game.

        :param level: The desired difficulty level ('easy', 'medium', 'hard', 'impossible').
        """
        if level in ['easy', 'medium', 'hard', 'impossible']:
            self.__difficulty = level

    def check_winner(self, piece, last_row, last_col):
        """
        Checks if the last move created a winning condition (4 in a row).
        Optimized to check only around the last placed piece.
        This function is kept for the medium AI logic, as the hard AI uses the C++ engine.

        :param piece: The piece value that was just placed (1 for player, -1 for AI).
        :param last_row: The row index of the last placed piece.
        :param last_col: The column index of the last placed piece.
        :return: True if the move resulted in a win, False otherwise.
        """
        board = self.__board.get_board()

        def count_direction(dr, dc):
            """
            Counts consecutive pieces of the same value in a given direction from the starting point.

            :param dr: direction row
            :param dc: direction column
            :return: number of consecutive pieces in that direction
            """
            count = 0
            # Check in the positive direction
            r, c = last_row + dr, last_col + dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r][c] == piece:
                count += 1
                r += dr
                c += dc

            # Check in the negative direction
            r, c = last_row - dr, last_col - dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r][c] == piece:
                count += 1
                r -= dr
                c -= dc
            return count

        # Check all four directions
        if count_direction(0, 1) >= 3: return True
        if count_direction(1, 0) >= 3: return True
        if count_direction(1, 1) >= 3: return True
        if count_direction(1, -1) >= 3: return True
        return False

    def is_full(self):
        """
        Checks if the board is full (draw condition).

        :return: True if the board is full, False otherwise.
        """
        board = self.__board.get_board()
        for i in range(6):
            for j in range(7):
                if board[i][j] == Board.EMPTY:
                    return False
        return True

    def make_move(self, column):
        """
        Executes a player's move in the specified column.

        :param column: The column index where the player wants to place their piece.
        :return: True if the move results in a win, False otherwise.
        :raises InvalidMove: If the move is invalid (e.g., column full or out of bounds).
        """
        row = self.__board.place_piece(column, self.__current_player)
        self.__cpp_engine.make_move(column, self.__current_player)
        if self.__cpp_engine.check_winner(self.__current_player, row, column):
            return True
        self.__switch_player()
        return False

    def computer_move(self):
        """
        Executes the AI's move based on the current difficulty level.

        :return: True if the move results in a win, False otherwise.
        """
        if self.__difficulty == 'easy':
            col = self.__get_easy_move()
        elif self.__difficulty == 'medium':
            col = self.__get_medium_move()
        elif self.__difficulty == 'hard':
            col = self.__get_hard_move()
        else:
            col = self.__get_impossible_move()

        row = self.__board.place_piece(col, self.__current_player)
        self.__last_move = (row, col)

        self.__cpp_engine.make_move(col, self.__current_player)

        if self.__cpp_engine.check_winner(self.__current_player, row, col):
            return True
        self.__switch_player()
        return False

    # --- AI Move Strategies ---

    def __get_easy_move(self):
        """
        Selects a random valid column for the AI to place its piece.

        :return: A valid column index, or -1 if no valid moves are available.
        """
        valid_columns = [c for c in range(7) if self.__board.get_board()[0][c] == Board.EMPTY]
        if not valid_columns:
            return -1
        return choice(valid_columns)

    def __get_medium_move(self):
        """
        Strategy:
        1. Check for a winning move and take it.
        2. Check if the opponent has a winning move next turn and block it.
        3. If neither, pick a random valid move.

        :return: A valid column index for the AI's move.
        """
        # 1. Try to win
        for col in range(7):
            try:
                row = self.__board.place_piece(col, self.__current_player)
                if self.check_winner(self.__current_player, row, col):
                    self.__board.remove_piece(col)
                    return col
                self.__board.remove_piece(col)
            except InvalidMove:
                continue

        # 2. Block opponent
        opponent = self.PLAYER_KEY
        for col in range(7):
            try:
                row = self.__board.place_piece(col, opponent)
                if self.check_winner(opponent, row, col):
                    self.__board.remove_piece(col)
                    return col
                self.__board.remove_piece(col)
            except InvalidMove:
                continue

        return self.__get_easy_move()

    def __get_hard_move(self):
        """
        Uses the C++ Minimax engine for maximum performance.

        :return: A valid column index for the AI's move.
        """
        # Calling C++ engine's minimax function
        score, col = self.__cpp_engine.get_best_move(5, self.COMPUTER_KEY)
        return col

    def __get_impossible_move(self):
        """
        Uses the C++ Minimax engine for maximum performance.

        :return: A valid column index for the AI's move.
        """
        # Calling C++ engine's minimax function
        score, col = self.__cpp_engine.get_best_move(9, self.COMPUTER_KEY)
        return col

    def __switch_player(self):
        """
        Switches the current player between the human player and the computer.
        """
        if self.__current_player == self.PLAYER_KEY:
            self.__current_player = self.COMPUTER_KEY
        else:
            self.__current_player = self.PLAYER_KEY

    def get_board(self):
        """
        Retrieves the current state of the board.

        :return: The current board as a 2D list.
        """
        return self.__board.get_board()

    def set_board(self, new_board):
        self.__board.set_board(new_board)
        self.__cpp_engine.reset()
        # Rebuild C++ engine state
        for r in range(5, -1, -1):
            for c in range(7):
                piece = new_board[r][c]
                if piece != Board.EMPTY:
                    self.__cpp_engine.make_move(c, piece)

    def get_last_move(self):
        return self.__last_move
