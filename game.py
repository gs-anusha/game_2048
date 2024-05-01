import random
import numpy as np
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QMessageBox, QTableWidgetItem
from pyqt_interface import Ui_MainWindow

# temp_board = np.array([[4, 64, 2, 4], [32, 2, 1024, 1024], [64, 32, 8, 4], [2, 8, 4, 2]])


class Game2048:
    def __init__(self):
        self.board_size = 4
        self.current_board = self.initial_board()
        self.game_over = False

    def initial_board(self):
        board = np.zeros((4, 4), dtype=int)

        i = 2
        while i > 0:
            row_num = random.randint(0, self.board_size - 1)
            col_num = random.randint(0, self.board_size - 1)
            if board[row_num][col_num] == 0:
                board[row_num][col_num] = self.pick_input()
                i -= 1

        return board

    def pick_input(self):
        if random.randint(1, 10) == 1:
            return 4
        else:
            return 2

    def zeroes_on_board(self, board):
        zero_indices = [(i, j) for i in range(self.board_size) for j in
                        range(self.board_size) if board[i][j] == 0]
        return zero_indices

    def add_num(self, board):
        zero_indices = self.zeroes_on_board(board)

        chosen_index = random.choice(zero_indices)
        row_num, col_num = chosen_index

        board[row_num][col_num] = self.pick_input()

        return board

    def move_left(self, row):
        i = 0
        j = 0
        while i < len(row):
            if row[i] != 0:
                if row[j] == 0:
                    row[j] = row[i]
                    row[i] = 0
                j += 1
            i += 1

        return row

    def compare(self, A, B):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if A[i][j] == B[i][j]:
                    continue
                else:
                    return False

        return True

    def merge_one_row_left(self, row):
        row = self.move_left(row)
        for i in range(len(row)-1):
            if row[i] == row[i+1]:
                row[i] *= 2
                row[i+1] = 0

        return self.move_left(row)

    def merge_board_left(self, board):
        for row in board:
            row = self.merge_one_row_left(row)

        return board

    def merge_board_right(self, board):
        for i in range(self.board_size):
            board[i] = self.merge_one_row_left(board[i][::-1])[::-1]

        return board

    def merge_board_up(self, board):
        return self.merge_board_left(board.T).T

    def merge_board_down(self, board):
        return self.merge_board_right(board.T).T

    def possible_merges(self, board):
        temp = board.copy()
        if self.compare(board, self.merge_board_left(temp)) or self.compare(board, self.merge_board_right(temp)) or \
                self.compare(board, self.merge_board_up(temp)) or self.compare(board, self.merge_board_down(temp)):
            return False
        return True

    def handle_merge_board_left(self, board):
        return self.merge_board_left(board)

    def handle_merge_board_right(self, board):
        return self.merge_board_right(board)

    def handle_merge_board_up(self, board):
        return self.merge_board_up(board)

    def handle_merge_board_down(self, board):
        return self.merge_board_down(board)


class TerminalUI:
    def __init__(self, game):
        self.game = game

    def display_t(self, board):
        for row in board:
            current = "|"
            for element in row:
                if element == 0:
                    current += "    |"
                else:
                    current += str(element) + " " * (4 - len(str(element))) + "|"
            print(current)

    def start_game(self):
        info = "\nTo move left type L \nTo move right type R \nTo move up type U \nTo move down type D"
        print(info)
        if self.game.game_over:
            print("GAME OVER")
        else:
            self.display_t(self.game.current_board)
            instruction = input("make your move\n").upper()
            temp = self.game.current_board.copy()
            if instruction == "L":
                temp = self.game.merge_board_left(temp)
            elif instruction == "R":
                temp = self.game.merge_board_right(temp)
            elif instruction == "U":
                temp = self.game.merge_board_up(temp)
            elif instruction == "D":
                temp = self.game.merge_board_down(temp)
            else:
                print("Try again")
                self.start_game()

            largest = np.max(temp)
            if largest == 2048:
                self.display_t(temp)
                print("You Win")

            else:
                if not self.game.compare(self.game.current_board, temp):
                    temp = self.game.add_num(temp)
                else:
                    if self.game.zeroes_on_board(temp):
                        print("Invalid move try again")
                    else:
                        if self.game.possible_merges(temp):
                            print("Invalid move try again")
                        else:
                            self.game.game_over = True

                self.game.current_board = temp
                self.start_game()


