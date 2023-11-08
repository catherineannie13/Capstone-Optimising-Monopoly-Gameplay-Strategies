class Chance:
    """
    This class represents the Chance spaces in a Monopoly game. It includes attributes to
    track the type of space, its location on the board, and a deck of Chance cards.

    Attributes
    ----------
    type: str
        The type of space (set to 'Chance').
    loc: int
        The position of the Chance spaces on the Monopoly board.
    cards: list
        A list of Chance cards in the deck.
    top_card_idx: int
        The index of the top card in the deck.

    Methods
    -------
    __init__(locs)
        Initialises the Chance space with its location and a shuffled deck of Chance cards.
    __repr__()
        Provides a string representation of the Chance space, including the top card.
    __lt__(other)
        Compares two spaces based on their locations on the Monopoly board.
    choose_card()
        Draws and returns the top card from the deck of Chance cards.
    """

    def __init__(self, locs):
        self.type = "Chance"
        self.loc = locs
        self.cards = [
            "Advance to Go.",
            "Advance to Trafalgar Square. If you pass Go, collect £200.",
            "Advance to Mayfair. If you pass Go, collect £200.",
            "Advance to Pall Mall. If you pass Go, collect £200.",
            "Advance to the nearest Station. If unowned, you may buy it from the Bank. If owned, pay the owner twice the rental to which they are otherwise entitled.",
            "Advance to the nearest Station. If unowned, you may buy it from the Bank. If owned, pay the owner twice the rental to which they are otherwise entitled.",
            "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times the amount thrown.",
            "Bank pays you a dividend of £50.",
            "Get Out of Jail Free.",
            "Go back 3 Spaces.",
            "Go to Jail. Go directly to Jail, do not pass Go, do not collect £200.",
            "Make general repairs on all your property. For each house pay £25. For each hotel pay £100",
            "Speeding fine £15.",
            "Take a trip to King's Cross Station. If you pass Go, collect £200.",
            "You have been elected Chairman of the Board. Pay each player £50.",
            "Your building loan matures. Collect £150."
        ]
        random.shuffle(self.cards)
        self.top_card_idx = 0

    def __repr__(self):
        """
        This method provides a string representation of the Chance class, including all
        relevant attributes. This ensures that a printed chance object displays something
        that is interpretable (printed string).
        
        Parameters
        ----------
        None

        Returns
        -------
        str
            String representation of class.
        """
        return f'Chance spaces are located at positions {self.loc} on the Monopoly board. \
            \n The card on the top of the pile is: "{self.cards[self.top_card_idx]}".'

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

    def choose_card(self):
        """
        This method chooses the top card from the pile of chance cards and returns this card as
        a string.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The string of the card on the top of the pile.
        """
        card = self.cards[self.top_card_idx]
        self.top_card_idx = (self.top_card_idx + 1) % len(self.cards)
        return card