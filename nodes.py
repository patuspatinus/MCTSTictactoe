import numpy as np
from tictactoe import *
from collections import defaultdict

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
        center_actions = [action for action in self.untried_actions if action.x_coordinate == 2 and action.y_coordinate == 2]
        if center_actions:
            return center_actions[0]
        # If no center moves, choose a random untried action
        return self.untried_actions.pop()

    # def select_action(self):
    #     best_action = None
    #     best_value = float('-inf')
    #     for action in self.untried_actions:
    #         next_state = self.state.move(action)
    #         value = self.alpha_beta(next_state, float('-inf'), float('inf'), 3)  # Adjust the depth as needed
    #         if value > best_value:
    #             best_value = value
    #             best_action = action
    #     return best_action
    #
    # def alpha_beta(self, state, alpha, beta, depth):
    #     key = state.hash()  # Generate a unique key for the state
    #     if key in self.transposition_table:  # Check if state has already been evaluated
    #         return self.transposition_table[key]
    #
    #     if self.parent is None or state.next_to_move == 1:
    #         value = float('-inf')
    #         for action in state.get_legal_actions():
    #             next_state = state.move(action)
    #             value = max(value, self.alpha_beta(next_state, alpha, beta, depth - 1))
    #             alpha = max(alpha, value)
    #             if alpha >= beta:
    #                 break
    #         self.transposition_table[key] = value  # Cache the evaluated state
    #         return value
    #     else:
    #         value = float('inf')
    #         for action in state.get_legal_actions():
    #             next_state = state.move(action)
    #             value = min(value, self.alpha_beta(next_state, alpha, beta, depth - 1))
    #             beta = min(beta, value)
    #             if alpha >= beta:
    #                 break
    #         self.transposition_table[key] = value  # Cache the evaluated state
    #         return value

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
            (c.q / (c.n)) + c_param * np.sqrt((2 * np.log(self.n) / (c.n)))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        for move in possible_moves:
            try_move = TicTacToeMove(move.x_coordinate, move.y_coordinate, self.state.next_to_move)
            next_state = self.state.move(try_move)
            if next_state.is_game_over() and next_state.game_result == self.state.next_to_move:
                return move
        return possible_moves[np.random.randint(len(possible_moves))]