class QtUI(QMainWindow, Ui_MainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.setupUi(self)
        self.setWindowTitle("2048 Game")

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.moves = QButtonGroup()
        self.init_ui()

        self.start_game()

    def init_ui(self):

        self.moves.addButton(self.rb_left)
        self.moves.addButton(self.rb_right)
        self.moves.addButton(self.rb_up)
        self.moves.addButton(self.rb_down)

        self.rb_left.clicked.connect(self.start_game)
        self.rb_right.clicked.connect(self.start_game)
        self.rb_up.clicked.connect(self.start_game)
        self.rb_down.clicked.connect(self.start_game)

        self.restart.clicked.connect(self.restart_game)

    def display_qt(self, board):

        self.game_board.clear()

        self.game_board.setRowCount(self.game.board_size)
        self.game_board.setColumnCount(self.game.board_size)

        self.game_board.horizontalHeader().setVisible(False)
        self.game_board.verticalHeader().setVisible(False)

        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                value = board[i][j]
                item = QTableWidgetItem(str(value))
                if value != 0:
                    item.setBackground(QtGui.QColor(255, 200, 0))
                else:
                    item.setBackground(QtGui.QColor(230, 220, 210))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.game_board.setItem(i, j, item)

    def show_message(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("2048 Game")
        msg.setText(message)
        msg.exec_()

    def clear_selection(self):
        self.moves.setExclusive(False)
        for button in self.moves.buttons():
            button.setChecked(False)
        self.moves.setExclusive(True)

    def set_square_cells(self):
        for i in range(game.board_size):
            self.game_board.setRowHeight(i, self.game_board.height() // self.game.board_size)
            self.game_board.setColumnWidth(i, self.game_board.width() // self.game.board_size)

        self.game_board.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.game_board.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def start_game(self):
        self.display_qt(self.game.current_board)
        self.set_square_cells()

        if self.game.game_over:
            self.show_message("Game Over")
        else:
            selected_button = self.moves.checkedButton()

            if selected_button is None:
                return

            direction_map = {
                self.rb_left: self.game.handle_merge_board_left,
                self.rb_right: self.game.handle_merge_board_right,
                self.rb_up: self.game.handle_merge_board_up,
                self.rb_down: self.game.handle_merge_board_down
            }

            handle_function = direction_map[selected_button]

            temp = self.game.current_board.copy()
            temp = handle_function(temp)

            largest = np.max(temp)
            if largest == 2048:
                self.display_qt(temp)
                self.show_message("You Win")
                self.restart_game()
            else:
                if not self.game.compare(self.game.current_board, temp):
                    temp = self.game.add_num(temp)
                else:
                    if self.game.zeroes_on_board(temp):
                        self.show_message("Invalid move try again")
                    else:
                        if self.game.possible_merges(temp):
                            self.show_message("Invalid move try again")
                        else:
                            self.game.game_over = True

                self.game.current_board = temp
                self.display_qt(self.game.current_board)
                self.clear_selection()

    def restart_game(self):
        self.game.current_board = self.game.initial_board()
        self.game.game_over = False
        self.clear_selection()
        self.start_game()


if __name__ == '__main__':
    game = Game2048()  # Create an instance of Game2048
    ui = input("Choose your interface. Type terminal or qt\n").lower()
    if ui == "terminal":
        terminal_ui = TerminalUI(game)  # Pass the Game2048 instance to TerminalUI
        terminal_ui.start_game()
    elif ui == "qt":
        app = QApplication(sys.argv)
        qt_ui = QtUI(game)  # Pass the Game2048 instance to QtUI
        qt_ui.show()
        sys.exit(app.exec_())

