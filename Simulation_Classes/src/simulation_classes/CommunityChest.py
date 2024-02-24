import random
class CommunityChest:
    """
    This class represents the Community Chest spaces in a Monopoly game. It includes attributes to
    track the type of space, its location on the board, and a deck of Community Chest cards.

    Attributes
    ----------
    type: str
        The type of space (set to 'Community Chest').
    loc: int
        The position of the Community Chest spaces on the Monopoly board.
    cards: list
        A list of Community Chest cards in the deck.
    top_card_idx: int
        The index of the top card in the deck.

    Methods
    -------
    __init__(locs)
        Initialises the Community Chest space with its location and a shuffled deck of 
        Community Chest cards.
    __repr__()
        Provides a string representation of the Community Chest space, including the top card.
    __lt__(other)
        Compares two spaces based on their locations on the Monopoly board.
    choose_card()
        Draws and returns the top card from the deck of Community Chest cards.
    """

    def __init__(self, locs):
        self.type = "Community Chest"
        self.loc = locs
        self.cards = [
            "Advance to Go.",
            "Bank error in your favor. Collect £200.",
            "Doctor’s fee. Pay £50.",
            "From sale of stock you get £50.",
            "Get Out of Jail Free.",
            "Go to Jail. Go directly to jail, do not pass Go, do not collect £200.",
            "Holiday fund matures. Receive £100.",
            "Income tax refund. Collect £20.",
            "It is your birthday. Collect £10 from every player.",
            "Life insurance matures. Collect £100.",
            "Pay hospital fees of £100.",
            "Pay school fees of £50.",
            "Receive £25 consultancy fee.",
            "You are assessed for street repairs. £40 per house. £115 per hotel.",
            "You have won second prize in a beauty contest. Collect £10.",
            "You inherit £100."
        ]
        random.shuffle(self.cards)
        self.top_card_idx = 0

    def __repr__(self):
        """
        This method provides a string representation of the CommunityChest class, including all
        relevant attributes. This ensures that a printed community chest object displays something
        that is interpretable (printed string).
        
        Parameters
        ----------
        None

        Returns
        -------
        str
            String representation of class.
        """
        return f'Community chest spaces are located at positions {self.loc} on the Monopoly board. \
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
        This method chooses the top card from the pile of community chest cards and returns this 
        card as a string.

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