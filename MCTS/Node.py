class Node:
    def __init__(self, state, parent = None):
        self.state = state # STATE SHOULD BE A COPY OF THE MONOPOLYGAMEMCTS CLASS
        self.children = []
        self.visits = 0
        self.total_reward = 0
        self.parent = parent
        # self.action = action

    def terminal(self):
        pass

    def get_child_with_action(self, action):
        pass

    def add_child(self, action, child):
        pass