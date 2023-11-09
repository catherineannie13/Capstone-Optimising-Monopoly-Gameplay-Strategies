class MCTS:
    def __init__(self, root_state, max_iterations):
        self.root = Node(root_state)
        self.max_iterations = max_iterations

    def uct(self, node, exploration_weight = 1):
        # return infinity for unvisited nodes
        if node.visits == 0:
            return float('inf')
        
        # 2 components of UCT
        exploitation = node.total_reward/node.visits
        exploration = exploration_weight*(np.log(node.parent.visits)/node.visits)**0.5

        return exploitation + exploration
    
    def select_best_action(self, node, exploration_weight = 1):
        best_action = None
        best_value = float('-inf')

        # find the child node with the highest UCT value
        for child in node.children:
            uct_value = self.uct(child, exploration_weight)

            # update best child node choice
            if uct_value > best_value:
                best_action = child.action
                best_value = uct_value

        return best_action

    def selection(self, node):
        # traverse tree until terminal node or node with unexplored children is reached
        while not node.is_terminal() and len(node.children) == len(node.state.get_legal_actions()):
            best_action = self.select_best_action(node)
            node = node.get_child_with_action(best_action)

        return node

    def expansion(self, node):
        legal_actions = node.state.get_legal_actions()
        children_actions = [child.action for child in node.children]
        untried_actions = [action for action in legal_actions if action not in children_actions]

        # if there are untried actions, randomly choose one & create child node
        if untried_actions:
            action = random.choice(untried_actions)
            new_state = node.state.perform_action(action)

            # create child node for new action
            child = Node(new_state, action, parent = node)
            node.children.append(child)

            return child
        
        # if all actions have been tried, use UCT to choose child
        else:

            # TO DO: maybe there is a better way to keep track of the child node with the best action
            best_action = self.select_best_action(node)
            return node.get_child_with_action(best_action)

    def simulation(self, node):
        # TO DO: EDIT THIS METHOD SO THAT THE GAME IS PLAYED OUT CORRECTLY (INCLUDING OPPONENTS' TURNS)
        state = node.state

        while not state.is_terminal():
            legal_actions = state.get_legal_actions()

            if legal_actions:
                # TO DO: modify to follow strategy rather than random choice
                # TO DO: call the relevant method from MonopolyGameMCTS to perform the action
                action = random.choice(legal_actions)
                state = state.perform_action(action)

            # TO DO: edit to raise error (if the state is not terminal, there should be legal actions to take) - is this true??
            # TO DO: is it a typeError or a different kind?
            else:
                raise GameLogicError("There are no legal actions, but the state of the game is not terminal")
        
        # TO DO: wealth calculation
        # MAYBE: WEALTH MIGHT BE GIVEN BY THE RATIO OF THE AGENTS WEALTH TO THE AVERAGE OF OTHER PLAYERS' WEALTH
        return state.calculate_reward()


    def backpropagation(self, node, reward):
        # traverse up the tree to the root
        while node is not None:

            # modify node properties
            node.visits += 1
            node.total_reward += reward

            # traverse up the tree until root node is reached
            node = node.parent

    def search(self):
        for _ in range(self.max_iterations):
            node = self.root

            # selection phase
            node = self.selection(node)

            # expansion phase
            if not node.is_terminal():
                node = self.expansion(node)

            # simulation phase
            reward = self.simulation(node)

            # backpropagation phase
            self.backpropagation(node, reward)

        # select the best action to take from the root node
        best_action = self.select_best_action(self.root)

        return best_action
class GameLogicError(Exception):
    pass