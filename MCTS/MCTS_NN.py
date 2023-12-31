import numpy as np
import random
import copy
from Node import Node
from State import State
from NN import NN
from tqdm import tqdm
import torch.optim as optim
import torch.nn as nn
import torch
class MCTS:
    def __init__(self, root_state, max_iterations, exploration_weight = 1, state_size = 1000):
        self.root = Node(root_state)
        self.max_iterations = max_iterations
        self.best_actions = []
        self.exploration_weight = exploration_weight
        self.q_network = NN(input_size=state_size, output_size=len(root_state.get_legal_actions()))
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()

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

        while not board.is_terminal():
            legal_actions = board.get_legal_actions()

            if legal_actions:
                # use neural network to predict Q-values
                state = State()
                state.to_monopoly_board(board)
                state_tensor = torch.tensor(state.preprocess_state()).float().unsqueeze(0)
                q_values = self.q_network(state_tensor).detach().numpy()

                # select and perform action with highest Q-value
                action = np.argmax(q_values)
                board.perform_action(action)

        return board.calculate_reward()

    def backpropagation(self, node, reward):
        while node is not None:
            state_tensor = torch.tensor(node.state.preprocess_state()).float().unsqueeze(0)
            q_values = self.q_network(state_tensor)

            # choose best action based on Q-values
            best_action = self.select_best_action(node)
            best_action_index = node.state.get_legal_actions().index(best_action)

            # Q-learning update
            q_values[0, best_action_index] += reward

            # compute loss and perform gradient descent
            target_q_values = torch.tensor(q_values).float()
            loss = self.criterion(self.q_network(state_tensor), target_q_values)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

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