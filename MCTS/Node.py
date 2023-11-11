class Node:
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

        # game ends when either the agent is bankrupt or the agent won
        if self.state.agent.bankrupt or all([other_player.bankrupt for other_player in self.state.other_players]):
            return True
        else:
            return False

    def get_child_with_action(self, action):

        # find child with corresponding action
        for child in self.children:
            if child.action == action:
                return child

        raise ChildNotFoundError(f"Child with action {action} does not exist")

class ChildNotFoundError(Exception):
    pass