import math
from random import choice

from domain.board import Board
from exceptions import InvalidMove


class Game:
    def __init__(self):
        self.__board = Board()
        self.__current_player = '\U0001F534'
        self.__computer_color = '\U0001F7E1'
        self.__difficulty = 'hard'

    def set_difficulty(self, level):
        """
        Sets the difficulty of the AI.
        :param level: 'easy', 'medium', or 'hard'
        """
        if level in ['easy', 'medium', 'hard']:
            self.__difficulty = level

    def check_winner(self, color, last_row, last_col):
        """
        Checks if the last move at (last_row, last_col) created a win.
        """
        board = self.__board.get_board()

        def count_direction(dr, dc):
            count = 0
            r, c = last_row + dr, last_col + dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r][c] == color:
                count += 1
                r += dr
                c += dc

            r, c = last_row - dr, last_col - dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r][c] == color:
                count += 1
                r -= dr
                c -= dc
            return count

        # Check all 4 axes
        if count_direction(0, 1) >= 3: return True
        if count_direction(1, 0) >= 3: return True
        if count_direction(1, 1) >= 3: return True
        if count_direction(1, -1) >= 3: return True
        return False

    def is_full(self):
        board = self.__board.get_board()
        for i in range(6):
            for j in range(7):
                if board[i][j] == ' ':
                    return False
        return True

    def make_move(self, column):
        """
        Makes a human move.
        """
        row = self.__board.place_piece(column, self.__current_player)
        if self.check_winner(self.__current_player, row, column):
            return True
        self.__switch_player()
        return False

    def computer_move(self):
        """
        Determines the move based on difficulty and executes it.
        """
        col = -1

        if self.__difficulty == 'easy':
            col = self.__get_easy_move()
        elif self.__difficulty == 'medium':
            col = self.__get_medium_move()
        else:
            col = self.__get_hard_move()

        row = self.__board.place_piece(col, self.__current_player)
        if self.check_winner(self.__current_player, row, col):
            return True
        self.__switch_player()
        return False

    def __get_easy_move(self):
        """Returns a random valid column."""
        valid_columns = [c for c in range(7) if self.__board.get_board()[0][c] == ' ']
        if not valid_columns:
            return -1
        return choice(valid_columns)

    def __get_medium_move(self):
        """
        1. Win if possible.
        2. Block opponent if they can win.
        3. Random otherwise.
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
        opponent = '\U0001F534'
        for col in range(7):
            try:
                row = self.__board.place_piece(col, opponent)
                if self.check_winner(opponent, row, col):
                    self.__board.remove_piece(col)
                    return col
                self.__board.remove_piece(col)
            except InvalidMove:
                continue

        # 3. Random fallback
        return self.__get_easy_move()

    def __get_hard_move(self):
        """Uses Minimax with Alpha-Beta Pruning."""
        score, col = self.__minimax(6, -math.inf, math.inf, True)
        return col

    # --- MINIMAX ENGINE ---

    def __minimax(self, depth, alpha, beta, maximizing_player):
        # 1. Get valid locations
        valid_locations = [c for c in range(7) if self.__board.get_board()[0][c] == ' ']

        # 2. Check Terminal States (Win/Draw) or Depth Limit
        if depth == 0 or len(valid_locations) == 0:
            return self.__evaluate_board(), None

        # 3. Recursion
        if maximizing_player:
            value = -math.inf
            best_col = valid_locations[0]
            for col in valid_locations:
                row = self.__board.place_piece(col, self.__computer_color)

                if self.check_winner(self.__computer_color, row, col):
                    self.__board.remove_piece(col)
                    return 1000000 + depth, col

                new_score, _ = self.__minimax(depth - 1, alpha, beta, False)

                self.__board.remove_piece(col)

                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_col

        else:
            value = math.inf
            best_col = valid_locations[0]
            opponent = '\U0001F534'
            for col in valid_locations:
                row = self.__board.place_piece(col, opponent)

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
                    break
            return value, best_col

    def __evaluate_board(self):
        """
        Optimized Heuristic: Checks Center + Windows.
        """
        score = 0
        board = self.__board.get_board()

        my_color = self.__computer_color
        opp_color = '\U0001F534' if my_color == '\U0001F7E1' else '\U0001F7E1'

        # 1. Center Column Preference
        center_array = [row[3] for row in board]
        center_count = center_array.count(my_color)
        score += center_count * 3

        # 2. Scan all windows
        # Horizontal
        for r in range(6):
            for c in range(4):
                score += self.__evaluate_window_optimized(board, r, c, 0, 1, my_color, opp_color)

        # Vertical
        for c in range(7):
            for r in range(3):
                score += self.__evaluate_window_optimized(board, r, c, 1, 0, my_color, opp_color)

        # Positive Diagonal (/)
        for r in range(3):
            for c in range(4):
                score += self.__evaluate_window_optimized(board, r, c, 1, 1, my_color, opp_color)

        # Negative Diagonal (\)
        for r in range(3, 6):
            for c in range(4):
                score += self.__evaluate_window_optimized(board, r, c, -1, 1, my_color, opp_color)

        return score

    @staticmethod
    def __evaluate_window_optimized(board, r, c, dr, dc, color, opp_color):
        """
        Scans a window defined by start (r, c) and direction (dr, dc).
        Calculates gravity only when necessary.
        """
        score = 0
        window = [board[r + i * dr][c + i * dc] for i in range(4)]

        my_count = window.count(color)
        empty_count = window.count(' ')
        opp_count = window.count(opp_color)

        if my_count == 4:
            score += 100
        elif my_count == 3 and empty_count == 1:
            empty_i = window.index(' ')
            val_r = r + empty_i * dr
            val_c = c + empty_i * dc
            if val_r == 5 or board[val_r + 1][val_c] != ' ':
                score += 5
        elif my_count == 2 and empty_count == 2:
            score += 2

        if opp_count == 3 and empty_count == 1:
            empty_i = window.index(' ')
            val_r = r + empty_i * dr
            val_c = c + empty_i * dc
            if val_r == 5 or board[val_r + 1][val_c] != ' ':
                score -= 80

        return score

    def __switch_player(self):
        """
        Switches the current player.
        """
        self.__current_player = '\U0001F7E1' if self.__current_player == '\U0001F534' else '\U0001F534'

    def get_board(self):
        return self.__board.get_board()
