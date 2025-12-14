import tkinter as tk
from tkinter import messagebox
from services.game import Game
from exceptions import InvalidMove
from domain.board import Board

# Constants for piece representation
KEY_PLAYER = 'red'
KEY_COMPUTER = 'yellow'
KEY_EMPTY = Board.EMPTY

# Mapping piece characters to colors
PIECE_MAP = {
    KEY_PLAYER: 'red',
    KEY_COMPUTER: 'yellow',
    KEY_EMPTY: 'white'
}


class Gui:
    """Manages the graphical user interface for the Connect Four game using Tkinter.
    Handles user input, rendering the board, and game state updates."""

    def __init__(self):
        """Initializes the main GUI window and game state."""
        self.root = tk.Tk()
        self.root.title("Connect Four")
        self.root.resizable(False, False)

        self.rows = 6
        self.cols = 7
        self.cell_size = 100
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size

        self.difficulty_var = tk.StringVar(value="hard")
        self.__game = None
        self.__ghost = None

        self.start_new_game()
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        """Creates the menu bar with game options and difficulty settings."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Game Menu (New Game, Exit)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.start_new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Game", menu=game_menu)

        # Difficulty Menu (Easy, Medium, Hard) - can be changed anytime in the game
        diff_menu = tk.Menu(menubar, tearoff=0)
        diff_menu.add_radiobutton(label="Easy", variable=self.difficulty_var, value="easy",
                                  command=self.change_difficulty)
        diff_menu.add_radiobutton(label="Medium", variable=self.difficulty_var, value="medium",
                                  command=self.change_difficulty)
        diff_menu.add_radiobutton(label="Hard", variable=self.difficulty_var, value="hard",
                                  command=self.change_difficulty)
        menubar.add_cascade(label="Difficulty", menu=diff_menu)

    def create_widgets(self):
        """Creates the main canvas for the game board."""
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg='blue',
            highlightthickness=0
        )
        self.canvas.pack()
        # Bind mouse click for making moves
        self.canvas.bind("<Button-1>", self.handle_click)
        # Bind mouse motion for hover effect + leave event
        self.canvas.bind("<Motion>", self.__handle_hover)
        self.canvas.bind("<Leave>", self.__handle_leave)
        self.draw_board()

    def start_new_game(self):
        """Starts a new game with the selected difficulty."""
        current_diff = self.difficulty_var.get()
        self.__game = Game(difficulty=current_diff)
        if hasattr(self, 'canvas'):
            self.draw_board()

    def change_difficulty(self):
        """Changes the game's difficulty setting."""
        new_diff = self.difficulty_var.get()
        self.__game.set_difficulty(new_diff)

    def draw_board(self):
        """Draws the current state of the game board on the canvas."""
        self.canvas.delete("all")
        self.__ghost = None
        board = self.__game.get_board()

        for r in range(self.rows):
            for c in range(self.cols):
                x0 = c * self.cell_size
                y0 = r * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size

                piece_char = board[r][c]
                color = PIECE_MAP.get(piece_char, 'white')

                self.canvas.create_oval(
                    x0 + 10, y0 + 10,
                    x1 - 10, y1 - 10,
                    fill=color, outline="black", width=2
                )

    def handle_click(self, event):
        """Handles mouse click events to make a move."""
        column = event.x // self.cell_size
        self.make_move(column)

    def make_move(self, column):
        """Attempts to make a move in the specified column for the player, then triggers the computer's move."""
        try:
            win = self.__game.make_move(column)
            self.draw_board()

            if win:
                self.game_over("You won!")
            elif self.__game.is_full():
                self.game_over("It's a draw!")
            else:
                self.root.after(500, self.computer_move)

        except InvalidMove:
            pass

    def computer_move(self):
        """Triggers the computer's move and checks for game over conditions."""
        try:
            win = self.__game.computer_move()
            self.draw_board()

            if win:
                self.game_over("Computer won!")
            elif self.__game.is_full():
                self.game_over("It's a draw!")
        except InvalidMove as er:
            print(f"Computer Error: {er}")

    def __handle_hover(self, event):
        """Calculates where the piece would drop and draws a ghost piece."""
        col = event.x // self.cell_size
        if 0 <= col < self.cols:
            self.__draw_ghost(col)

    def __handle_leave(self, event):
        """Removes the ghost piece when the mouse leaves the canvas."""
        if self.__ghost:
            self.canvas.delete(self.__ghost)
            self.__ghost = None

    def __draw_ghost(self, col):
        """Finds the lowest empty row in the column and draws a transparent piece."""
        if self.__ghost:
            self.canvas.delete(self.__ghost)
            self.__ghost = None

        board = self.__game.get_board()
        target_row = -1

        for r in reversed(range(self.rows)):
            if board[r][col] == KEY_EMPTY:
                target_row = r
                break

        if target_row != -1:
            x0 = col * self.cell_size
            y0 = target_row * self.cell_size
            x1 = x0 + self.cell_size
            y1 = y0 + self.cell_size

            # Draw ghost piece (white with player-colored outline)
            self.__ghost = self.canvas.create_oval(
                x0 + 10, y0 + 10,
                x1 - 10, y1 - 10,
                fill="",
                outline=PIECE_MAP[KEY_PLAYER],
                width=4
            )

    def game_over(self, message):
        """Displays a game over message and prompts to play again."""
        answer = messagebox.askyesno("Game Over", f"{message}\nDo you want to play again?")
        if answer:
            self.start_new_game()
        else:
            self.root.quit()

    def start(self):
        self.root.mainloop()
