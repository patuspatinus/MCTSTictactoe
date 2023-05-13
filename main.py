import numpy as np
from nodes import *
from search import MonteCarloTreeSearch
from tictactoe import *


def init():
    state = np.zeros((10, 10))
    initial_board_state = TicTacToeGameState(state=state, next_to_move=1)
    root = MonteCarloTreeSearchNode(state=initial_board_state, parent=None)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(initial_board_state,3)
    c_state = best_node.state
    c_board = c_state.board
    # move = get_action(initial_board_state)
    # c_state = initial_board_state.move(move)
    # c_board = c_state.board
    return c_state,c_board


def graphics(board):
    for i in range(10):
        print("")
        print("{0:10}".format(i).center(8)+"|", end='')
        for j in range(10):
            if c_board[i][j] == 0:
                print('_'.center(8), end='')
            if c_board[i][j] == 1:
                print('X'.center(8), end='')
            if c_board[i][j] == -1:
                print('O'.center(8), end='')
    print("")
    print("______________________________")


def get_action(state):
    while True:
        try:
            location = input("Your move (format: row,column): ")
            row, column = map(int, location.split(","))
            move = TicTacToeMove(row, column, -1)
            if state.is_move_legal(move):
                return move
            else:
                print("Invalid move. Please try again.")
        except ValueError:
            print("Invalid input. Please enter the move in the correct format (row,column).")
        except Exception as e:
            print("An error occurred:", str(e))

def judge(state):
    if state.is_game_over():
        if state.game_result == 1.0:
            print("You lose!")
        if state.game_result == 0.0:
            print("Tie!")
        if state.game_result == -1.0:
            print("You Win!")
        return 1
    else:
        return -1


c_state,c_board = init()
graphics(c_board)


while True:
    move1 = get_action(c_state)
    c_state = c_state.move(move1)
    c_board = c_state.board
    graphics(c_board)

    board_state = TicTacToeGameState(state=c_board, next_to_move=1)
    root = MonteCarloTreeSearchNode(state=board_state, parent=None)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(board_state,3)
    best_move = best_node.state.last_move

    x_coordinate = best_move.x_coordinate
    y_coordinate = best_move.y_coordinate
    print(x_coordinate,y_coordinate)
    c_state = best_node.state
    c_board = c_state.board
    graphics(c_board)

    # move1 = get_action(c_state)
    # c_state = c_state.move(move1)
    # c_board = c_state.board
    # graphics(c_board)
    if judge(c_state)==1:
        break
    elif judge(c_state)==-1:
        continue