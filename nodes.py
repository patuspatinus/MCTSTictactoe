import numpy as np
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
        action = self.untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
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
            (c.q / (c.n)) + c_param * 50 * np.sqrt((np.log(self.n) / (c.n)))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]
