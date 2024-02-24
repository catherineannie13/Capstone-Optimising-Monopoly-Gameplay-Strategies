from Player import Player
from MonopolyBoardMCTS import MonopolyBoardMCTS
class State:
    """
    Represents the state of the Monopoly game board.

    Attributes
    ----------
    rounds : int
        The number of rounds played.
    agent : list
        Information about the agent player.
    other_players : list
        Information about the other players.
    properties : list
        Information about the properties on the board.
    stations : list
        Information about the stations on the board.
    utilities : list
        Information about the utilities on the board.
    agent_wealth : int
        The wealth of the agent player.
    other_players_wealth : list
        The wealth of the other players.

    Methods
    -------
    from_monopoly_board(board)
        Converts a Monopoly board object to a State object.
    to_monopoly_board()
        Converts a State object to a Monopoly board object.
    preprocess_state()
        Preprocesses the state representation for the Monte Carlo Tree Search algorithm.
    """
    def __init__(self):
        self.rounds = None
        self.agent = None
        self.other_players = []
        self.properties = []
        self.stations = []
        self.utilities = []
        self.agent_wealth = 0
        self.other_players_wealth = []

    def from_monopoly_board(self, board):
        """
        Converts a Monopoly board object to a State object.

        Parameters
        ----------
        board : MonopolyBoardMCTS
            The Monopoly board object.

        Returns
        -------
        None
        """
        self.rounds = board.rounds

        agent = board.agent
        money_owed_agent = {player.name if player is not None else player: amount for player, amount in agent.money_owed.items()}
        self.agent = [agent.name, agent.position, agent.money, agent.bankrupt,
                      agent.in_jail, agent.turns_in_jail, agent.double_rolled,
                      agent.num_doubles, agent.jail_cards, money_owed_agent]

        for player in board.other_players:
            money_owed_player = {other.name if other is not None else other: amount for other, amount in agent.money_owed.items()}
            self.other_players.append([player.name, player.position, player.money, player.bankrupt,
                                       player.in_jail, player.turns_in_jail, player.double_rolled,
                                       player.num_doubles, player.jail_cards, money_owed_player])

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

        self.agent_wealth = board.agent.wealth()
        self.other_players_wealth = [player.wealth() for player in board.other_players]

    def to_monopoly_board(self):
        """
        Converts a State object to a Monopoly board object.

        Returns
        -------
        MonopolyBoardMCTS
            The Monopoly board object.
        """
        # reconstruction of Monopoly board
        board = MonopolyBoardMCTS()
        board.rounds = self.rounds

        # initialise agent and overwrite properties
        agent = Player(self.agent[0])
        agent.position, agent.money, agent.bankrupt, agent.in_jail, agent.turns_in_jail, \
            agent.double_rolled, agent.num_doubles, agent.jail_cards = self.agent[1:-1]
        board.add_agent(agent)

        # initialise players again and overwrite properties for each player
        for player_info in self.other_players:
            player = Player(player_info[0])
            player.position, player.money, player.bankrupt, player.in_jail, player.turns_in_jail, \
                player.double_rolled, player.num_doubles, player.jail_cards = player_info[1:-1]
            board.add_other_player(player)

        # add money owed by agent
        money_owed_dict = {}
        for player_name, amount in self.agent[-1].items():
            if not player_name:
                money_owed_dict[None] = amount
            else:
                for player in board.players:
                    if player.name == player_name:
                        money_owed_dict[player] = amount

        # add money owed by other players
        for other_player in self.other_players:
            money_owed_dict = {}
            for player_name, amount in other_player[-1].items():
                if not player_name:
                    money_owed_dict[None] = amount
                else:
                    for player in board.players:
                        if player.name == player_name:
                            money_owed_dict[player] = amount
        
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

    def preprocess_state(self):
        """
        Preprocesses the state representation for the Monte Carlo Tree Search algorithm.

        Returns
        -------
        list
            The preprocessed state representation.
        """
        state_representation = []
        state_representation.append(self.rounds)
        state_representation.extend(self.agent[:-1])

        for player, amount in self.agent[-1].items():
            state_representation.append(player)
            state_representation.append(amount)

        for other_player in self.other_players:
            state_representation.extend(other_player[:-1])

            for player, amount in other_player[-1].items():
                state_representation.append(player)
                state_representation.append(amount)

        for prop in self.properties:
            state_representation.extend(prop)

        for station in self.stations:
            state_representation.extend(station)

        for utility in self.utilities:
            state_representation.extend(utility)

        return state_representation