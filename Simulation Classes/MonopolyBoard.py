from Chance import Chance
from CommunityChest import CommunityChest
from FreeParking import FreeParking
from Go import Go
from GoToJail import GoToJail
from Jail import Jail
from Player import Player
from Station import Station
from Strategy import Strategy
from RandomStrategy import RandomStrategy
from Street import Street
from Tax import Tax
from Utility import Utility
import random
class MonopolyBoard:
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

    def add_player(self, player):
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
        
        # player goes to jail and revoke pass go money immediately
        elif space.type == "Go To Jail":
            player.position = 10
            player.in_jail = True

            # in the case that the player goes to jail, they don't collect go money
            player.pay(self.board[0].income)

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
                raise TypeError("Cannot purchase space of type" + space.type)  
            
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