class State:
    def __init__(self):
        self.rounds = None
        self.agent = None
        self.other_players = []
        self.properties = []
        self.stations = []
        self.utilities = []

    def from_monopoly_board(self, board):
        self.rounds = board.rounds

        agent = board.agent
        self.agent = [agent.name, agent.position, agent.money, agent.bankrupt,
                      agent.in_jail, agent.turns_in_jail, agent.double_rolled,
                      agent.num_doubles, agent.jail_cards]

        for player in self.board.other_players:
            self.other_players.append([player.name, player.position, player.money, player.bankrupt,
                                       player.in_jail, player.turns_in_jail, player.double_rolled,
                                       player.num_doubles, player.jail_cards])

        for prop in board.properties:
            if prop.owner:
                self.properties.append([prop.num_houses, prop.hotel, prop.owner.name, prop.is_mortgaged])
            else:
                self.properties.append([prop.num_houses, prop.hotel, None, prop.is_mortgaged])

        for station in board.stations:
            if station.owner:
                self.stations.append([station.owner.name, station.is_mortgaged])
            else:
                self.stations.append([None, station.is_mortgaged])

        for utility in board.utilities:
            if utility.owner:
                self.utilities.append([utility.owner.name, utility.is_mortgaged])
            else:
                self.utilities.append([NotImplemented, utility.is_mortgaged])

    def to_monopoly_board(self):
        pass