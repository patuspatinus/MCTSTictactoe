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

    def __init__(self, state, next_to_move=1, last_move = None):
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Please play on 2D square board")
        self.board = state
        self.board_size = state.shape[0]
        self.next_to_move = next_to_move
        self.occupied_positions = self.get_occupied_positions()
        self.last_move = last_move

    def clone(self):
        new_state = TicTacToeGameState(np.zeros((self.board_size, self.board_size)))
        new_state.board = self.board.copy()
        new_state.next_to_move = self.next_to_move
        new_state.occupied_positions = self.occupied_positions.copy()
        return new_state

    @property
    def game_result(self):
        rows = self.board_size
        cols = self.board_size

        # Check rows
        for row in range(rows):
            for col in range(cols - 4):
                if self.board[row][col] != 0 and all(self.board[row][col] == self.board[row][col + i] for i in range(1, 5)):
                    return self.board[row][col]

        # Check columns
        for row in range(rows - 4):
            for col in range(cols):
                if self.board[row][col] != 0 and all(self.board[row][col] == self.board[row + i][col] for i in range(1, 5)):
                    return self.board[row][col]

        # Check diagonals (top left to bottom right)
        for row in range(rows - 4):
            for col in range(cols - 4):
                if self.board[row][col] != 0 and all(self.board[row][col] == self.board[row + i][col + i] for i in range(1, 5)):
                    return self.board[row][col]

        # Check diagonals (top right to bottom left)
        for row in range(rows - 4):
            for col in range(4, cols):
                if self.board[row][col] != 0 and all(self.board[row][col] == self.board[row + i][col - i] for i in range(1, 5)):
                    return self.board[row][col]

        # Check for a draw
        if np.all(self.board != 0):
            return 0

        # No winner or draw
        return None

        # # check if game is over
        # rowsum = np.sum(self.board, 0)
        # colsum = np.sum(self.board, 1)
        # diag_sum_tl = self.board.trace()
        # diag_sum_tr = self.board[::-1].trace()
        #
        # if any(rowsum == self.board_size) or any(
        #                 colsum == self.board_size) or diag_sum_tl == self.board_size or diag_sum_tr == self.board_size:
        #     return 1.
        # elif any(rowsum == -self.board_size) or any(
        #                 colsum == -self.board_size) or diag_sum_tl == -self.board_size or diag_sum_tr == -self.board_size:
        #
        #     return -1.
        # elif np.all(self.board != 0):
        #     return 0.
        # else:
        #     # if not over - no result
        #     return None



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
            raise ValueError(f"Move {move} on board {self.board} is not legal.")
        new_board = np.copy(self.board)
        new_board[move.x_coordinate, move.y_coordinate] = move.value
        next_to_move = TicTacToeGameState.o if self.next_to_move == TicTacToeGameState.x else TicTacToeGameState.x
        new_state = TicTacToeGameState(new_board, next_to_move)
        new_state.occupied_positions = self.occupied_positions.copy()
        new_state.occupied_positions.add((move.x_coordinate, move.y_coordinate))
        new_state.last_move = move
        return new_state

    def get_occupied_positions(self):
        return {(x, y) for x in range(self.board_size) for y in range(self.board_size) if self.board[x, y] != 0}

    def get_legal_actions(self):
        indices = np.where(self.board == 0)
        return [TicTacToeMove(coords[0], coords[1], self.next_to_move) for coords in list(zip(indices[0], indices[1]))]

    def hash(self):
        return tuple(map(tuple, self.board))