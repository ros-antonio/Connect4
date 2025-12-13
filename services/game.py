from domain.board import Board
from random import randint

from exceptions import InvalidMove


class Game:
    def __init__(self):
        """
        Initializes the game with a new board and the red dot as the first player.
        """
        self.__board = Board()
        self.__current_player = '\U0001F534'

    def check_winner(self, color, last_row, last_col):
        """
        Checks if the last move at (last_row, last_col) created a win.
        :param color: The color of the player given as a red dot or yellow dot.
        :param last_row: The row of the last move.
        :param last_col: The column of the last move.
        :return: True if the player has won the game, False otherwise.
        """
        board = self.__board.get_board()

        def count_direction(dr, dc):
            count = 0
            # 1. Look Forward
            r, c = last_row + dr, last_col + dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r][c] == color:
                count += 1
                r += dr
                c += dc

            # 2. Look Backward
            r, c = last_row - dr, last_col - dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r][c] == color:
                count += 1
                r -= dr
                c -= dc

            return count

        # Check all four directions
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            if count_direction(dr, dc) >= 3:
                return True

        return False

    def is_full(self):
        """
        Checks if the board is full (tie).
        :return: False if the board is not full, True otherwise.
        """
        board = self.__board.get_board()
        for i in range(6):
            for j in range(7):
                if board[i][j] == ' ':
                    return False
        return True

    def make_move(self, column):
        """
        Makes a human move on the board and switches the current player if the game is not over.
        :param column: The column on which the move has to be made.
        :return: True if the player has won the game, False otherwise.
        """
        row = self.__board.place_piece(column, self.__current_player)

        if self.check_winner(self.__current_player, row, column):
            return True

        self.__switch_player()
        return False

    def computer_move(self):
        """
        Makes a computer move on the board and switches the current player if the game is not over.
        If the computer can win the game, it will make the winning move.
        If the opponent can win the game, the computer will block the opponent.
        If none of the above, the computer will make a random move.
        :return: True if the computer has won the game, False otherwise.
        """
        for column in range(7):
            try:
                row = self.__board.place_piece(column, self.__current_player)
                if self.check_winner(self.__current_player, row, column):
                    return True
                self.__board.remove_piece(column)
            except InvalidMove:
                continue

        opponent = '\U0001F534' if self.__current_player == '\U0001F7E1' else '\U0001F7E1'
        for column in range(7):
            try:
                row = self.__board.place_piece(column, opponent)
                if self.check_winner(opponent, row, column):
                    self.__board.remove_piece(column)
                    self.__board.place_piece(column, self.__current_player)
                    self.__switch_player()
                    return False
                self.__board.remove_piece(column)
            except InvalidMove:
                continue

        while True:
            column = randint(0, 6)
            try:
                row = self.__board.place_piece(column, self.__current_player)
                if self.check_winner(self.__current_player, row, column):
                    return True
                self.__switch_player()
                return False
            except InvalidMove:
                continue

    def __switch_player(self):
        """
        Switches the current player.
        """
        self.__current_player = '\U0001F7E1' if self.__current_player == '\U0001F534' else '\U0001F534'

    def get_board(self):
        return self.__board.get_board()
