class Player:
    """
    This class represents a player in a Monopoly game. It includes attributes to track 
    the player's name, position on the board, money, properties, stations, utilities, 
    property sets, jail status, turns in jail, jail cards, houses, and hotels.

    Attributes
    ----------
    name: str
        The name of the player.
    position: int
        The current position of the player on the board.
    money: float
        The amount of money the player has.
    properties: lst
        A list of street properties owned by the player.
    stations: lst
        A list of station properties owned by the player.
    utilities: lst
        A list of utility properties owned by the player.
    property_sets: dict
        A dictionary that tracks the player's property sets by group.
    bankrupt: bool
        A flag indicating if the player is bankrupt.
    in_jail: bool
        A flag indicating if the player is in jail.
    turns_in_jail: int
        The number of turns the player has spent in jail.
    jail_cards: int
        The number of 'Get Out of Jail' cards the player holds.
    houses: int
        The number of houses the player owns.
    hotels: int
        The number of hotels the player owns.

    Methods
    -------
    __init__(name)
        Initialises the attributes of the player.
    __repr__()
        Provides a string representation of the player, including relevant attributes.
    move(steps)
        Moves the player to a different location on the Monopoly board based on a given 
        number of steps.
    pay(amount)
        Deducts a given amount from the player's money.
    receive(amount)
        Adds a given amount to the player's money.
    buy_property(street)
        Purchases a street property for the player.
    buy_station(station)
        Purchases a station property for the player.
    buy_utility(utility)
        Purchases a utility property for the player.
    wealth()
        Calculates the wealth of the player, considering money, properties, and buildings.
    """

    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.properties = []
        self.stations = []
        self.utilities = []
        self.property_sets = {"brown":[], "lightblue":[], "pink":[], "orange":[], 
                              "red":[], "yellow":[], "green":[], "darkblue":[]}
        #self._bankrupt = False
        self.bankrupt = False
        self.in_jail = False
        self.turns_in_jail = 0
        self.double_rolled = False
        self.num_doubles = 0
        self.jail_cards = 0
        self.houses = 0
        self.hotels = 0
        self.money_owed = {}

    def __repr__(self):
        """
        This method provides a string representation of the Player class, including all
        relevant attributes. This ensures that a printed player object displays something
        that is interpretable (printed string).
        
        Parameters
        ----------
        None

        Returns
        -------
        str
            String representation of class.
        """
        return f'Player {self.name} is currently as position {self.position} on the board, with ${round(self.money, 2)}. \
            \n They hold the following properties: {[street.name for street in self.properties]}.\
            \n They hold the following stations: {[station.name for station in self.stations]}\
            \n They hold the following utilities: {[utility.name for utility in self.utilities]}\
            \n The player has {self.houses} houses and {self.hotels} hotels \
            \n The player is currently {"in" if self.in_jail else "not in"} jail.'
    
    #@property
    #def bankrupt(self):
    #    return self._bankrupt

    #@bankrupt.setter
    #def bankrupt(self, value):
    #    # TO DO: CHANGE THIS TO WHATEVER ACTION TO PERFORM WHEN A PLAYER GOES BANKRUPT
    #    if self._bankrupt is False and value is True:
    #        print(f'Player {self.name} has gone bankrupt.')
    #    self._bankrupt = value

    def move(self, steps):
        """
        This method moves a player to a different location on a Monopoly board based on a
        given number of steps.
        
        Parameters
        ----------
        steps: int
            The number of steps to move a player forward.

        Returns
        -------
        None
        """
        self.position = (self.position + steps) % 40

    def pay(self, amount):
        """
        This method deducts a given amount from the player's money.
        
        Parameters
        ----------
        amount: float
            The amount of money to deduct from the player's money.

        Returns
        -------
        None
        """
        self.money -= amount

    def receive(self, amount):
        """
        This method adds a given amount to the player's money.
        
        Parameters
        ----------
        amount: float
            The amount of money to add to the player's money.

        Returns
        -------
        None
        """
        self.money += amount

    def buy_property(self, street):
        """
        This method purchases a street property for the player. It first checks that
        there is no current owner and that the player has sufficient funds, then the
        property is added to the player's properties and the player pays the price for
        the given property.
        
        Parameters
        ----------
        street: obj
            An instance of the Street class. A property that the player will purchase
            if possible.

        Returns
        -------
        bool
            Whether or not the player purchased the property.
        """
        if street.owner is None and self.money >= street.price:
            self.properties.append(street)
            self.property_sets[street.group].append(street)
            self.pay(street.price)
            street.owner = self
            return True
        return False
    
    def buy_station(self, station):
        """
        This method purchases a station property for the player. It first checks that
        there is no current owner and that the player has sufficient funds, then the
        property is added to the player's properties and the player pays the price for
        the given property.
        
        Parameters
        ----------
        station: obj
            An instance of the Station class. A property that the player will purchase
            if possible.

        Returns
        -------
        bool
            Whether or not the player purchased the property.
        """
        if station.owner is None and self.money >= station.price:
            self.stations.append(station)
            self.pay(station.price)
            station.owner = self
            return True
        return False

    def buy_utility(self, utility):
        """
        This method purchases a utility property for the player. It first checks that
        there is no current owner and that the player has sufficient funds, then the
        property is added to the player's properties and the player pays the price for
        the given property.
        
        Parameters
        ----------
        utility: obj
            An instance of the Utility class. A property that the player will purchase
            if possible.

        Returns
        -------
        bool
            Whether or not the player purchased the property.
        """
        if utility.owner is None and self.money >= utility.price:
            self.utilities.append(utility)
            self.pay(utility.price)
            utility.owner = self
            return True
        return False
    
    def wealth(self):
        """
        This method calculates the wealth of the player. It sums the value of: money that
        the player possesses; any properties that the player holds, both mortgaged and unmortgaged;
        the buildings that the player owns, both houses and hotels.
        
        Parameters
        ----------
        None

        Returns
        -------
        float
            The calculated wealth of the player.
        """
        street_wealth = sum([street.price if street.is_mortgaged == False else 0 for street in self.properties])
        street_mortgaged_wealth = sum([street.calculate_mortgage_value() if street.is_mortgaged else 0 for street in self.properties])
        station_wealth = sum([station.price for station in self.stations])
        utility_wealth = sum([utility.price for utility in self.utilities])
        house_wealth = sum([street.num_houses*street.house_price for street in self.properties])
        hotel_wealth = sum([street.hotel*street.house_price for street in self.properties])
        money_wealth = self.money

        return street_wealth + street_mortgaged_wealth + station_wealth + utility_wealth + house_wealth + hotel_wealth + money_wealth