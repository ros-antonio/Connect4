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

    def check_winner(self, color):
        """
        Checks if the player with the given color has won the game.
        :param color: The color of the player given as a red dot or yellow dot.
        :return: True if the player has won the game, False otherwise.
        """
        board = self.__board.get_board()
        for i in range(6):
            for j in range(7):
                if board[i][j] == color:
                    if i + 3 < 6 and board[i + 1][j] == color and board[i + 2][j] == color and board[i + 3][j] == color:
                        return True
                    if j + 3 < 7 and board[i][j + 1] == color and board[i][j + 2] == color and board[i][j + 3] == color:
                        return True
                    if i + 3 < 6 and j + 3 < 7 and board[i + 1][j + 1] == color and board[i + 2][j + 2] == color and \
                            board[i + 3][j + 3] == color:
                        return True
                    if i + 3 < 6 and j - 3 >= 0 and board[i + 1][j - 1] == color and board[i + 2][j - 2] == color and \
                            board[i + 3][j - 3] == color:
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
        self.__board.place_piece(column, self.__current_player)
        if self.check_winner(self.__current_player):
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
                self.__board.place_piece(column, self.__current_player)
                if self.check_winner(self.__current_player):
                    return True
                self.__board.remove_piece(column)
            except InvalidMove:
                continue

        opponent = '\U0001F534' if self.__current_player == '\U0001F7E1' else '\U0001F7E1'
        for column in range(7):
            try:
                self.__board.place_piece(column, opponent)
                if self.check_winner(opponent):
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
                self.__board.place_piece(column, self.__current_player)
                if self.check_winner(self.__current_player):
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

    def get_current_player(self):
        return self.__current_player

    def get_board(self):
        return self.__board.get_board()

    def get_board_show(self):
        return str(self.__board)
