from services.game import Game
from exceptions import InvalidMove
import tkinter as tk
from tkinter import messagebox


class Gui:
    def __init__(self):
        self.board_labels = None
        self.buttons = None
        self.__game = Game()
        self.root = tk.Tk()
        self.root.title("Connect Four")
        self.create_widgets()

    def create_widgets(self):
        self.buttons = []
        for i in range(7):
            button = tk.Button(self.root, text=f"Column {i}", command=lambda i=i: self.make_move(i))
            button.grid(row=0, column=i)
            self.buttons.append(button)
        self.board_labels = [
            [tk.Label(self.root, text=" ", font=("Courier", 12), width=4, height=2, borderwidth=2, relief="groove") for
             _ in range(7)] for _ in range(6)]
        for i in range(6):
            for j in range(7):
                self.board_labels[i][j].grid(row=i + 1, column=j)

    def make_move(self, column):
        try:
            win = self.__game.make_move(column)
            self.update_board()
            if win:
                messagebox.showinfo("Game Over", "You won!")
                self.root.quit()
            elif self.__game.is_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.root.quit()
            else:
                self.computer_move()
        except InvalidMove as er:
            messagebox.showerror("Invalid Move", str(er))

    def computer_move(self):
        try:
            win = self.__game.computer_move()
            self.update_board()
            if win:
                messagebox.showinfo("Game Over", "Computer won!")
                self.root.quit()
        except InvalidMove as er:
            messagebox.showerror("Invalid Move", str(er))

    def update_board(self):
        board = self.__game.get_board()
        for i in range(6):
            for j in range(7):
                self.board_labels[i][j].config(text=board[i][j])

    def start(self):
        self.root.mainloop()
