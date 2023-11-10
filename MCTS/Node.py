class Node:
    def __init__(self, state, action=None, parent=None):
        self.state = state  # STATE SHOULD BE A COPY OF THE MONOPOLYBOARDMCTS CLASS
        self.children = []
        self.visits = 0
        self.total_reward = 0
        self.action = action
        self.parent = parent

    def is_terminal(self):
        if self.state.agent.bankrupt or all([other_player.bankrupt for other_player in self.state.other_players]):
            return True
        else:
            return False

    def get_child_with_action(self, action):
        for child in self.children:
            if child.action == action:
                return child

        raise ChildNotFoundError(f"Child with action {action} does not exist")

class ChildNotFoundError(Exception):
    pass