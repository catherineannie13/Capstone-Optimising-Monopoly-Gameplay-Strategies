import numpy as np
import random
from tqdm import tqdm
from Node import Node
from State import State
class MCTS:
    def __init__(self, root_state, max_iterations, exploration_weight = 1, max_simulations = 1000):
        self.root = Node(root_state)
        self.max_iterations = max_iterations
        self.max_simulations = max_simulations
        self.best_actions = []
        self.exploration_weight = exploration_weight

    def uct(self, node):
        # return infinity for unvisited nodes
        if node.visits == 0:
            return float('inf')
        
        # 2 components of UCT
        exploitation = node.total_reward/node.visits
        exploration = self.exploration_weight*(np.log(node.parent.visits)/node.visits)**0.5

        return exploitation + exploration
    
    def select_best_action(self, node):
        best_action = None
        best_value = float('-inf')

        # find the child node with the highest UCT value
        for child in node.children:
            uct_value = self.uct(child)

            # update best child node choice
            if uct_value > best_value:
                best_action = child.action
                best_value = uct_value

        return best_action

    def selection(self, node):
        # convert state back to Monopoly board to get legal actions for that state
        board = node.state.to_monopoly_board()
        legal_actions = board.get_legal_actions()

        # traverse tree until terminal node or node with unexplored children is reached
        while not node.is_terminal() and len(node.children) == len(legal_actions):
            best_action = self.select_best_action(node)
            
            if best_action:
                node = node.get_child_with_action(best_action)
            else:
                return node

        return node

    def expansion(self, node):
        # convert state back to Monopoly board to get legal actions for that state
        board = node.state.to_monopoly_board()
        legal_actions = board.get_legal_actions()

        # get untried actions
        children_actions = [child.action for child in node.children]
        untried_actions = [action for action in legal_actions if action not in children_actions]

        # if there are untried actions, randomly choose one & create child node
        if untried_actions:
            action = random.choice(untried_actions)
            board.perform_action(action)

            # create new state from Monopoly board for child node
            new_state = State()
            new_state.from_monopoly_board(board)

            # create child node for new action
            child = Node(new_state, action, parent = node)
            node.children.append(child)
            return child
        
        # if all actions have been tried, use UCT to choose child
        else:

            # TO DO: maybe there is a better way to keep track of the child node with the best action
            best_action = self.select_best_action(node)
            if not best_action: # PERHAPS NOT NECESSARY
                return node # PERHAPS NOT NECESSARY
            return node.get_child_with_action(best_action)

    def simulation(self, node):
        board = node.state.to_monopoly_board()
        sims = 0

        while not board.is_terminal() and sims < self.max_simulations:
            legal_actions = board.get_legal_actions()

            if legal_actions:
                # TO DO: modify to follow strategy rather than random choice
                # TO DO: the code should take the state (particularly the agent player) and determine which move to make based on strategy
                action = random.choice(legal_actions)
                # player unmortgages properties if possible
                # player builds on properties if possible (only one house/hotel per turn)
                # player leaves jail first with a jail card if they have one, if not with 50 if they have it
                # if land on property: player buys if they either have fewer than 3 properties or if they already have properties belonging to that set
                # if the player cannot pay: player first sells hotels/houses on most expensive properties, then mortgages most expensive properties until they have enough money
                
                board.perform_action(action)

            sims += 1

        # TO DO: PERHAPS DELETE STATE COPY AFTER USING IN SIMULATION (WE DON'T NEED IT ANYMORE)
        return board.calculate_reward()

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
    
    def run(self):
        best_action = self.search()

        # if there is no best action, there is no action choice at all
        if not best_action: # PERHAPS NOT NECESSARY
            return # PERHAPS NOT NECESSARY

        self.best_actions.append(best_action)
            
        # update root node to the child node corresponding to best action
        self.root = self.root.get_child_with_action(best_action)

    def run_game(self, max_actions=1000):
        actions = 0
        pbar = tqdm(total=max_actions, desc="Running MCTS game")

        # play game until a maximum number of actions or game has ended
        while actions < max_actions and not self.root.is_terminal():
            self.run()
            actions += 1
            pbar.update(1)

        pbar.close()

class GameLogicError(Exception):
    pass