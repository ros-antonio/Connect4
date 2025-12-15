from exceptions import InvalidMove

class Board:
    # Constant for readability
    EMPTY = 'empty'

    def __init__(self):
        """
        Initializes the board with 6 rows and 7 columns using the EMPTY constant.
        """
        self.__board = [[self.EMPTY for _ in range(7)] for _ in range(6)]

    def place_piece(self, column, piece):
        """
        Places a piece on the board.
        """
        if column < 0 or column >= 7:
            raise InvalidMove('Out of bounds. Please choose a column between 0 and 6.\n')

        for row in reversed(range(6)):
            if self.__board[row][column] == self.EMPTY:
                self.__board[row][column] = piece
                return row
        raise InvalidMove('Column is full. Please choose another column.\n')

    def remove_piece(self, column):
        """
        Removes a piece from the board (sets it back to EMPTY).
        """
        for row in range(6):
            if self.__board[row][column] != self.EMPTY:
                self.__board[row][column] = self.EMPTY
                return

    def get_board(self):
        return self.__board

    def set_board(self, new_board):
        self.__board = new_board