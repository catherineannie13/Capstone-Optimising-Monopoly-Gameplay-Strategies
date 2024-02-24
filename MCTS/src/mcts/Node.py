class Node:
    """
    Represents a node in the Monte Carlo Tree Search (MCTS) algorithm.

    Attributes
    ----------
    state : obj
        The state of the game at this node.
    children : list
        The list of child nodes.
    visits : int
        The number of times this node has been visited.
    total_reward : int
        The total reward accumulated at this node.
    action : obj
        The action taken to reach this node.
    parent : obj
        The parent node of this node.

    Methods
    -------
    __repr__():
        Returns a string representation of the action taken to reach this node.
    is_terminal():
        Checks if the game has reached a terminal state.
    get_child_with_action(action):
        Returns the child node with the specified action.
    """

    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.children = []
        self.visits = 0
        self.total_reward = 0
        self.action = action
        self.parent = parent

    def __repr__(self):
        return f"{self.action}"

    def is_terminal(self):
        """
        Checks if the game has reached a terminal state.

        Returns
        -------
        bool
            True if the game has reached a terminal state, False otherwise.
        """
        if self.state.agent[3] or all([other_player[3] for other_player in self.state.other_players]):
            return True
        else:
            return False

    def get_child_with_action(self, action):
        """
        Returns the child node with the specified action.

        Parameters
        ----------
        action : obj
            The action to search for.

        Returns
        -------
        obj
            The child node with the specified action.

        Raises
        ------
        ChildNotFoundError
            If no child node with the specified action is found.
        """
        for child in self.children:
            if child.action == action:
                return child

        raise ChildNotFoundError(f"Child with action {action} does not exist")

class ChildNotFoundError(Exception):
    pass