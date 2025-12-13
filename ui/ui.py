from services.game import Game
from colorama import Fore, Style
from exceptions import InvalidMove


class Ui:
    def __init__(self):
        self.__game = Game()

    def print_intro(self):
        print(Fore.CYAN)
        print("\n\nWelcome to Connect Four!\n")
        print("You are the red player(\U0001F534). The computer is the yellow player(\U0001F7E1).\n")
        print("To make a move, enter a number between 0 and 6.\n")
        print("The first player to connect four pieces wins!\n")
        print("Good luck!\n\n")
        print(Style.RESET_ALL)

    def start(self):
        self.print_intro()
        while True:
            if self.__game.get_current_player() == '\U0001F534':
                print(self.__game.get_board_show())
                try:
                    column = int(input('Enter column: '))
                except ValueError:
                    print('Please enter an integer.\n')
                    continue
                try:
                    win = self.__game.make_move(column)
                except InvalidMove as er:
                    print(er)
                    continue
            else:
                try:
                    win = self.__game.computer_move()
                except InvalidMove as er:
                    print(er)
                    continue
            if win and self.__game.get_current_player() == '\U0001F534':
                print(Fore.GREEN + "\n\nYou won!\n\n" + Style.RESET_ALL)
                break
            elif win and self.__game.get_current_player() == '\U0001F7E1':
                print(Fore.RED + "\n\nComputer won!\n\n" + Style.RESET_ALL)
                break

            if self.__game.is_full():
                print(Fore.YELLOW + "\n\nIt's a draw!\n\n" + Style.RESET_ALL)
                break
        print(self.__game.get_board_show())
