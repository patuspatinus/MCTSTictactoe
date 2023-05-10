from nodes import MonteCarloTreeSearchNode


class MonteCarloTreeSearch:
    def __init__(self, node: MonteCarloTreeSearchNode):
        self.root = node

    # def best_action(self, simulations_number):
    #     for _ in range(0, simulations_number):
    #         v = self.tree_policy()
    #         reward = v.rollout()
    #         v.backpropagate(reward)
    #     # exploitation only
    #     return self.root.best_child(c_param=0.)
    #
    # def tree_policy(self):
    #     current_node = self.root
    #     while not current_node.is_terminal_node():
    #         if not current_node.is_fully_expanded():
    #             return current_node.expand()
    #         else:
    #             current_node = current_node.best_child()
    #     return current_node
    def best_action(self,state,simulations_number):
        for _ in range(simulations_number):
            node = self.root
            state = state.clone()

            # Selection
            while not node.is_terminal_node():
                if node.is_fully_expanded():
                    node = node.best_child()
                else:
                    node = node.expand()
                    break

            # Rollout
            if node.is_terminal_node():
                current_rollout_state = state
            else:
                current_rollout_state = node.state

            result = current_rollout_state.game_result
            if result is None:
                result = node.rollout()

            # Backpropagation
            node.backpropagate(result)

            # Select the best move based on the number of visits
        best_child = self.root.best_child(c_param=0)

        return best_child
