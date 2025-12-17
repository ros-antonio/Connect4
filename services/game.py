import math
from random import choice

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

        :param difficulty: The initial difficulty level for the AI ('easy', 'medium', 'hard').
                           Defaults to 'hard' if an invalid value is provided.
        """
        self.__board = Board()

        # Constants for player representation (using Board constants)
        self.PLAYER_KEY = Board.PLAYER  # 1 (red)
        self.COMPUTER_KEY = Board.COMPUTER  # -1 (yellow)
        self.__current_player = self.PLAYER_KEY
        # Ensure valid difficulty, default to 'hard' if invalid
        self.__difficulty = difficulty if difficulty in ['easy', 'medium', 'hard'] else 'hard'
        # for AI last move tracking
        self.__last_move = None
        self.__transposition_table = {}

    def set_difficulty(self, level):
        """
        Updates the difficulty level of the AI. Can be called anytime during the game.

        :param level: The desired difficulty level ('easy', 'medium', 'hard').
        """
        if level in ['easy', 'medium', 'hard']:
            self.__difficulty = level

    def check_winner(self, piece, last_row, last_col):
        """
        Checks if the last move created a winning condition (4 in a row).
        Optimized to check only around the last placed piece.

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
        if self.check_winner(self.__current_player, row, column):
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
        else:
            col = self.__get_hard_move()

        row = self.__board.place_piece(col, self.__current_player)

        self.__last_move = (row, col)

        if self.check_winner(self.__current_player, row, col):
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
        Uses the Minimax algorithm with alpha-beta pruning to select the optimal move.

        :return: A valid column index for the AI's move.
        """
        # Minimax to depth 6 for a balance between performance and decision quality
        score, col = self.__minimax(7, -math.inf, math.inf, True)
        return col

    def __minimax(self, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning.

        :param depth: How many moves ahead to evaluate.
        :param alpha: Alpha value for pruning (best already explored option along the path to the root for maximizer).
        :param beta: Beta value for pruning (best already explored option along the path to the root for minimizer).
        :param maximizing_player: True if it's the AI's turn (maximize score), False if it's the player's turn (minimize score).
        :return: A tuple of (score, column) representing the best score and corresponding column.
        """
        valid_locations = [c for c in range(7) if self.__board.get_board()[0][c] == Board.EMPTY]
        # Prioritize center columns for better performance, improves pruning efficiency
        search_order = [3, 2, 4, 1, 5, 0, 6]
        valid_locations.sort(key=lambda x: search_order.index(x))

        board_tuple = tuple(tuple(row) for row in self.__board.get_board())
        state_key = (board_tuple, maximizing_player)

        # If we've seen this exact board at a deeper or equal depth, use the saved score
        if state_key in self.__transposition_table:
            stored_depth, stored_score = self.__transposition_table[state_key]
            if stored_depth >= depth:
                return stored_score, None

        if depth == 0 or len(valid_locations) == 0:
            return self.__evaluate_board(), None

        if maximizing_player:
            value = -math.inf
            best_col = valid_locations[0]
            for col in valid_locations:
                row = self.__board.place_piece(col, self.COMPUTER_KEY)
                # Check for immediate win, optimize by returning early
                if self.check_winner(self.COMPUTER_KEY, row, col):
                    self.__board.remove_piece(col)
                    return 1000000 + depth, col

                new_score, _ = self.__minimax(depth - 1, alpha, beta, False)
                self.__board.remove_piece(col)

                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cut-off
            self.__transposition_table[state_key] = (depth, value)
            return value, best_col
        else:
            value = math.inf
            best_col = valid_locations[0]
            opponent = self.PLAYER_KEY
            for col in valid_locations:
                row = self.__board.place_piece(col, opponent)
                # Check for immediate loss, optimize by returning early
                if self.check_winner(opponent, row, col):
                    self.__board.remove_piece(col)
                    return -1000000 - depth, col

                new_score, _ = self.__minimax(depth - 1, alpha, beta, True)
                self.__board.remove_piece(col)

                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cut-off
            self.__transposition_table[state_key] = (depth, value)
            return value, best_col

    def __evaluate_board(self):
        """
        Heuristic evaluation function.
        Assigns a score to the board state based on the number of potential winning lines.

        :return: The board evaluation score
        """
        score = 0
        board = self.__board.get_board()
        my_piece = self.COMPUTER_KEY  # -1
        opp_piece = self.PLAYER_KEY  # 1

        # Score center column higher (statistically better position)
        center_count = 0
        for r in range(6):
            if board[r][3] == my_piece:
                center_count += 1
        score += center_count * 3

        # Score all possible windows of 4
        # Horizontal
        for r in range(6):
            for c in range(4):
                score += self.__evaluate_window_optimized(board, r, c, 0, 1, my_piece, opp_piece)
        # Vertical
        for c in range(7):
            for r in range(3):
                score += self.__evaluate_window_optimized(board, r, c, 1, 0, my_piece, opp_piece)
        # Diagonal (positive slope)
        for r in range(3):
            for c in range(4):
                score += self.__evaluate_window_optimized(board, r, c, 1, 1, my_piece, opp_piece)
        # Diagonal (negative slope)
        for r in range(3, 6):
            for c in range(4):
                score += self.__evaluate_window_optimized(board, r, c, -1, 1, my_piece, opp_piece)
        return score

    @staticmethod
    def __evaluate_window_optimized(board, r, c, dr, dc, my_piece, opp_piece):
        """
        Scores a specific window of 4 cells.

        :param board: current board state
        :param r: row
        :param c: column
        :param dr: direction row
        :param dc: direction column
        :param my_piece: AI piece value (-1)
        :param opp_piece: Opponent piece value (1)
        :return: score for the window
        """
        my_count = 0
        opp_count = 0
        empty_count = 0

        for i in range(4):
            val = board[r + i * dr][c + i * dc]
            if val == my_piece:
                my_count += 1
            elif val == opp_piece:
                opp_count += 1
            else:
                empty_count += 1

        score = 0
        if my_count == 4:
            score += 100
        elif my_count == 3 and empty_count == 1:
            score += 5
        elif my_count == 2 and empty_count == 2:
            score += 2

        # Penalize opponent's potential wins
        if opp_count == 3 and empty_count == 1:
            score -= 80

        return score

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

    def get_last_move(self):
        return self.__last_move
