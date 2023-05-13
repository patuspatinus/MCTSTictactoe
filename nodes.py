import numpy as np
from tictactoe import *
from collections import defaultdict
import copy

check_occupied_position = list(zip())

class TicTacToeGameState:
    # Implement the TicTacToeGameState class with necessary methods and functionalities
    pass


class MonteCarloTreeSearchNode:
    def __init__(self, state: TicTacToeGameState, parent=None):
        self._number_of_visits = 0
        self._results = np.zeros(3)  # Index 0: draws, Index 1: player 1 wins, Index 2: player 2 wins
        self.state = state
        self.parent = parent
        self.children = []
        self.transposition_table = {}

    @property
    def untried_actions(self):
        if not hasattr(self, '_untried_actions'):
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        wins = self._results[self.parent.state.next_to_move]
        loses = self._results[-1 * self.parent.state.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        if len(self.untried_actions) == 0:
            return None  # No more untried actions
        # action = self.untried_actions.pop()
        action = self.select_action_heuristic()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def select_action_heuristic(self):
        # Prioritize moves in the center of the board
        center_actions = [action for action in self.untried_actions if
                          action.x_coordinate == 4 and action.y_coordinate == 4]
        if center_actions:
            return center_actions[0]

        for move in self.untried_actions:
            try_move = TicTacToeMove(move.x_coordinate, move.y_coordinate, self.state.next_to_move)
            next_state = self.state.move(try_move)
            if next_state.is_game_over() and next_state.game_result == self.state.next_to_move:
                return move


        for move in self.untried_actions:
            try_move = TicTacToeMove(move.x_coordinate, move.y_coordinate, self.state.next_to_move)
            next_state = self.state.move(try_move)
            # Check for potential winning lines horizontally
            for row in range(self.state.board_size):
                for col in range(self.state.board_size - 3):
                    if all(next_state.board[row][col + i] == self.state.next_to_move for i in range(4)):
                        if (col == 0 and next_state.board[row][col + 4] == -1):
                            continue
                        elif (next_state.board[row][col-1] == -1 and col + 4 > self.state.board_size):
                            continue
                        elif (next_state.board[row][col-1] == -1 and next_state.board[row][col + 4] == -1):
                            continue
                        print("x")
                        return move

            # Check for potential winning lines vertically
            for col in range(self.state.board_size):
                for row in range(self.state.board_size - 3):
                    if all(next_state.board[row + i][col] == self.state.next_to_move for i in range(4)):
                        if row == 0 and next_state.board[row + 4][col] == -1:
                            continue
                        elif next_state.board[row - 1][col] == -1 and row + 4 > self.state.board_size:
                            continue
                        elif next_state.board[row - 1][col] == -1 and next_state.board[row + 4][col] == -1:
                            continue
                        print("y")
                        return move

            # Check for potential winning lines diagonally (top-left to bottom-right)
            for row in range(self.state.board_size - 3):
                for col in range(self.state.board_size - 3):
                    if all(next_state.board[row + i][col + i] == self.state.next_to_move for i in range(4)):
                        if (row == 0 and col == 0 and next_state.board[row + 4][col + 4] == -1) or \
                                (row > 0 and col > 0 and next_state.board[row - 1][col - 1] == -1 and
                                 next_state.board[row + 4][col + 4] == -1) or \
                                (row > 0 and col == 0 and next_state.board[row - 1][col + 4] == -1) or \
                                (row == 0 and col > 0 and next_state.board[row + 4][col - 1] == -1):
                            continue
                        print("z")
                        return move

            # Check for potential winning lines diagonally (top-right to bottom-left)
            for row in range(self.state.board_size - 3):
                for col in range(3, self.state.board_size):
                    if all(next_state.board[row + i][col - i] == self.state.next_to_move for i in range(4)):
                        if (row == 0 and col == self.state.board_size - 1 and next_state.board[row + 4][
                            col - 4] == -1) or \
                                (row > 0 and col < self.state.board_size - 1 and next_state.board[row - 1][
                                    col + 1] == -1 and next_state.board[row + 4][col - 4] == -1) or \
                                (row > 0 and col == self.state.board_size - 1 and next_state.board[row - 1][
                                    col - 4] == -1) or \
                                (row == 0 and col < self.state.board_size - 1 and next_state.board[row + 4][
                                    col + 1] == -1):
                            continue
                        print("t")
                        return move

        # for move in self.untried_actions:
        #     try_move = TicTacToeMove(move.x_coordinate, move.y_coordinate, -1)
        #     next_state = self.state.move(try_move)
        #     if next_state.is_game_over() and next_state.game_result == -1:
        #         return move

        #Doublemove
        for move in self.untried_actions:
            try_move = TicTacToeMove(move.x_coordinate, move.y_coordinate, self.state.next_to_move)
            next_state = self.state.move(try_move)
            # Check for potential winning lines horizontally
            for move in self.untried_actions:
                try_move = TicTacToeMove(move.x_coordinate, move.y_coordinate, self.state.next_to_move)
                next_state = self.state.move(try_move)

                # Check for potential winning lines vertically
                for row in range(self.state.board_size):
                    count = 0
                    for i in range(self.state.board_size):
                        if (next_state.board[row][i] == -1):
                            count = count + 1
                        if (count >= 2):
                            break
                    if count >= 2:
                        continue
                    for col in range(self.state.board_size - 2):
                        if all(next_state.board[row][col + i] == self.state.next_to_move for i in range(3)):
                            for col_vert in (col, col + 2):
                                # Check for potential winning lines diagonally (top-right to bottom-left)
                                if ((all(next_state.board[row + i][col + i] == self.state.next_to_move for i in
                                         range(-2, 1)) and col >= 2 and row >= 2) or
                                        (all(next_state.board[row + i][col + i] == self.state.next_to_move for i in
                                             range(-1,
                                                   2)) and col >= 1 and col + 1 < self.state.board_size and row >= 1 and row + 1 < self.state.board_size) or
                                        (all(next_state.board[row + i][col + i] == self.state.next_to_move for i in
                                             range(0,
                                                   3)) and col + 2 < self.state.board_size and row + 2 < self.state.board_size)):
                                    print("Vertical and Diagonal (top-right to bottom-left)")
                                    return move

                                # Check for potential winning lines diagonally (top-left to bottom-right)
                                if ((all(next_state.board[row + i][col - i] == self.state.next_to_move for i in
                                         range(-2, 1)) and col <= self.state.board_size - 3 and row >= 2) or
                                        (all(next_state.board[row + i][col - i] == self.state.next_to_move for i in
                                             range(-1,
                                                   2)) and col <= self.state.board_size - 2 and col - 1 >= 0 and row >= 1 and row + 1 < self.state.board_size) or
                                        (all(next_state.board[row + i][col - i] == self.state.next_to_move for i in
                                             range(0, 3)) and col - 2 >= 0 and row + 2 < self.state.board_size)):
                                    print("Vertical and Diagonal (top-left to bottom-right)")
                                    return move

                                if ((all(next_state.board[row + i][col_vert] == self.state.next_to_move for i in
                                         range(-2, 1)) and row >= 2) or
                                        (all(next_state.board[row + i][col_vert] == self.state.next_to_move for i in
                                             range(-1, 2)) and row >= 1 and row + 1 < self.state.board) or
                                        (all(next_state.board[row + i][col_vert] == self.state.next_to_move for i in
                                             range(0, 3)) and row + 2 < self.state.board)):
                                    print("Vertical and Horizontal")
                                    return move

                for col in range(self.state.board_size):
                    for i in range(self.state.board_size):
                        if (next_state.board[i][col] == -1):
                            count = count + 1
                        if (count >= 2):
                            break
                    if count >= 2:
                        continue
                    for row in range(self.state.board_size - 2):
                        if all(next_state.board[row + i][col] == self.state.next_to_move for i in range(3)):
                            print(row, col)
                            for row_horiz in (row, row + 2):
                                    # Check for potential winning lines diagonally (top-left to bottom-right)
                                if ((all(next_state.board[row_horiz + i][col + i] == self.state.next_to_move for i in
                                        range(-2, 1)) and col >= 2 and row_horiz >= 2) or
                                        (all(next_state.board[row_horiz + i][col + i] == self.state.next_to_move for i in
                                            range(-1,
                                                2)) and col >= 1 and col + 1 < self.state.board_size and row_horiz >= 1 and row_horiz + 1 < self.state.board_size) or
                                        (all(next_state.board[row_horiz + i][col + i] == self.state.next_to_move for i in
                                            range(0,
                                                3)) and col + 2 < self.state.board_size and row_horiz + 2 < self.state.board_size)):
                                    print("Ngang_cheo1")
                                    return move
                                    # Check for potential winning lines diagonally (top-right to bottom-left)
                                if ((all(next_state.board[row_horiz + i][col - i] == self.state.next_to_move for i in
                                        range(-2, 1)) and col <= self.state.board_size - 3 and row_horiz >= 2) or
                                        (all(next_state.board[row_horiz + i][col - i] == self.state.next_to_move for i in
                                            range(-1,
                                                2)) and col <= self.state.board_size - 2 and col - 1 >= 0 and row_horiz >= 1 and row_horiz + 1 < self.state.board_size) or
                                        (all(next_state.board[row_horiz + i][col - i] == self.state.next_to_move for i in
                                            range(0, 3)) and col - 2 >= 0 and row_horiz + 2 < self.state.board_size)):
                                    print("Ngang_cheo2")
                                    return move

                                if ((all(next_state.board[row_horiz][col + i] == self.state.next_to_move for i in
                                        range(-2, 1)) and col >= 2) or
                                        (all(next_state.board[row_horiz][col + i] == self.state.next_to_move for i in
                                            range(-1, 2)) and col >= 1 and col + 1 < self.state.board_size) or
                                        (all(next_state.board[row_horiz][col + i] == self.state.next_to_move for i in
                                            range(0, 3)) and col + 2 < self.state.board_size)):
                                    print("Vert_Hori")
                                    return move


        for (x,y) in self.state.occupied_positions:
            if (x,y) not in check_occupied_position:
                check_occupied_position.append((x, y))
        print(check_occupied_position)
        #Upper
        for (x, y) in check_occupied_position:
            if (self.state.board[x][y] == -1):
                continue
            print("Upper ", x, y)
            near_occupied_position_actions = [action for action in self.untried_actions if
                                              (action.x_coordinate, action.y_coordinate) in [(x-1, y),(x+1, y),(x, y-1),(x, y+1)]]
        if near_occupied_position_actions:
            return near_occupied_position_actions.pop(0)

        # #Lower
        # for (x, y) in reversed(check_occupied_position):
        #     if (self.state.board[x][y] == -1):
        #         continue
        #     print("Lower ", x, y)
        #     near_occupied_position_actions = [action for action in self.untried_actions if
        #                                       (action.x_coordinate, action.y_coordinate) == (x+1, y)]
        # if near_occupied_position_actions:
        #     return near_occupied_position_actions.pop(0)
        #
        # #Left
        # for (x, y) in check_occupied_position:
        #     if (self.state.board[x][y] == -1):
        #         continue
        #     near_occupied_position_actions = [action for action in self.untried_actions if
        #                                       (action.x_coordinate, action.y_coordinate) == (x, y-1)]
        # if near_occupied_position_actions:
        #     return near_occupied_position_actions.pop(0)
        #
        # #Right
        # for (x, y) in check_occupied_position:
        #     if (self.state.board[x][y] == -1):
        #         continue
        #     near_occupied_position_actions = [action for action in self.untried_actions if
        #                                       (action.x_coordinate, action.y_coordinate) == (x, y+1)]
        # if near_occupied_position_actions:
        #     return near_occupied_position_actions.pop(0)
        #
        # # If no center or near center moves, choose a random untried action
        # return self.untried_actions.pop()

    def is_terminal_node(self):
        def is_terminal_node(self):
            if self.parent is None:
                return False  # Root node is not a terminal node
            return self.state.is_game_over()

    def rollout(self):
        if self.state.hash() in self.transposition_table:
            return self.transposition_table[self.state.hash()]

        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)

        result = current_rollout_state.game_result
        self.transposition_table[self.state.hash()] = result
        return result

    def backpropagate(self, result):
        self._number_of_visits += 1
        if result is None:
            # Draw
            self._results[0] += 1
        else:
            # Player 1 wins
            if result == 1:
                self._results[1] += 1
            # Player 2 wins
            elif result == -1:
                self._results[2] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / (c.n)) + c_param * 50 * np.sqrt((2 * np.log(self.n) / (c.n)))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        for move in possible_moves:
            try_move = TicTacToeMove(move.x_coordinate, move.y_coordinate, self.state.next_to_move)
            next_state = self.state.move(try_move)
            if next_state.is_game_over() and next_state.game_result == self.state.next_to_move:
                return move

        for move in possible_moves:
            try_move = TicTacToeMove(move.x_coordinate, move.y_coordinate, -1)
            next_state = self.state.move(try_move)
            if next_state.is_game_over() and next_state.game_result == -1:
                return move

        return possible_moves[np.random.randint(len(possible_moves))]