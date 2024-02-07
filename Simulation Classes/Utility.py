class Utility:
    """
    This class represents a utility property in a Monopoly game. It includes attributes 
    to track the utility's name, price, rent multipliers, location, owner, and mortgage status.

    Attributes
    ----------
    name: str
        The name of the utility property.
    price: float
        The purchase price of the property.
    type: str
        The type of property (set to 'Utility').
    rent_multipliers: list
        A list of rent multipliers based on the number of utilities owned (1-2).
    loc: int
        The position of the utility property on the Monopoly board.
    owner: Player
        The player who currently owns the property.
    is_mortgaged: bool
        A flag indicating whether the property is mortgaged.

    Methods
    -------
    __init__(name, price, rent_multiplier, rent_multiplier_two, loc)
        Initialises the attributes of the utility property.
    __repr__()
        Provides a string representation of the utility property, including relevant attributes.
    __lt__(other)
        Compares two properties based on their locations on the Monopoly board.
    calculate_rent(dice_roll, utilities_owned)
        Calculates the rent on this utility property based on the relevant multiplier and dice roll, 
        considering the number of utilities owned.
    calculate_mortgage_value()
        Calculates the mortgage value of the property.
    calculate_unmortgage_price()
        Calculates the cost of unmortgaging this property.
    """

    def __init__(self, name, price, rent_multiplier, rent_multiplier_two, loc):
        self.name = name
        self.price = price
        self.type = "Utility"
        self.rent_multipliers = [rent_multiplier, rent_multiplier_two]
        self.loc = loc
        self.owner = None
        self.is_mortgaged = False

    def __repr__(self):
        """
        This method provides a string representation of the Utility class, including all
        relevant attributes. This ensures that a printed utility object displays something
        that is interpretable (printed string).
        
        Parameters
        ----------
        None

        Returns
        -------
        str
            String representation of class.
        """
        return f'{self.name} is a utility located at position {self.loc} on the Monopoly board that can be purchased for {self.price}.\
            \n If a player owns a single utility, they must be paid {self.rent_multipliers[0]} multiplied by the dice roll in rent.\
            \n If a player owns both utilities, they must by paid {self.rent_multipliers[1]} multiplied by the dice roll in rent.\
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

    def calculate_rent(self, dice_roll, utilities_owned):
        """
        This method calculates the rent on this utility property. If there is an owner, 
        the rent is given based on the relevant multiplier times the given dice roll.

        Parameters
        ----------
        dice_roll: int
            The dice roll rolled by the player.
        utilities_owned: int
            The number of utilities owned by the own of this utility.
        
        Returns
        -------
        int
            The rent to be paid on this utility.
        """
        if self.owner:
            multipler = self.rent_multipliers[utilities_owned - 1]
            return int(multipler * dice_roll)
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