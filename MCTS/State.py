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

        for player in board.other_players:
            self.other_players.append([player.name, player.position, player.money, player.bankrupt,
                                       player.in_jail, player.turns_in_jail, player.double_rolled,
                                       player.num_doubles, player.jail_cards])

        for prop in board.properties:
            if prop.owner:
                self.properties.append([prop.owner.name, prop.num_houses, prop.hotel, prop.is_mortgaged])
            else:
                self.properties.append([None, prop.num_houses, prop.hotel, prop.is_mortgaged])

        for station in board.stations:
            if station.owner:
                self.stations.append([station.owner.name, station.is_mortgaged])
            else:
                self.stations.append([None, station.is_mortgaged])

        for utility in board.utilities:
            if utility.owner:
                self.utilities.append([utility.owner.name, utility.is_mortgaged])
            else:
                self.utilities.append([None, utility.is_mortgaged])

    def to_monopoly_board(self):
        # reconstruction of Monopoly board
        board = MonopolyBoardMCTS()
        board.rounds = self.rounds

        # initialise agent and overwrite properties
        agent = Player(self.agent[0])
        agent.position, agent.money, agent.bankrupt, agent.in_jail, agent.turns_in_jail, \
            agent.double_rolled, agent.num_doubles, agent.jail_cards = self.agent[1:]
        board.add_agent(agent)

        # initialise players again and overwrite properties for each player
        for player_info in self.other_players:
            player = Player(player_info[0])
            player.position, player.money, player.bankrupt, player.in_jail, player.turns_in_jail, \
                player.double_rolled, player.num_doubles, player.jail_cards = player_info[1:]
            board.add_other_player(player)
        
        for idx, prop in enumerate(self.properties):
            # properties have already been initialised in board (just overwrite some properties)
            # if there is an owner, property also needs to be added to player (player needs to be found by name)
            if prop[0]:
                for player in board.players:
                    if player.name == prop[0]:
                        player.properties.append(board.properties[idx])
                        prop_group = board.properties[idx].group
                        player.property_sets[prop_group].append(board.properties[idx])
                        board.properties[idx].owner = player
                        break

            board.properties[idx].num_houses, board.properties[idx].hotel, board.properties[idx].is_mortgaged = prop[1:]

        # count player houses and hotel counts
        for player in board.players:
            house_count = sum([prop.num_houses for prop in player.properties])
            hotel_count = sum([prop.hotel for prop in player.properties])
            player.houses = house_count
            player.hotels = hotel_count

        # and for stations and utilities
        for idx, station in enumerate(self.stations):
            if station[0]:
                for player in board.players:
                    if player.name == station[0]:
                        player.stations.append(board.stations[idx])
                        board.stations[idx].owner = player

            board.stations[idx].is_mortgaged = station[1]

        for idx, utility in enumerate(self.utilities):
            if utility[0]:
                for player in board.players:
                    if player.name == utility[0]:
                        player.utilities.append(board.utilities[idx])
                        board.utilities[idx].owner = player

            board.utilities[idx].is_mortgaged = utility[1]

        return board