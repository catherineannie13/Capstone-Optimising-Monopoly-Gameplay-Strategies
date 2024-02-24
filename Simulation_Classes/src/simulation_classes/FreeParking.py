class FreeParking:
    """
    This class represents the Free Parking space in a Monopoly game. It includes attributes to
    track the type of space and its location on the board.

    Attributes
    ----------
    type: str
        The type of space (set to 'Free Parking').
    loc: int
        The position of the Free Parking space on the Monopoly board.

    Methods
    -------
    __init__(loc)
        Initialises the Free Parking space with its location.
    __repr__()
        Provides a string representation of the Free Parking space.
    __lt__(other)
        Compares two spaces based on their locations on the Monopoly board.
    """
    def __init__(self, loc):
        self.type = "Free Parking"
        self.loc = loc

    def __repr__(self):
        """
        This method provides a string representation of the FreeParking class, including all
        relevant attributes. This ensures that a printed free parking object displays something
        that is interpretable (printed string).
        
        Parameters
        ----------
        None

        Returns
        -------
        str
            String representation of class.
        """
        return f'Free parking is located at position {self.loc} on the Monopoly board.'
    
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