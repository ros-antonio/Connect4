from exceptions import InvalidMove


class Board:
    # Constants for piece representation
    # 0 = empty/white, 1 = red/player, -1 = yellow/AI
    EMPTY = 0
    PLAYER = 1
    COMPUTER = -1

    def __init__(self):
        """
        Initializes the board with 6 rows and 7 columns using the EMPTY constant (0).
        """
        self.__board = [[self.EMPTY for _ in range(7)] for _ in range(6)]
        self.__col_heights = [5] * 7

    def place_piece(self, column, piece):
        """
        Places a piece on the board.
        """
        if column < 0 or column >= 7:
            raise InvalidMove('Out of bounds. Please choose a column between 0 and 6.\n')

        row = self.__col_heights[column]
        if row < 0:
            raise InvalidMove('Column is full. Please choose another column.\n')

        self.__board[row][column] = piece
        self.__col_heights[column] -= 1
        return row

    def remove_piece(self, column):
        """
        Removes a piece from the board (sets it back to EMPTY).
        """
        self.__col_heights[column] += 1
        row = self.__col_heights[column]
        self.__board[row][column] = self.EMPTY

    def get_board(self):
        return self.__board

    def set_board(self, new_board):
        self.__board = new_board
