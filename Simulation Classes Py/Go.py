class Go:
    """
    This class represents the Go space in a Monopoly game. It includes attributes to
    track the income received and the location on the board.

    Attributes
    ----------
    income: float
        The income that players receive every time they pass the Go space.
    type: str
        The type of space (set to 'Go').
    loc: int
        The position of the Go space on the Monopoly board.

    Methods
    -------
    __init__(income, loc)
        Initialises the Go space with its income and location.
    __repr__()
        Provides a string representation of the Go space, including the income.
    __lt__(other)
        Compares two spaces based on their locations on the Monopoly board.
    """
    def __init__(self, income, loc):
        self.income = income
        self.type = "Go"
        self.loc = loc

    def __repr__(self):
        """
        This method provides a string representation of the Go class, including all
        relevant attributes. This ensures that a printed go object displays something
        that is interpretable (printed string).
        
        Parameters
        ----------
        None

        Returns
        -------
        str
            String representation of class.
        """
        return f'Go is located at position {self.loc} on the Monopoly board. Players receive {self.income} every time they pass go.'
    
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