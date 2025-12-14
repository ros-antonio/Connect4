import math
from random import choice

from domain.board import Board
from exceptions import InvalidMove


class Game:
    def __init__(self, difficulty):
        self.__board = Board()
        self.PLAYER_KEY = 'red'
        self.COMPUTER_KEY = 'yellow'
        self.__current_player = self.PLAYER_KEY
        self.__difficulty = difficulty if difficulty in ['easy', 'medium', 'hard'] else 'hard'

    def set_difficulty(self, level):
        if level in ['easy', 'medium', 'hard']:
            self.__difficulty = level

    def check_winner(self, color, last_row, last_col):
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

        if count_direction(0, 1) >= 3: return True
        if count_direction(1, 0) >= 3: return True
        if count_direction(1, 1) >= 3: return True
        if count_direction(1, -1) >= 3: return True
        return False

    def is_full(self):
        board = self.__board.get_board()
        for i in range(6):
            for j in range(7):
                if board[i][j] == Board.EMPTY:
                    return False
        return True

    def make_move(self, column):
        row = self.__board.place_piece(column, self.__current_player)
        if self.check_winner(self.__current_player, row, column):
            return True
        self.__switch_player()
        return False

    def computer_move(self):
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
        valid_columns = [c for c in range(7) if self.__board.get_board()[0][c] == Board.EMPTY]
        if not valid_columns:
            return -1
        return choice(valid_columns)

    def __get_medium_move(self):
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
        score, col = self.__minimax(6, -math.inf, math.inf, True)
        return col

    def __minimax(self, depth, alpha, beta, maximizing_player):
        valid_locations = [c for c in range(7) if self.__board.get_board()[0][c] == Board.EMPTY]

        if self.__has_winning_position(self.COMPUTER_KEY):
            return 1000000 + depth, None
        elif self.__has_winning_position(self.PLAYER_KEY):
            return -1000000 - depth, None

        if depth == 0 or len(valid_locations) == 0:
            return self.__evaluate_board(), None

        if maximizing_player:
            value = -math.inf
            best_col = choice(valid_locations)
            for col in valid_locations:
                row = self.__board.place_piece(col, self.COMPUTER_KEY)
                if self.check_winner(self.COMPUTER_KEY, row, col):
                    self.__board.remove_piece(col)
                    return 1000000 + depth, col
                new_score, _ = self.__minimax(depth - 1, alpha, beta, False)
                self.__board.remove_piece(col)
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta: break
            return value, best_col
        else:
            value = math.inf
            best_col = choice(valid_locations)
            opponent = self.PLAYER_KEY
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
                if alpha >= beta: break
            return value, best_col

    def __evaluate_board(self):
        score = 0
        board = self.__board.get_board()
        my_color = self.COMPUTER_KEY
        opp_color = self.PLAYER_KEY

        center_array = [row[3] for row in board]
        center_count = center_array.count(my_color)
        score += center_count * 3

        for r in range(6):
            for c in range(4):
                score += self.__evaluate_window_optimized(board, r, c, 0, 1, my_color, opp_color)
        for c in range(7):
            for r in range(3):
                score += self.__evaluate_window_optimized(board, r, c, 1, 0, my_color, opp_color)
        for r in range(3):
            for c in range(4):
                score += self.__evaluate_window_optimized(board, r, c, 1, 1, my_color, opp_color)
        for r in range(3, 6):
            for c in range(4):
                score += self.__evaluate_window_optimized(board, r, c, -1, 1, my_color, opp_color)
        return score

    @staticmethod
    def __evaluate_window_optimized(board, r, c, dr, dc, color, opp_color):
        score = 0
        window = [board[r + i * dr][c + i * dc] for i in range(4)]
        my_count = window.count(color)
        empty_count = window.count(Board.EMPTY)
        opp_count = window.count(opp_color)

        if my_count == 4: score += 100
        elif my_count == 3 and empty_count == 1: score += 5
        elif my_count == 2 and empty_count == 2: score += 2

        if opp_count == 3 and empty_count == 1: score -= 80

        return score

    def __has_winning_position(self, color):
        board = self.__board.get_board()
        for r in range(6):
            for c in range(4):
                if all(board[r][c + i] == color for i in range(4)): return True
        for r in range(3):
            for c in range(7):
                if all(board[r + i][c] == color for i in range(4)): return True
        for r in range(3):
            for c in range(4):
                if all(board[r + i][c + i] == color for i in range(4)): return True
        for r in range(3, 6):
            for c in range(4):
                if all(board[r - i][c + i] == color for i in range(4)): return True
        return False

    def __switch_player(self):
        if self.__current_player == self.PLAYER_KEY:
            self.__current_player = self.COMPUTER_KEY
        else:
            self.__current_player = self.PLAYER_KEY

    def get_board(self):
        return self.__board.get_board()