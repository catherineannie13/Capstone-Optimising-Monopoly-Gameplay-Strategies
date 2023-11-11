class Tax:
    """
    This class represents the Tax spaces in a Monopoly game. It includes attributes to
    track the name, tax amount, type of space, and its location on the board.

    Attributes
    ----------
    name: str
        The name of the Tax space (e.g., "Income Tax").
    amount: float
        The tax amount that players must pay when they land on this space.
    type: str
        The type of space (set to 'Tax').
    loc: int
        The position of the Tax space on the Monopoly board.

    Methods
    -------
    __init__(name, amount, loc)
        Initialises the Tax space with its name, tax amount, and location.
    __repr__()
        Provides a string representation of the Tax space, including the name and tax amount.
    __lt__(other)
        Compares two spaces based on their locations on the Monopoly board.
    calculate_tax(player)
        Calculates the amount of tax that a player must pay when landing on this Tax space.
    """
    def __init__(self, name, amount, loc):
        self.name = name
        self.amount = amount
        self.type = "Tax"
        self.loc = loc

    def __repr__(self):
        """
        This method provides a string representation of the Tax class, including all
        relevant attributes. This ensures that a printed tax object displays something
        that is interpretable (printed string).
        
        Parameters
        ----------
        None

        Returns
        -------
        str
            String representation of class.
        """
        return f'{self.name} is located at position {self.loc} on the Monopoly board. Players must pay {self.amount} if they land here.\
            \n {"Alternatively, they can pay 10 percent of their wealth." if self.name == "Income Tax" else ""}'
    
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
    
    def calculate_tax(self, player):
        """
        This method calculates the amount of tax that the player must pay. If the player lands
        on Income Tax, they can either pay the tax value or 10% of their wealth.

        Parameters
        ----------
        player: obj
            An instance of the Player class.

        Returns
        -------
        float
            The amount of tax that the player must pay.
        """
        if self.name == "Income Tax":
            base = self.amount
            alternative = 0.1 * player.wealth()
            return min([base, alternative])
        else:
            return self.amount