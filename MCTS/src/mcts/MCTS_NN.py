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
    """
    Monte Carlo Tree Search (MCTS) algorithm for decision-making in Monopoly gameplay.

    Attributes
    ----------
    root : Node
        The root node of the search tree.
    max_iterations : int
        The maximum number of iterations for the search algorithm.
    best_actions : list
        A list to store the best actions found during the search.
    exploration_weight : float, optional
        The exploration weight parameter for the UCT (Upper Confidence Bound for Trees) formula.
    q_network : NN
        The neural network used for Q-value estimation.
    optimizer : torch.optim.Optimizer
        The optimizer used for updating the neural network parameters.
    criterion : torch.nn.modules.loss._Loss
        The loss function used for training the neural network.

    Methods
    -------
    uct(node)
        Calculates the UCT (Upper Confidence Bound for Trees) value for a given node.
    select_best_action(node)
        Selects the best action based on the UCT values of the child nodes.
    selection(node)
        Performs the selection phase of the MCTS algorithm.
    expansion(node)
        Performs the expansion phase of the MCTS algorithm.
    simulation(node)
        Performs the simulation phase of the MCTS algorithm.
    backpropagation(node, reward)
        Performs the backpropagation phase of the MCTS algorithm.
    search()
        Executes the MCTS algorithm.
    run()
        Runs a single iteration of the MCTS algorithm.
    run_game(max_actions=1000)
        Runs the MCTS algorithm for a specified number of actions or until the game ends.
    """

    def __init__(self, root_state, max_iterations, exploration_weight=1, state_size=1000):
        self.root = Node(root_state)
        self.max_iterations = max_iterations
        self.best_actions = []
        self.exploration_weight = exploration_weight
        self.q_network = NN(input_size=state_size, output_size=len(root_state.get_legal_actions()))
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()

    def uct(self, node):
        """
        Calculates the UCT (Upper Confidence Bound for Trees) value for a given node.

        Parameters
        ----------
        node : Node
            The node for which to calculate the UCT value.

        Returns
        -------
        float
            The UCT value for the given node.
        """
        if node.visits == 0:
            return float('inf')

        exploitation = node.total_reward / node.visits
        exploration = self.exploration_weight * (np.log(node.parent.visits) / node.visits) ** 0.5

        return exploitation + exploration

    def select_best_action(self, node):
        """
        Selects the best action based on the UCT values of the child nodes.

        Parameters
        ----------
        node : Node
            The node for which to select the best action.

        Returns
        -------
        object
            The best action to take from the given node.
        """
        best_action = None
        best_value = float('-inf')

        for child in node.children:
            uct_value = self.uct(child)

            if uct_value > best_value:
                best_action = child.action
                best_value = uct_value

        return best_action

    def selection(self, node):
        """
        Performs the selection phase of the MCTS algorithm.

        Parameters
        ----------
        node : Node
            The node from which to start the selection.

        Returns
        -------
        Node
            The selected node for expansion or simulation.
        """
        board = node.state.to_monopoly_board()
        legal_actions = board.get_legal_actions()

        while not node.is_terminal() and len(node.children) == len(legal_actions):
            best_action = self.select_best_action(node)

            if best_action:
                node = node.get_child_with_action(best_action)
            else:
                return node

        return node

    def expansion(self, node):
        """
        Performs the expansion phase of the MCTS algorithm.

        Parameters
        ----------
        node : Node
            The node to expand.

        Returns
        -------
        Node
            The child node created during the expansion.
        """
        board = node.state.to_monopoly_board()
        legal_actions = board.get_legal_actions()

        children_actions = [child.action for child in node.children]
        untried_actions = [action for action in legal_actions if action not in children_actions]

        if untried_actions:
            action = random.choice(untried_actions)
            board.perform_action(action)

            new_state = State()
            new_state.from_monopoly_board(board)

            child = Node(new_state, action, parent=node)
            node.children.append(child)

            return child

        else:
            best_action = self.select_best_action(node)
            if not best_action:
                return node
            return node.get_child_with_action(best_action)

    def simulation(self, node):
        """
        Performs the simulation phase of the MCTS algorithm.

        Parameters
        ----------
        node : Node
            The node to simulate from.

        Returns
        -------
        float
            The reward obtained from the simulation.
        """
        board = node.state.to_monopoly_board()

        while not board.is_terminal():
            legal_actions = board.get_legal_actions()

            if legal_actions:
                state = State()
                state.to_monopoly_board(board)
                state_tensor = torch.tensor(state.preprocess_state()).float().unsqueeze(0)
                q_values = self.q_network(state_tensor).detach().numpy()

                action = np.argmax(q_values)
                board.perform_action(action)

        return board.calculate_reward()

    def backpropagation(self, node, reward):
        """
        Performs the backpropagation phase of the MCTS algorithm.

        Parameters
        ----------
        node : Node
            The node to start the backpropagation from.
        reward : float
            The reward obtained from the simulation.
        """
        while node is not None:
            state_tensor = torch.tensor(node.state.preprocess_state()).float().unsqueeze(0)
            q_values = self.q_network(state_tensor)

            best_action = self.select_best_action(node)
            best_action_index = node.state.get_legal_actions().index(best_action)

            q_values[0, best_action_index] += reward

            target_q_values = torch.tensor(q_values).float()
            loss = self.criterion(self.q_network(state_tensor), target_q_values)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            node = node.parent

    def search(self):
        """
        Executes the MCTS algorithm.

        Returns
        -------
        object
            The best action to take from the root node.
        """
        for _ in range(self.max_iterations):
            node = self.root

            node = self.selection(node)

            if not node.is_terminal():
                node = self.expansion(node)

            reward = self.simulation(node)

            self.backpropagation(node, reward)

        best_action = self.select_best_action(self.root)

        return best_action

    def run(self):
        """
        Runs a single iteration of the MCTS algorithm.
        """
        best_action = self.search()

        if not best_action:
            return

        self.best_actions.append(best_action)
        self.root = self.root.get_child_with_action(best_action)

    def run_game(self, max_actions=1000):
        """
        Runs the MCTS algorithm for a specified number of actions or until the game ends.

        Parameters
        ----------
        max_actions : int, optional
            The maximum number of actions to take.

        Returns
        -------
        None
        """
        actions = 0
        pbar = tqdm(total=max_actions, desc="Running MCTS game")

        while actions < max_actions and not self.root.is_terminal():
            self.run()
            actions += 1
            pbar.update(1)

        pbar.close()

class GameLogicError(Exception):
    pass