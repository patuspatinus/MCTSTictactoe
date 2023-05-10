import numpy as np


class TicTacToeMove(object):
    def __init__(self, x_coordinate, y_coordinate, value):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value

    def __repr__(self):
        return "x:" + str(self.x_coordinate) + " y:" + str(self.y_coordinate) + " v:" + str(self.value)


class TicTacToeGameState(object):
    x = 1
    o = -1

    def __init__(self, state, next_to_move=1):
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Please play on 2D square board")
        self.board = state
        self.board_size = state.shape[0]
        self.next_to_move = next_to_move

    @property
    def game_result(self):
        # wining_position = [[0,1,2,3,4],[1,2,3,4,5],[2,3,4,5,6],[3,4,5,6,7],[4,5,6,7,8],[5,6,7,8,9]]
        # #checkrow
        # for pst in range (self.board_size):
        #     for pst1 in range(6):
        #         if (str(self.board[pst][wining_position[pst1][0]]) + str(self.board[pst][wining_position[pst1][1]])
        #                 + str(self.board[pst][wining_position[pst1][2]]) + str(self.board[pst][wining_position[pst1][3]])
        #                 + str(self.board[pst][wining_position[pst1][4]]) == "11111"):
        #             return 1.
        # for pst in range(self.board_size):
        #     for pst1 in range(6):
        #         if (str(self.board[pst][wining_position[pst1][0]]) + str(self.board[pst][wining_position[pst1][1]])
        #                 + str(self.board[pst][wining_position[pst1][2]]) + str(self.board[pst][wining_position[pst1][3]])
        #                 + str(self.board[pst][wining_position[pst1][4]]) == "-1-1-1-1-1"):
        #             return -1.
        # #checkcolumn
        # for pst in range(self.board_size):
        #     for pst1 in range(6):
        #         if (str(self.board[wining_position[pst1][0]][pst]) + str(self.board[wining_position[pst1][1]][pst])
        #                 + str(self.board[wining_position[pst1][2]][pst]) + str(self.board[wining_position[pst1][3]][pst])
        #                 + str(self.board[wining_position[pst1][4]][pst]) == "11111"):
        #             return 1.
        # for pst in range (self.board_size):
        #     for pst1 in range(6):
        #         if (str(self.board[wining_position[pst1][0]][pst]) + str(self.board[wining_position[pst1][1]][pst])
        #                 + str(self.board[wining_position[pst1][2]][pst]) + str(self.board[wining_position[pst1][3]][pst])
        #                 + str(self.board[wining_position[pst1][4]][pst]) == "-1-1-1-1-1"):
        #             return -1.
        # #checkdiagonal
        # #lefttoright
        # for i in range(6):
        #     for j in range(6-i):
        #         if (str(self.board[j][i+j]) + str(self.board[j+1][i+j+1]) + str(self.board[j+2][i+j+2]) + str(self.board[j+3][i+j+3]) + str(self.board[j+4][i+j+4]) == "11111") or \
        #                 (str(self.board[i+j][j]) + str(self.board[i+j+1][j+1]) + str(self.board[i+j+2][j+2]) + str(self.board[i+j+3][j+3]) + str(self.board[i+j+4][j+4]) == "11111"):
        #             return 1.
        # for i in range(6):
        #     for j in range(6 - i):
        #         if (str(self.board[j][i + j]) + str(self.board[j + 1][i + j + 1]) + str(self.board[j + 2][i + j + 2]) + str(self.board[j + 3][i + j + 3]) + str(self.board[j + 4][i + j + 4]) == "-1-1-1-1-1") or \
        #                 (str(self.board[i + j][j]) + str(self.board[i + j + 1][j + 1]) + str(self.board[i + j + 2][j + 2]) + str(self.board[i + j + 3][j + 3]) + str(self.board[i + j + 4][j + 4]) == "-1-1-1-1-1"):
        #             return -1.
        # #righttoleft
        # for i in range(6):
        #     for j in range(6 - i):
        #         if (str(self.board[j][self.board_size-1-i-j]) + str(self.board[j+1][self.board_size-1-i-(j+1)]) + str(self.board[j+2][self.board_size-1-i-(j+2)]) + str(self.board[j+3][self.board_size-1-i-(j+3)]) + str(self.board[j+4][self.board_size-1-i-(j+4)]) == "11111") or \
        #                 (str(self.board[self.board_size-1-i-j][j]) + str(self.board[self.board_size-1-i-(j+1)][j+1]) + str(self.board[self.board_size-1-i-(j+2)][j+2]) + str(self.board[self.board_size-1-i-(j+3)][j+3]) + str(self.board[self.board_size-1-i-(j+4)][j+4]) == "11111"):
        #             return 1.
        # for i in range(6):
        #     for j in range(6 - i):
        #         if (str(self.board[j][self.board_size-1-i-j]) + str(self.board[j+1][self.board_size-1-i-(j+1)]) + str(self.board[j+2][self.board_size-1-i-(j+2)]) + str(self.board[j+3][self.board_size-1-i-(j+3)]) + str(self.board[j+4][self.board_size-1-i-(j+4)]) == "-1-1-1-1-1") or \
        #                 (str(self.board[self.board_size-1-i-j][j]) + str(self.board[self.board_size-1-i-(j+1)][j+1]) + str(self.board[self.board_size-1-i-(j+2)][j+2]) + str(self.board[self.board_size-1-i-(j+3)][j+3]) + str(self.board[self.board_size-1-i-(j+4)][j+4]) == "-1-1-1-1-1"):
        #             return -1.
        # return None
        # check if game is over
        rowsum = np.sum(self.board, 0)
        colsum = np.sum(self.board, 1)
        diag_sum_tl = self.board.trace()
        diag_sum_tr = self.board[::-1].trace()

        if any(rowsum == self.board_size) or any(
                        colsum == self.board_size) or diag_sum_tl == self.board_size or diag_sum_tr == self.board_size:
            return 1.
        elif any(rowsum == -self.board_size) or any(
                        colsum == -self.board_size) or diag_sum_tl == -self.board_size or diag_sum_tr == -self.board_size:

            return -1.
        elif np.all(self.board != 0):
            return 0.
        else:
            # if not over - no result
            return None



    def is_game_over(self):
        return self.game_result != None

    def is_move_legal(self, move):
        # check if correct player moves
        if move.value != self.next_to_move:
            return False

        # check if inside the board
        x_in_range = move.x_coordinate < self.board_size and move.x_coordinate >= 0
        if not x_in_range:
            return False

        # check if inside the board
        y_in_range = move.y_coordinate < self.board_size and move.y_coordinate >= 0
        if not y_in_range:
            return False

        # finally check if board field not occupied yet
        return self.board[move.x_coordinate, move.y_coordinate] == 0

    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError("move " + move + " on board " + self.board + " is not legal")
        new_board = np.copy(self.board)
        new_board[move.x_coordinate, move.y_coordinate] = move.value
        next_to_move = TicTacToeGameState.o if self.next_to_move == TicTacToeGameState.x else TicTacToeGameState.x
        return TicTacToeGameState(new_board, next_to_move)

    def get_legal_actions(self):
        indices = np.where(self.board == 0)
        return [TicTacToeMove(coords[0], coords[1], self.next_to_move) for coords in list(zip(indices[0], indices[1]))]
