import copy
import os
import random

import colorama

from termcolor import colored

colorama.init()

GRID = [
    [None, None, None],
    [None, None, None],
    [None, None, None]]

ELEMENTS = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(1, 0), (1, 1), (1, 2)],
    [(0, 1), (1, 1), (2, 1)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)]]

CLEAR = "clear" if os.name == "posix" else "cls"

def clear():
    os.system(CLEAR)

def shuffled(iter):
    # return a randomly shuffled version of iter
    iter = list(iter)
    random.shuffle(iter)
    return iter

def similar(x, indexes):
    # check if elements are the same
    i, j = indexes[0]
    ref = x[3 * i + j]
    for index in indexes:
        i, j = index
        if x[3 * i + j] != ref:
            return False
    return True

def color(x, indexes):
    for i, j in indexes:
        x[3 * i + j] = colored(x[3 * i + j], "red")

def display(grid):
    x = [grid[i][j] or " " for i in range(3) for j in range(3)]
    #if the computer wins color the winning set
    for element in ELEMENTS:
        if similar(x, element):
            color(x, element)

    result = """
         1 | 2 | 3                       {} | {} | {}
        ---+---+---                     ---+---+---
         4 | 5 | 6                       {} | {} | {}
        ---+---+---                     ---+---+---
         7 | 8 | 9                       {} | {} | {}
    
        Choose a number : """.format(*x)

    clear()
    print(result, end="")

def win_player(grid, char):
    # check rows
    for i in range(3):
        if all(grid[i][j] == char for j in range(3)):
            return True
    # check columns
    for j in range(3):
        if all(grid[i][j] == char for i in range(3)):
            return True
    # check diagonals
    if all(grid[i][i] == char for i in range(3)):
        return True
    if all(grid[i][2 - i] == char for i in range(3)):
        return True

def coordinates(choice):
    # get row
    row = 3 - ((choice + 2) // 3)
    # get col
    col = (choice - 1) % 3
    return row, col

def terminal(grid):
    # player wins
    if win_player(grid, "X"):
        return True
    # computer wins
    if win_player(grid, "O"):
        return True
    # tie
    if all(grid[i][j] != None for i in range(3) for j in range(3)):
        return True
    # otherwise the game isn't over yet
    return False


def utility(grid):
    if win_player(grid, "X"):
        return -1
    if win_player(grid, "O"):
        return 1
    return 0


def actions(grid):
    result = []
    for i in shuffled(range(3)):
        for j in shuffled(range(3)):
            if grid[i][j] == None:
                result.append((i, j))
    return result


def minimax(grid, computer, alpha, beta):
    if terminal(grid):
        return utility(grid)

    if computer:
        func = max
        m = -float("inf")
        char = "O"
    else:
        func = min
        m = float("inf")
        char = "X"

    for action in actions(grid):
        i, j = action
        grid[i][j] = char
        value = minimax(grid, not computer, alpha, beta)
        m = func(m, value)
        # undo the move
        grid[i][j] = None
        # alpha-beta pruning
        if computer:
            alpha = func(alpha, m)
        else:
            beta = func(beta, m)

        if beta <= alpha:
            break

    return m


def best_move(grid):
    # find all empty cells and compute the minimax for each one
    alpha = -float("inf")
    beta = float("inf")
    m = -float("inf")
    for action in actions(grid):
        i, j = action
        grid[i][j] = "O"
        value = minimax(grid, False, alpha, beta)
        if value > m:
            result = (i, j)
            m = value
        # undo the move
        grid[i][j] = None
    return result


def get_user_input(grid):
    # ask for player input : a number between 1 and 9
    while True:
        display(grid)
        choice = input()
        # validate input
        if choice not in [str(i) for i in range(1, 10)]:
            continue
        choice = int(choice)
        i, j = coordinates(choice)
        if grid[i][j] != None:
            continue
        # if cell is not full : fill with 'X'
        grid[i][j] = "X"
        break


def game_loop(grid):
    while True:
        # player turn
        get_user_input(grid)
        display(grid)
        # check if the player wins
        if win_player(grid, "X"):
            print(colored("\n\tYou win!", "green"))
            break
        # check if it's a tie
        if terminal(grid):
            print(colored("\n\tTie!", "blue"))
            break
        # computer turn
        # find the best move to play
        i, j = best_move(grid)
        grid[i][j] = "O"
        # display the grid
        display(grid)
        # check if the computer wins with this choice
        if win_player(grid, "O"):
            print(colored("\n\tYou lose!", "red"))
            break


def play():
    while True:
        grid = copy.deepcopy(GRID)
        game_loop(grid)
        again = input("\tplay again ? [y/n] ")
        if again.upper() != "Y":
            break


if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print("\n\tkeyboard interrupt : abort")