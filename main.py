''''
1. Create function to merge single row left - done
2. Create function to merge board left - done
3. Create function to reverse row - done
4. Create function to merge right - done
5. create function to transpose board - done
6. create function to merge up - done
7. create function to merge down - done
8. create function for game - done
9. create function to make intial board - done
10. create function to display the board - done
11. check if 2048 achieved - done
12. create function to see if game over - done
'''

import random
import numpy as np
import os

# temp_board = np.array([[4, 64, 2, 4], [32, 2, 1024, 1024], [64, 32, 8, 4], [2, 8, 4, 2]])
board_size = 4


def pick_input():
    if random.randint(1, 10) == 1:
        return 4
    else:
        return 2


def initial_board():
    board = np.zeros((4, 4), dtype=int)

    i = 2
    while i > 0:
        row_num = random.randint(0, board_size - 1)
        col_num = random.randint(0, board_size - 1)
        board[row_num][col_num] = pick_input()
        i -= 1

    return board


def zeroes_on_board(board):
    zero_indices = [(i, j) for i in range(board_size) for j in range(board_size) if board[i][j] == 0]
    return zero_indices


def add_num(board):
    zero_indices = zeroes_on_board(board)

    chosen_index = random.choice(zero_indices)
    row_num, col_num = chosen_index

    board[row_num][col_num] = pick_input()

    return board


def move_left(row):
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


def compare(A, B):
    for i in range(board_size):
        for j in range(board_size):
            if A[i][j] == B[i][j]:
                continue
            else:
                return False

    return True


def merge_one_row_left(row):
    row = move_left(row)
    for i in range(len(row)-1):
        if row[i] == row[i+1]:
            row[i] *= 2
            row[i+1] = 0

    return move_left(row)


def display(board):
    for row in board:
        current = "|"
        for element in row:
            if element == 0:
                current += "    |"
            else:
                current += str(element) + " "*(4-len(str(element))) + "|"
        print(current)


def merge_board_left(board):
    for row in board:
        row = merge_one_row_left(row)

    return board


def merge_board_right(board):
    for i in range(board_size):
        board[i] = merge_one_row_left(board[i][::-1])[::-1]

    return board


def merge_board_up(board):
    return merge_board_left(board.T).T


def merge_board_down(board):
    return merge_board_right(board.T).T


def possible_merges(board):
    temp = board.copy()
    if compare(board, merge_board_left(temp)) or compare(board, merge_board_right(temp)) or \
            compare(board, merge_board_up(temp)) or compare(board, merge_board_down(temp)):
        return False
    return True


def start_game(current_board=initial_board(), game_over=False):
    info = "\nTo move left type L \nTo move right type R \nTo move up type U \nTo move down type D"
    print(info)
    if game_over:
        print("GAME OVER")
    else:
        display(current_board)
        instruction = input("make your move\n").upper()
        temp = current_board.copy()
        if instruction == "L":
            temp = merge_board_left(temp)
        elif instruction == "R":
            temp = merge_board_right(temp)
        elif instruction == "U":
            temp = merge_board_up(temp)
        elif instruction == "D":
            temp = merge_board_down(temp)
        else:
            print("Try again")
            start_game(current_board=current_board)

        largest = np.max(temp)
        if largest == 2048:
            display(temp)
            print("You Win")

        else:
            if not compare(current_board, temp):
                temp = add_num(temp)
            else:
                if zeroes_on_board(temp):
                    print("Invalid move try again")
                else:
                    if possible_merges(temp):
                        print("Invalid move try again")
                    else:
                        game_over = True

            start_game(current_board=temp, game_over=game_over)


start_game()
