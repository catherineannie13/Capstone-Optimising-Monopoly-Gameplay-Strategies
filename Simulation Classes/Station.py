class Station:
    """
    This class represents a station property in a Monopoly game. It includes attributes 
    to track the station's name, price, rents, location, owner, and mortgage status.

    Attributes
    ----------
    name: str
        The name of the station property.
    price: float
        The purchase price of the property.
    type: str
        The type of property (set to 'Station').
    rents: lst
        A list of rents based on the number of stations owned (1-4).
    loc: int
        The position of the station property on the Monopoly board.
    owner: obj
        The player who currently owns the property.
    is_mortgaged: bool
        A flag indicating whether the property is mortgaged.

    Methods
    -------
    __init__(name, price, rent_one, rent_two, rent_three, rent_four, loc)
        Initialises the attributes of the station property.
    __repr__()
        Provides a string representation of the station property, including relevant 
        attributes.
    __lt__(other)
        Compares two properties based on their locations on the Monopoly board.
    calculate_rent(stations_owned)
        Calculates the rent on this station property based on the number of stations 
        owned by the owner.
    calculate_mortgage_value()
        Calculates the mortgage value of the property.
    calculate_unmortgage_price()
        Calculates the cost of unmortgaging this property.
    """

    def __init__(self, name, price, rent_one, rent_two, rent_three, rent_four, loc):
        self.name = name
        self.price = price
        self.type = "Station"
        self.rents = [rent_one, rent_two, rent_three, rent_four]
        self.loc = loc
        self.owner = None
        self.is_mortgaged = False

    def __repr__(self):
        """
        This method provides a string representation of the Station class, including all
        relevant attributes. This ensures that a printed station object displays something
        that is interpretable (printed string).
        
        Parameters
        ----------
        None

        Returns
        -------
        str
            String representation of class.
        """
        return f'{self.name} is a station located at position {self.loc} on the Monopoly board that can be purchased for {self.price}.\
            \n Rent is as follows: \
            \n Rent if a single station is owned: {self.rents[0]} \
            \n Rent if two stations are owned: {self.rents[1]} \
            \n Rent if three stations are owned: {self.rents[2]} \
            \n Rent if four stations are owned: {self.rents[3]} \
            \n This property is currently owned by {self.owner.name if self.owner else "no-one"} and is{"" if self.is_mortgaged else " not"} mortgaged.'
    
    def __lt__(self, other):
        """
        This operator method compares two objects based on their locations on the Monopoly 
        board. It ensures that two objects can be compared.

        Parameters
        ----------
        other: obj
            The object to compare to the self (this object).

        Returns
        -------
        bool
            Whether or not the location of this object is less than the location of the other
            object.
        """
        return self.loc < other.loc

    def calculate_rent(self, stations_owned):
        """
        This method calculates the rent on this station property. If there is an owner, 
        the rent is given based on the number of stations owned by that player.

        Parameters
        ----------
        stations_owned: int
            The number of stations owned by the own of this station.
        
        Returns
        -------
        int
            The rent to be paid on this station.
        """
        if self.owner:
            return self.rents[stations_owned - 1]
        else:
            return 0
        
    def calculate_mortgage_value(self):
        """
        This method calculates the mortgage value of the property.

        Parameters
        ----------
        None

        Returns
        -------
        float
            The mortgage price of the property.
        """
        return int(self.price/2)
    
    def calculate_unmortgage_price(self):
        """
        This method calculates the cost of unmortgaging this property, 
        given that it is mortgaged to begin with.

        Parameters
        ----------
        None

        Returns
        -------
        float
            The price to unmortgage this property.
        """
        return int((self.price/2)*1.1)