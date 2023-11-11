from Chance import Chance
from CommunityChest import CommunityChest
from FreeParking import FreeParking
from Go import Go
from GoToJail import GoToJail
from Jail import Jail
from Player import Player
from Station import Station
from Strategy import Strategy
from Street import Street
from Tax import Tax
from Utility import Utility
import random
import numpy as np
class MonopolyBoardMCTS:
    """
    This class represents the Monopoly board and the game logic. It provides methods for creating 
    the game board, adding players, and playing the game.

    Attributes
    ----------
    players: lst
        A list of Player objects representing the players in the game.
    board: lst
        A list of spaces on the Monopoly board.
    properties: lst
        A list of all street properties on the board.
    stations: lst
        A list of all station properties on the board.
    utilities: lst
        A list of utility properties on the board.
    tax: lst
        A list of tax spaces on the board.
    chance: obj
        The Chance card pile object.
    community_chest: obj
        The Community Chest card pile object.
    go: obj
        The Go space object.
    jail: obj
        The Jail space object.
    free_parking: obj
        The Free Parking space object.
    go_to_jail: obj
        The Go To Jail space object.
    property_sets: dict
        A dictionary of property sets grouped by colour.
    strategy: obj
        The object containing the strategy for the players.

    Methods
    -------
    __init__()
        Initialises the MonopolyBoard with all necessary properties and spaces.
    create_properties()
        Creates instances of the Street class for street properties on the board.
    create_stations()
        Creates instances of the Station class for station properties on the board.
    create_utilities()
        Creates instances of the Utility class for utility properties on the board.
    create_chance()
        Creates the Chance card pile and places it on the board.
    create_community_chest()
        Creates the Community Chest card pile and places it on the board.
    create_tax()
        Creates instances of the Tax class for tax spaces on the board.
    create_go()
        Creates the Go space and places it on the board.
    create_jail()
        Creates the Jail space and places it on the board.
    create_free_parking()
        Creates the Free Parking space and places it on the board.
    create_go_to_jail()
        Creates the Go To Jail space and places it on the board.
    add_player(player)
        Adds a player to the game.
    play_game(stopping_condition=float('inf'))
        Starts the Monopoly game and continues until there is a winner or a stopping condition 
        is met.
    take_turn(player, doubles=0)
        Executes a turn for a player, handling movement, actions, and decisions.
    perform_chance(player, dice_roll)
        Handles the execution of a Chance card drawn by a player.
    perform_community_chest(player)
        Handles the execution of a Community Chest card drawn by a player.
    handle_property(player, space, dice_roll=0)
        Handles actions when a player lands on a property space.
    raise_funds(player, cost)
        Raises funds for a player by selling houses and mortgaging properties.
    """

    def __init__(self):
        self.players = []
        self.agent = None
        self.other_players = []
        self.board = [None]*40
        self.properties = []
        self.stations = []
        self.utilities = []
        self.tax = []
        self.chance = None
        self.community_chest = None
        self.go = None
        self.jail = None
        self.free_parking = None
        self.go_to_jail = None
        self.property_sets = {"brown":[], "lightblue":[], "pink":[], "orange":[], 
                              "red":[], "yellow":[], "green":[], "darkblue":[]}
        self.properties_dict = {}
        self.rounds = 0

        self.create_properties()
        self.create_stations()
        self.create_utilities()
        self.create_chance()
        self.create_community_chest()
        self.create_tax()
        self.create_go()
        self.create_jail()
        self.create_free_parking()
        self.create_go_to_jail()

        self.strategy = Strategy()

    def __repr__(self):
        return f'Monopoly Board'

    def create_properties(self):
        """
        This method creates instances of the class Street for each street property on the Monopoly board.
        This does not include stations or utilities. It initialises all the necessary attributes of the class.
        Each street is added to the properties list and property_sets dictionary. Each street property
        is added at it's corresponding index on the Monopoly board to the list board.

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        street_data = [
            ("Old Kent Road", 60, 50, 2, 10, 30, 90, 160, 250, 1, "brown", 2),
            ("Whitechapel Road", 60, 50, 4, 20, 60, 180, 320, 450, 3, "brown", 2),
            ("The Angel Islington", 100, 50, 6, 30, 90, 270, 400, 550, 6, "lightblue", 3),
            ("Euston Road", 100, 50, 6, 30, 90, 270, 400, 550, 8, "lightblue", 3),
            ("Pentonville Road", 120, 50, 8, 40, 100, 300, 450, 600, 9, "lightblue", 3),
            ("Pall Mall", 140, 100, 10, 50, 150, 450, 625, 750, 11, "pink", 3),
            ("Whitehall", 140, 100, 10, 50, 150, 450, 625, 750, 13, "pink", 3),
            ("Northumberland Avenue", 160, 100, 12, 60, 180, 500, 700, 900, 14, "pink", 3),
            ("Bow Street", 180, 100, 14, 70, 200, 550, 750, 950, 16, "orange", 3),
            ("Marlborough Street", 180, 100, 14, 70, 200, 550, 750, 950, 18, "orange", 3),
            ("Vine Street", 200, 100, 16, 80, 220, 600, 800, 1000, 19, "orange", 3),
            ("The Strand", 220, 150, 18, 90, 250, 700, 875, 1050, 21, "red", 3),
            ("Fleet Street", 220, 150, 18, 90, 250, 700, 875, 1050, 23, "red", 3),
            ("Trafalgar Square", 240, 150, 20, 100, 300, 750, 925, 1100, 24, "red", 3),
            ("Leicester Square", 260, 150, 22, 110, 330, 800, 975, 1150, 26, "yellow", 3),
            ("Coventry Street", 260, 150, 22, 110, 330, 800, 975, 1150, 27, "yellow", 3),
            ("Piccadilly", 280, 150, 24, 120, 360, 850, 1025, 1200, 29, "yellow", 3),
            ("Regent Street", 300, 200, 26, 130, 390, 900, 1100, 1275, 31, "green", 3),
            ("Oxford Street", 300, 200, 26, 130, 390, 900, 1100, 1275, 32, "green", 3),
            ("Bond Street", 320, 200, 28, 150, 450, 1000, 1200, 1400, 34, "green", 3),
            ("Park Lane", 350, 200, 35, 175, 500, 1100, 1300, 1500, 37, "darkblue", 2),
            ("Mayfair", 400, 200, 50, 200, 600, 1400, 1700, 2000, 39, "darkblue", 2)
        ]

        # create instances of class with corresponding attributes & store them
        for name, price, house_price, rent, one_house, two_houses, three_houses, four_houses, hotel, loc, group, num_in_group in street_data:
            street = Street(name, price, house_price, rent, one_house, two_houses, three_houses, four_houses, hotel, loc, group, num_in_group)
            self.properties.append(street)
            self.board[loc] = street
            self.property_sets[group].append(street)
            self.properties_dict[street.name] = street

    def create_stations(self):
        """
        This method creates instances of the class Station for each station property on the Monopoly board.
        It initialises all the necessary attributes of the class. Each station is added to the stations list.
        Each station property is added at it's corresponding index on the Monopoly board to the list board.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        station_data = [
            ("King's Cross Station", 200, 25, 50, 100, 200, 5),
            ("Marylebone Station", 200, 25, 50, 100, 200, 15),
            ("Fenchurch St. Station", 200, 25, 50, 100, 200, 25),
            ("Liverpool St. Station", 200, 25, 50, 100, 200, 35)
        ]
        
        # create instances of class with corresponding attributes & store them
        for name, price, rent_one, rent_two, rent_three, rent_four, loc in station_data:
            station = Station(name, price, rent_one, rent_two, rent_three, rent_four, loc)
            self.stations.append(station)
            self.board[loc] = station
            self.properties_dict[station.name] = station

    def create_utilities(self):
        """
        This method creates instances of the class Utility for each utility property on the Monopoly board.
        It initialises all the necessary attributes of the class. Each utility is added to the utilities list.
        Each utility property is added at it's corresponding index on the Monopoly board to the list board.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        utility_data = [
            ("Electric Company", 150, 4, 10, 12),
            ("Water Works", 150, 4, 10, 28)
        ]
        
        # create instances of class with corresponding attributes & store them
        for name, price, rent_multiplier, rent_multiplier_two, loc in utility_data:
            utility = Utility(name, price, rent_multiplier, rent_multiplier_two, loc)
            self.utilities.append(utility)
            self.board[loc] = utility
            self.properties_dict[utility.name] = utility

    def create_chance(self):
        """
        This method creates a single instance of the Chance class. This class contains all necessary
        attributes for the chance card pile. Given that all chance spaces perform the same operation on
        a single pile of cards, only a single instance is created. This instance is stored at the 
        location of the chance spaces on the Monopoly board in the list board.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        chance_locs = [7, 22, 36]

        # create instance of class with corresponding attributes & store them
        chance = Chance(chance_locs)
        self.chance = chance

        for loc in chance_locs:
            self.board[loc] = chance

    def create_community_chest(self):
        """
        This method creates a single instance of the CommunityChest class. This class contains all 
        necessary attributes for the community chest pile. Given that all community chest spaces perform 
        the same operation on a single pile of cards, only a single instance is created. This instance 
        is stored at the location of the community chest spaces on the Monopoly board in the list board.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        community_chest_locs = [2, 17, 33]

        # create instance of class with corresponding attributes & store them
        community_chest = CommunityChest(community_chest_locs)
        self.community_chest = community_chest

        for loc in community_chest_locs:
            self.board[loc] = community_chest

    def create_tax(self):
        """
        This method creates instances of the class Tax for all tax spaces on the Monopoly board.
        It initialises all necessary attributes of the class. These instances are stored in the
        tax list. They are also stored at the location of the space on the Monopoly board in the 
        list board.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        tax_data = [
            ("Income Tax", 200, 4),
            ("Super Tax", 100, 38)
        ]

        # create instances of class with corresponding attributes & store them
        for name, amount, loc in tax_data:
            tax = Tax(name, amount, loc)
            self.tax.append(tax)
            self.board[loc] = tax

    def create_go(self):
        """
        This method creates a single instance of the class Go. It also initialises all necessary 
        attributes of the class. This instance is stored at the corresponding index that it is 
        located at on the Monopoly board in the list board.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        loc = 0

        # create instance of class with corresponding attributes & store them
        go = Go(200, loc)
        self.board[loc] = go
        self.go = go

    def create_jail(self):
        """
        This method creates a single instance of the class Jail. It also initialises all necessary 
        attributes of the class. This instance is stored at the corresponding index that it is 
        located at on the Monopoly board in the list board.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        loc = 10

        # create instance of class with corresponding attributes & store them
        jail = Jail(loc)
        self.board[loc] = jail
        self.jail = jail

    def create_free_parking(self):
        """
        This method creates a single instance of the class FreeParking. It also initialises all 
        necessary attributes of the class. This instance is stored at the corresponding index 
        that it is located at on the Monopoly board in the list board.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        loc = 20

        # create instance of class with corresponding attributes & store them
        free_parking = FreeParking(loc)
        self.board[loc] = free_parking
        self.free_parking = free_parking

    def create_go_to_jail(self):
        """
        This method creates a single instance of the class GoToJail. It also initialises all 
        necessary attributes of the class. This instance is stored at the corresponding index 
        that it is located at on the Monopoly board in the list board.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        loc = 30

        # create instance of class with corresponding attributes & store them
        go_to_jail = GoToJail(loc)
        self.board[loc] = go_to_jail
        self.go_to_jail = go_to_jail

    def add_other_player(self, player):
        """
        This method adds a single player to the MonopolyBoard class. Each player is an instance
        of the class Player and contains all necessary information about that player and their 
        standing (eg. what properties they own, how much money they possess, etc.). The player
        is appended to a list of players that are playing the Monopoly game. 
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.players.append(player)
        self.other_players.append(player)

    def add_agent(self, agent):
        self.players.append(agent)
        self.agent = agent

    def play_game(self, stopping_condition = float('inf')):
        """
        This method starts the Monopoly game. The players take it in turns to play their go until
        either there is only a single player that is not yet bankrupt or until a stopping 
        condition is reached. The default stopping condition is infinity, meaning the game will 
        run until all players but one are bankrupt.
        
        Parameters
        ----------
        stopping_condition: float, optional, default: float('inf')
            The value at which to stop playing the game (the maximum number of rounds).
        
        Returns
        -------
        None
        """
        i = 0

        # randomise order of players
        random.shuffle(self.players)

        # play continues until there is a winner/stopping condition met
        while len([player for player in self.players if not player.bankrupt]) >= 2 and i < stopping_condition:
            i += 1
            for player in self.players:
                self.take_turn(player)
            
    def take_turn(self, player, doubles = 0):
        """
        This method executes a turn of a player. This method begins by determining the player's 
        strategy to decide whether to build on their properties. Then, it simulates the player's 
        dice roll, checks if the player is in jail, and handles various outcomes based on the player's 
        position on the game board. If the player rolls doubles, they may take another turn, and 
        consecutive doubles are tracked. If the player rolls three doubles in a row, they go to jail, 
        and their turn ends.
        
        Parameters
        ----------
        player: obj
            Instance of the class Player.
        doubles: int, optional, default: 0
            The number of doubles that the player has rolled during this turn.
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the space type on the game board is not recognised or is of an incorrect type.
        """
        self.strategy.decide_unmortgage_properties(player)
        self.strategy.decide_build_on_properties(player, self.property_sets)

        # player rolls the dice
        a_roll = random.randint(1, 6)
        b_roll = random.randint(1, 6)
        dice_roll = a_roll + b_roll

        # if the player is in jail
        if player.in_jail:
            player.turns_in_jail += 1

            # player must leave jail after 3 rounds
            if player.turns_in_jail > 2:
                if a_roll == b_roll:
                    pass
                elif player.jail_cards > 0:
                    player.jail_cards -= 1
                elif player.money >= 50:
                    player.pay(50)
                else:
                    self.raise_funds(player, 50)
                
                player.in_jail = False

            # decide whether or not to leave jail before 3 rounds
            elif self.strategy.decide_to_leave_jail(player):
                player.in_jail = False

            # not leaving jail so turn is over
            else:
                return

        # count consecutive doubles for player
        if a_roll == b_roll:
            doubles += 1

        # go to jail if third double in a row and end turn
        if doubles > 2:
            player.position = 10
            player.in_jail = True
            return
            
        # player moves the number of spaces shown on the two dice combined
        previous_position = player.position
        player.move(dice_roll)
        new_position = player.position
        space = self.board[new_position]

        # if the player passed go, collect the Go income
        if previous_position > new_position:
            player.receive(self.board[0].income)

        if space.type == "Street":
            self.handle_property(player, space)

        elif space.type == "Station":
            self.handle_property(player, space)

        elif space.type == "Utility":
            self.handle_property(player, space, dice_roll)
        
        # handle chance card outcomes
        elif space.type == "Chance":
            self.perform_chance(player, dice_roll)

        # handle community chest card outcomes
        elif space.type == "Community Chest":
            self.perform_community_chest(player)

        # player pays the tax amount to the bank and no further action is taken
        elif space.type == "Tax":
            tax = space.calculate_tax(player)

            if player.money >= tax:
                player.pay(tax)
            else:
                self.raise_funds(player, tax)

        # no action is taken if the player lands on Go
        elif space.type == "Go":
            pass
        
        # no action is taken if the player lands on jail since they are just visiting
        elif space.type == "Jail":
            pass

        # no action is taken if the player lands on free parking
        elif space.type == "Free Parking":
            pass
        
        # player goes to jail
        elif space.type == "Go To Jail":
            player.position = 10
            player.in_jail = True

        else:
            raise TypeError("Space of incorrect type found on board. Type: " + space.type)
        
        # player takes another turn if they roll a double
        if a_roll == b_roll:
            self.take_turn(player, doubles)
        else:
            return

    def perform_chance(self, player, dice_roll):
        """
        This method executes a player picking a chance card from the top of the chance card
        pile. The method draws a card from the stack contained within an instance of the
        Chance object. The method then handles the card that is chosen from the stack.
        
        Parameters
        ----------
        player: obj
            Instance of the class Player.
        dice_roll: int
            The number that the player has rolled on the dice.
        
        Returns
        -------
        None
        """
        chance_card = self.chance.choose_card()

        if chance_card == "Advance to Go.":
            player.position = 0
            player.receive(200)

        elif chance_card == "Advance to Trafalgar Square. If you pass Go, collect £200.":
            previous_position = player.position
            traf_position = 24
            player.position = traf_position

            # collect pass go money
            if previous_position > traf_position:
                player.receive(200)

            # pay rent if owned, if not decide to purchase/not
            street = self.board[traf_position]
            self.handle_property(player, street)

        elif chance_card == "Advance to Mayfair. If you pass Go, collect £200.":
            previous_position = player.position
            mayf_position = 39
            player.position = mayf_position

            # collect pass go money
            if previous_position > mayf_position:
                player.receive(200)

            # pay rent if owned, if not decide to purchase/not
            street = self.board[mayf_position]
            self.handle_property(player, street)

        elif chance_card == "Advance to Pall Mall. If you pass Go, collect £200.":
            previous_position = player.position
            pall_position = 11
            player.position = pall_position

            # collect pass go money
            if previous_position > pall_position:
                player.receive(200)

            # pay rent if owned, if not decide to purchase/not
            street = self.board[pall_position]
            self.handle_property(player, street)

        elif chance_card == "Advance to the nearest Station. If unowned, you may buy it from the Bank. \
            If owned, pay the owner twice the rental to which they are otherwise entitled.":
            if 5 <= player.position <= 14:
                idx = 15
                player.position = idx
            elif 15 <= player.position <= 24:
                idx = 25
                player.position = idx
            elif 25 <= player.position <= 34:
                idx = 35
                player.position = idx
            else:
                idx = 5
                player.position = idx

            # pay rent if owned, if not decide to purchase/not
            station = self.board[idx]
            self.handle_property(player, station)

        elif chance_card == "Advance token to nearest Utility. If unowned, you may buy it from the Bank. \
            If owned, throw dice and pay owner a total ten times the amount thrown.":
            if 12 <= player.position <= 27:
                idx = 28
                player.position = idx
            else:
                idx = 12
                player.position = idx

            # pay rent if owned, if not decide to purchase/not
            utility = self.board[idx]
            self.handle_property(player, utility, dice_roll)

        elif chance_card == "Bank pays you a dividend of £50.":
            player.receive(50)

        elif chance_card == "Get Out of Jail Free.":
            player.jail_cards += 1

        elif chance_card == "Go back 3 Spaces.":
            player.move(-3)

            # position of player is either community chest, vine street or income tax
            if player.position == 4:
                # pay income tax
                tax = self.board[4].calculate_tax(player)
                if player.money >= tax:
                    player.pay(tax)
                else:
                    self.raise_funds(player, tax)

            elif player.position == 19:
                # pay rent if owned, if not decide to purchase/not
                street = self.board[19]
                self.handle_property(player, street)

            elif player.position == 33:
                # perform community chest actions
                self.perform_community_chest(player)
            else:
                pass

        elif chance_card == "Go to Jail. Go directly to Jail, do not pass Go, do not collect £200.":
            player.position = 10
            player.in_jail = True

        elif chance_card == "Make general repairs on all your property. For each house pay £25. For each hotel pay £100":
            cost = 25*player.houses + 100*player.hotels
            if player.money >= cost:
                player.pay(cost)
            else:
                self.raise_funds(player, cost)

        elif chance_card == "Speeding fine £15.":
            if player.money >= 15:
                player.pay(15)
            else:
                self.raise_funds(player, 15)

        elif chance_card == "Take a trip to King's Cross Station. If you pass Go, collect £200.":
            previous_position = player.position
            king_position = 5
            player.position = king_position

            # collect pass go money
            if previous_position > king_position:
                player.receive(200)

            # pay rent if owned, if not decide to purchase/not
            station = self.board[king_position]
            self.handle_property(player, station)

        elif chance_card == "You have been elected Chairman of the Board. Pay each player £50.":
            for opponent in self.players:
                if player.money >= 50:
                    player.pay(50)
                    opponent.receive(50)
                else:
                    self.raise_funds(opponent, 50)

        elif chance_card == "Your building loan matures. Collect £150.":
            player.receive(150)

        else:
            # TO DO: RAISE CARD TYPE ERROR (AND IN ORIGINAL MONOPOLYBOARD CLASS)
            return
            
    def perform_community_chest(self, player):
        """
        This method executes a player picking a community chest card from the top of the 
        community chest card pile. The method draws a card from the stack contained within an 
        instance of the CommunityChest object. The method then handles the card that is chosen 
        from the stack.
        
        Parameters
        ----------
        player: obj
            Instance of the class Player.
        
        Returns
        -------
        None
        """
        community_chest_card = self.community_chest.choose_card()

        if community_chest_card == "Advance to Go.":
            player.position = 0
            player.receive(200)

        elif community_chest_card == "Bank error in your favor. Collect £200.":
            player.receive(200)
        
        elif community_chest_card == "Doctor’s fee. Pay £50.":
            if player.money >= 50:
                player.pay(50)
            else:
                self.raise_funds(player, 50)
        
        elif community_chest_card == "From sale of stock you get £50.":
            player.receive(50)
        
        elif community_chest_card == "Get Out of Jail Free.":
            player.jail_cards += 1
        
        elif community_chest_card == "Go to Jail. Go directly to jail, do not pass Go, do not collect £200.":
            player.position = 10
            player.in_jail = True
        
        elif community_chest_card == "Holiday fund matures. Receive £100.":
            player.receive(100)
        
        elif community_chest_card == "Income tax refund. Collect £20.":
            player.receive(20)
        
        elif community_chest_card == "It is your birthday. Collect £10 from every player.":
            for opponent in self.players:
                if opponent.money >= 10:
                    player.receive(10)
                    opponent.pay(10)
                else:
                    self.raise_funds(opponent, 10)
        
        elif community_chest_card == "Life insurance matures. Collect £100.":
            player.receive(100)
        
        elif community_chest_card == "Pay hospital fees of £100.":
            if player.money >= 100:
                player.pay(100)
            else:
                self.raise_funds(player, 100)
        
        elif community_chest_card == "Pay school fees of £50.":
            if player.money >= 50:
                player.pay(50)
            else:
                self.raise_funds(player, 50)
        
        elif community_chest_card == "Receive £25 consultancy fee.":
            player.receive(25)
        
        elif community_chest_card == "You are assessed for street repairs. £40 per house. £115 per hotel.":
            cost = 40*player.houses + 115*player.hotels
            if player.money >= cost:
                player.pay(cost)
            else:
                self.raise_funds(player, cost)
        
        elif community_chest_card == "You have won second prize in a beauty contest. Collect £10.":
            player.receive(10)
        
        elif community_chest_card == "You inherit £100.":
            player.receive(100)
        
        else:
            # TO DO: RAISE CARD TYPE ERROR (AND IN ORIGINAL MONOPOLYBOARD CLASS)
            return

    def handle_property(self, player, space, dice_roll = 0):
        """
        This method handles the case when a player lands on a property. First, the method checks
        if the space has an owner. If it does, the player must pay the owner the calculated rent
        on the property. If not, the player must decide whether or not to purchase the property.
        
        Parameters
        ----------
        player: obj
            An instance of the class Player.
        space: obj
            An instance of one of the classes Street/Station/Utility.
        dice_roll: int, optional, default: 0
            The value on the dice that the player rolled.
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the space type on the game board is not recognised or is of an incorrect type.
        """
        # if there is an owner, pay calculated rent on property
        if space.owner:
            if space.type == "Street":
                rent = space.calculate_rent()
            elif space.type == "Station":
                rent = space.calculate_rent(len(space.owner.stations))
            elif space.type == "Utility":
                rent = space.calculate_rent(dice_roll, len(space.owner.utilities))
            else:
                raise TypeError("Cannot pay rent on space of type" + space.type)  
            
            if player.money >= rent:
                player.pay(rent)
                space.owner.receive(rent)
            else:
                self.raise_funds(player, rent)

        # otherwise, decide whether to buy property
        elif self.strategy.decide_to_buy(player, space):
            space.owner = player
            player.pay(space.price)

            if space.type == "Street":
                player.properties.append(space)
                player.property_sets[space.group].append(space)
            elif space.type == "Station":
                player.stations.append(space)
            elif space.type == "Utility":
                player.utilities.append(space)
            else:
                raise TypeError("Cannot purchase space of type" + space.type) 
            
        else:
            return

    def raise_funds(self, player, cost):
        """
        This method raises funds for a player by selling houses and mortgaging properties (using 
        methods from the Strategy class). The method first attempts to sell any houses that the 
        player has on properties, and then mortgage properties. If neither of these options 
        mean that the player has money that is greater than or equal to the cost, they go bankrupt.
        
        Parameters
        ----------
        player: obj
            An instance of the class Player
        cost: int
            The amount of money that the player requires.
        
        Returns
        -------
        None
        """
        # sell houses to pay
        self.strategy.decide_sell_houses(player, cost - player.money)
        if player.money >= cost:
            player.pay(cost)
        else:
            # mortgage properties to pay
            self.strategy.decide_mortgage_properties(player, cost - player.money)
            if player.money >= cost:
                player.pay(cost)

            # when all houses/hotels are sold & properties mortgaged, player goes bankrupt
            # TO DO: PLAYER WILL NOT GO BANKRUPT IN THE CASE THAT THEY WANT TO PURCHASE 
            # SOMETHING ELSE WITH THE MONEY RATHER THAN PAY SOMEONE/BANK
            else:
                player.bankrupt = True

    def get_legal_actions(self):
        legal_actions = []

        # player can mortgage unmortgaged properties at any point given they are not built on
        unmortgaged_streets = [prop for prop in self.agent.properties if not prop.is_mortgaged and prop.num_houses == 0]
        unmortgaged_stations = [station for station in self.agent.stations if not station.is_mortgaged]
        unmortgaged_utilities = [utility for utility in self.agent.utilities if not utility.is_mortgaged]
        unmortgaged_properties = unmortgaged_streets + unmortgaged_stations + unmortgaged_utilities
        for prop in unmortgaged_properties:
            legal_actions.append(f"Mortgage {prop.name}")

        # player can sell hotels at any point (will never result in >1 discrepency between properties)
        sell_hotel_streets = [prop for prop in self.agent.properties if prop.hotel]
        for prop in sell_hotel_streets:
            legal_actions.append(f"Sell hotel on {prop.name}")

        # player can sell houses given house discrepency is <=1
        sell_house_streets = [prop for prop in self.agent.properties if prop.num_houses > 0 and not prop.hotel]
        for prop in sell_house_streets:
            new_prop_build = prop.num_houses + prop.hotel - 1
            house_discrepencies = [abs(new_prop_build - i.num_houses - i.hotel) <= 1 for i in self.agent.property_sets[prop.group]]

            if all(house_discrepencies):
                legal_actions.append(f"Sell house on {prop.name}")

        # if the player owes money, their only valid options are to mortgage, sell houses & hotels (above)
        if len(self.agent.money_owed) == 0:

            # if the player is in jail, legal options include using jail cards/paying
            if self.agent.in_jail:
                if self.agent.jail_cards > 0:
                    legal_actions.append("Use Get Out of Jail Free card")
                if self.agent.money >= 50:
                    legal_actions.append("Pay 50 to get out of jail")

            # if the player is in jail and must leave, their only valid options are mortgaging, selling houses/hotels, or getting out of jail (above)
            if not (self.agent.in_jail and self.agent.turns_in_jail > 2):

                # player can unmortgage mortgaged properties at any point given they have enough money
                mortgaged_streets = [prop for prop in self.agent.properties if prop.is_mortgaged]
                mortgaged_stations = [station for station in self.agent.stations if station.is_mortgaged]
                mortgaged_utilities = [utility for utility in self.agent.utilities if utility.is_mortgaged]
                mortgaged_properties = mortgaged_streets + mortgaged_stations + mortgaged_utilities
                for prop in mortgaged_properties:
                    if self.agent.money >= prop.calculate_unmortgage_price():
                        legal_actions.append(f"Unmortgage {prop.name}")

                # player can buy hotels at any point if they have 4 houses, no hotel, enough money & <=1 house discrepency
                buy_hotel_streets = [prop for prop in self.agent.properties if prop.num_houses==4 and not prop.hotel]
                for prop in buy_hotel_streets:
                    new_prop_build = prop.num_houses + prop.hotel + 1
                    house_discrepencies = [abs(new_prop_build - i.num_houses - i.hotel) <= 1 for i in self.agent.property_sets[prop.group]]

                    if all(house_discrepencies) and self.agent.money >= prop.house_price:
                        legal_actions.append(f"Buy hotel on {prop.name}")

                # player can buy houses at any point if they have fewer than 4 houses, enough money, a set & <= house discrepency
                buy_house_streets = [prop for prop in self.agent.properties if prop.num_houses < 4]
                for prop in buy_house_streets:
                    group = self.property_sets[prop.group]
                    player_group = self.agent.property_sets[prop.group]
                    new_prop_build = prop.num_houses + prop.hotel + 1
                    house_discrepencies = [abs(new_prop_build - i.num_houses - i.hotel) <= 1 for i in self.agent.property_sets[prop.group]]

                    if all(house_discrepencies) and self.agent.money >= prop.house_price and sorted(group) == sorted(player_group):
                        legal_actions.append(f"Buy house on {prop.name}")

                # if the player is on an unowned property, they can purchase it given they have enough money
                space = self.board[self.agent.position]
                is_property = (space.type == "Street" or space.type == "Station" or space.type == "Utility")
                if is_property and space.owner == None and self.agent.money >= space.price:
                    legal_actions.append(f"Purchase {space.name}")

                legal_actions.append("End turn")

        # if the player has no options, they are bankrupt
        if len(legal_actions) == 0:
            self.agent.bankrupt = True

        return legal_actions

    def perform_action(self, action):
        # TO DO: IF A PLAYER OWES MONEY, PAY IT OFF WITH MONEY THEY GET FROM MORTGAGING/SELLING HOUSES
        # unmortgage property
        if action.startswith("Unmortgage"):
            property_name = action[len("Unmortgage"):].strip()
            prop = self.properties_dict[property_name]

            unmortgage_cost = prop.calculate_unmortgage_price()
            self.agent.pay(unmortgage_cost)
            prop.is_mortgaged = False

        # mortgage property
        if action.startswith("Mortgage"):
            property_name = action[len("Mortgage"):].strip()
            prop = self.properties_dict[property_name]

            mortgage_value = prop.calculate_mortgage_value()
            self.agent.receive(mortgage_value)
            prop.is_mortgaged = True

        # sell hotel on property
        if action.startswith("Sell hotel on"):
            property_name = action[len("Sell hotel on"):].strip()
            prop = self.properties_dict[property_name]

            hotel_value = prop.calculate_house_sale_value()
            self.agent.receive(hotel_value)
            prop.hotel = False

        # sell house on property
        if action.startswith("Sell house on"):
            property_name = action[len("Sell house on"):].strip()
            prop = self.properties_dict[property_name]

            house_value = prop.calculate_house_sale_value()
            self.agent.receive(house_value)
            prop.num_houses -= 1

        # buy hotel on property
        if action.startswith("Buy hotel on"):
            property_name = action[len("Buy hotel on"):].strip()
            prop = self.properties_dict[property_name]

            self.agent.pay(prop.house_price)
            prop.hotel = True

        # buy house on property
        if action.startswith("Buy house on"):
            property_name = action[len("Buy house on"):].strip()
            prop = self.properties_dict[property_name]

            self.agent.pay(prop.house_price)
            prop.num_houses += 1

        # use get out of jail free card
        if action == "Use Get Out of Jail Free card":
            self.agent.jail_cards -= 1
            self.agent.in_jail = False
            self.agent.turns_in_jail = 0

        # pay to leave jail
        if action == "Pay 50 to get out of jail":
            self.agent.pay(50)
            self.agent.in_jail = False
            self.agent.turns_in_jail = 0

        # purchase property
        if action.startswith("Purchase"):
            property_name = action[len("Purchase"):].strip()
            prop = self.properties_dict[property_name]

            self.agent.pay(prop.price)
            prop.owner = self.agent

            if prop.type == "Street":
                self.agent.properties.append(prop)
                self.agent.property_sets[prop.group].append(prop)
            elif prop.type == "Station":
                self.agent.stations.append(prop)
            elif prop.type == "Utility":
                self.agent.utilities.append(prop)
            else:
                raise TypeError("Cannot purchase space of type" + prop.type)
        
        # if player owes money, pay it
        if len(self.agent.money_owed) > 0:
            items_to_delete = []

            for recipient, amount in self.agent.money_owed.items():

                # money owed to another player is payed if possible
                if recipient:
                    if self.agent.money >= amount:
                        self.agent.pay(amount)
                        recipient.receive(amount)
                        items_to_delete.append(recipient)
                    else:
                        pass

                # money owed to the bank is payed if possible
                else:
                    if self.agent.money >= amount:
                        self.agent.pay(amount)
                        items_to_delete.append(recipient)
                    else:
                        pass

            for recipient in items_to_delete:
                del self.agent.money_owed[recipient]
        
        # end of player's turn
        if action == "End turn":
            self.rounds += 1

            # if the player rolled doubles, they go again
            if self.agent.double_rolled:
                self.agent_turn()
                return

            # other players have their turns
            else:
                for other_player in self.other_players:
                    self.take_turn(other_player)

                self.agent_turn()
                return

    def agent_turn(self):
        # player rolls the dice
        a_roll = random.randint(1, 6)
        b_roll = random.randint(1, 6)
        dice_roll = a_roll + b_roll

        if self.agent.in_jail:
            self.agent.turns_in_jail += 1

            if self.agent.turns_in_jail > 2:
                if a_roll == b_roll:
                    self.agent.in_jail = False
                    self.agent.turns_in_jail = 0
                else:
                    return
                    
        if a_roll == b_roll:
            self.agent.num_doubles += 1

        # go to jail if third double in a row and end turn
        if self.agent.num_doubles > 2:
            self.agent.position = 10
            self.agent.in_jail = True
            self.agent.num_doubles = 0
            self.agent.double_rolled = False
            return
            
        # player moves the number of spaces shown on the two dice combined
        previous_position = self.agent.position
        self.agent.move(dice_roll)
        new_position = self.agent.position
        space = self.board[new_position]

        # if the player passed go, collect the Go income
        if previous_position > new_position:
            self.agent.receive(self.board[0].income)

        # handle street property
        if space.type == "Street":
            self.handle_property_agent(space)

        # handle station property
        elif space.type == "Station":
            self.handle_property_agent(space)

        # handle utility property
        elif space.type == "Utility":
            self.handle_property_agent(space, dice_roll)

        # handle chance
        elif space.type == "Chance":
            self.perform_chance_agent(dice_roll)

        # handle community chest
        elif space.type == "Community Chest":
            self.perform_community_chest_agent()

        # player pays tax if possible, otherwise they owe the money and must pay at next 'move'/child node
        elif space.type == "Tax":
            tax = space.calculate_tax(self.agent)
            self.handle_bank_payment_agent(tax)

        # no action is taken if the player lands on Go
        elif space.type == "Go":
            pass
            
        # no action is taken if the player lands on jail since they are just visiting
        elif space.type == "Jail":
            pass

        # no action is taken if the player lands on free parking
        elif space.type == "Free Parking":
            pass

        # player goes to jail
        elif space.type == "Go To Jail":
            self.agent.position = 10
            self.agent.in_jail = True

        else:
            raise TypeError("Space of incorrect type found on board. Type: " + space.type)
        
    def perform_chance_agent(self, dice_roll):
        chance_card = self.chance.choose_card()

        if chance_card == "Advance to Go.":
            self.agent.position = 0
            self.agent.receive(200)

        elif chance_card == "Advance to Trafalgar Square. If you pass Go, collect £200.":
            previous_position = self.agent.position
            traf_position = 24
            self.agent.position = traf_position

            # collect pass go money
            if previous_position > traf_position:
                self.agent.receive(200)

            street = self.board[traf_position]
            self.handle_property_agent(street)

        elif chance_card == "Advance to Mayfair. If you pass Go, collect £200.":
            previous_position = self.agent.position
            mayf_position = 39
            self.agent.position = mayf_position

            # collect pass go money
            if previous_position > mayf_position:
                self.agent.receive(200)

            street = self.board[mayf_position]
            self.handle_property_agent(street)

        elif chance_card == "Advance to Pall Mall. If you pass Go, collect £200.":
            previous_position = self.agent.position
            pall_position = 11
            self.agent.position = pall_position

            # collect pass go money
            if previous_position > pall_position:
                self.agent.receive(200)

            street = self.board[pall_position]
            self.handle_property_agent(street)

        elif chance_card == "Advance to the nearest Station. If unowned, you may buy it from the Bank. \
            If owned, pay the owner twice the rental to which they are otherwise entitled.":
            if 5 <= self.agent.position <= 14:
                idx = 15
                self.agent.position = idx
            elif 15 <= self.agent.position <= 24:
                idx = 25
                self.agent.position = idx
            elif 25 <= self.agent.position <= 34:
                idx = 35
                self.agent.position = idx
            else:
                idx = 5
                self.agent.position = idx

            station = self.board[idx]
            self.handle_property_agent(station)

        elif chance_card == "Advance token to nearest Utility. If unowned, you may buy it from the Bank. \
            If owned, throw dice and pay owner a total ten times the amount thrown.":
            if 12 <= self.agent.position <= 27:
                idx = 28
                self.agent.position = idx
            else:
                idx = 12
                self.agent.position = idx

            utility = self.board[idx]
            self.handle_property_agent(utility, dice_roll)

        elif chance_card == "Bank pays you a dividend of £50.":
            self.agent.receive(50)

        elif chance_card == "Get Out of Jail Free.":
            self.agent.jail_cards += 1

        elif chance_card == "Go back 3 Spaces.":
            self.agent.move(-3)

            # position of player is either community chest, vine street or income tax
            if self.agent.position == 4:
                # income tax
                space = self.board[4]
                tax = space.calculate_tax(self.agent)
                self.handle_bank_payment_agent(tax)

            elif self.agent.position == 19:
                # vine street
                street = self.board[19]
                self.handle_property_agent(street)

            elif self.agent.position == 33:
                # perform community chest actions
                self.perform_community_chest_agent()

            else:
                # TO DO: ADD RAISE ERROR HERE
                pass

        elif chance_card == "Go to Jail. Go directly to Jail, do not pass Go, do not collect £200.":
            self.agent.position = 10
            self.agent.in_jail = True

        elif chance_card == "Make general repairs on all your property. For each house pay £25. For each hotel pay £100.":
            cost = 25*self.agent.houses + 100*self.agent.hotels
            self.handle_bank_payment_agent(cost)

        elif chance_card == "Speeding fine £15.":
            self.handle_bank_payment_agent(15)

        elif chance_card == "Take a trip to King's Cross Station. If you pass Go, collect £200.":
            previous_position = self.agent.position
            king_position = 5
            self.agent.position = king_position

            # collect pass go money
            if previous_position > king_position:
                self.agent.receive(200)

            station = self.board[king_position]
            self.handle_property_agent(station)

        elif chance_card == "You have been elected Chairman of the Board. Pay each player £50.":
            for other_player in self.other_players:
                self.handle_opponent_payment_agent(50, other_player)

        elif chance_card == "Your building loan matures. Collect £150.":
            self.agent.receive(150)

        else:
            # TO DO: RAISE CARD TYPE ERROR (AND ABOVE FOR OTHER PLAYERS)
            return
        
    def perform_community_chest_agent(self):
        community_chest_card = self.community_chest.choose_card()

        if community_chest_card == "Advance to Go.":
            self.agent.position = 0
            self.agent.receive(200)

        elif community_chest_card == "Bank error in your favor. Collect £200.":
            self.agent.receive(200)
        
        elif community_chest_card == "Doctor’s fee. Pay £50.":
            self.handle_bank_payment_agent(50)
        
        elif community_chest_card == "From sale of stock you get £50.":
            self.agent.receive(50)
        
        elif community_chest_card == "Get Out of Jail Free.":
            self.agent.jail_cards += 1
        
        elif community_chest_card == "Go to Jail. Go directly to jail, do not pass Go, do not collect £200.":
            self.agent.position = 10
            self.agent.in_jail = True
        
        elif community_chest_card == "Holiday fund matures. Receive £100.":
            self.agent.receive(100)
        
        elif community_chest_card == "Income tax refund. Collect £20.":
            self.agent.receive(20)
        
        elif community_chest_card == "It is your birthday. Collect £10 from every player.":
            for opponent in self.players:
                if opponent.money >= 10:
                    self.agent.receive(10)
                    opponent.pay(10)
                else:
                    self.raise_funds(opponent, 10)
        
        elif community_chest_card == "Life insurance matures. Collect £100.":
            self.agent.receive(100)
        
        elif community_chest_card == "Pay hospital fees of £100.":
            self.handle_bank_payment_agent(100)
        
        elif community_chest_card == "Pay school fees of £50.":
            self.handle_bank_payment_agent(50)
        
        elif community_chest_card == "Receive £25 consultancy fee.":
            self.agent.receive(25)
        
        elif community_chest_card == "You are assessed for street repairs. £40 per house. £115 per hotel.":
            cost = 40*self.agent.houses + 115*self.agent.hotels
            self.handle_bank_payment_agent(cost)
        
        elif community_chest_card == "You have won second prize in a beauty contest. Collect £10.":
            self.agent.receive(10)
        
        elif community_chest_card == "You inherit £100.":
            self.agent.receive(100)
        
        else:
            # TO DO: RAISE CARD TYPE ERROR (AND ABOVE FOR OTHER PLAYERS)
            return
        
    def handle_property_agent(self, space, dice_roll = 0):
        # if there is an owner, pay calculated rent on property if possible
        if space.owner:
            if space.type == "Street":
                rent = space.calculate_rent()
            elif space.type == "Station":
                rent = space.calculate_rent(len(space.owner.stations))
            elif space.type == "Utility":
                rent = space.calculate_rent(dice_roll, len(space.owner.utilities))
            else:
                raise TypeError("Cannot pay rent on space of type" + space.type)  
            
            # pay rent if sufficient funds to do so
            if self.agent.money >= rent:
                self.agent.pay(rent)
                space.owner.receive(rent)

            # otherwise player owes money and must raise funds at next 'move'/child node
            else:
                self.agent.money_owed[space.owner] = rent

        # otherwise player will have option to purchase property in next 'move'/child node
        else:
            return
        
    def handle_bank_payment_agent(self, amount):
        if self.agent.money >= amount:
            self.agent.pay(amount)
        else:
            self.agent.money_owed[None] = amount

    def handle_opponent_payment_agent(self, amount, opponent):
        if self.agent.money >= amount:
            self.agent.pay(amount)
            opponent.receive(amount)
        else:
            self.agent.money_owed[opponent] = amount

    def is_terminal(self):
        if self.agent.bankrupt or all([other_player.bankrupt for other_player in self.other_players]):
            return True
        else:
            return False
        
    def calculate_reward(self):
        if self.agent.bankrupt:
            return 0
        else:
            return self.agent.wealth()/np.mean([other_player.wealth() for other_player in self.other_players])