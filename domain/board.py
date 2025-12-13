from exceptions import InvalidMove


class Board:
    def __init__(self):
        """
        Initializes the board with 6 rows and 7 columns.
        """
        self.__board = [[' ' for _ in range(7)] for _ in range(6)]

    def place_piece(self, column, piece):
        """
        Places a piece on the board.
        :param column: The column on which the piece has to be put.
        :param piece: The piece to be put on the board. (red dot or yellow dot)
        :raises InvalidMove: If the column is full or out of bounds.
        """
        if column < 0 or column >= 7:
            raise InvalidMove('Out of bounds. Please choose a column between 0 and 6.\n')

        for row in reversed(range(6)):
            if self.__board[row][column] == ' ':
                self.__board[row][column] = piece
                return
        raise InvalidMove('Column is full. Please choose another column.\n')

    def remove_piece(self, column):
        """
        Removes a piece from the board.
        :param column: The column from which the piece has to be removed.
        """
        for row in range(6):
            if self.__board[row][column] != ' ':
                self.__board[row][column] = ' '
                return

    def get_board(self):
        return self.__board
