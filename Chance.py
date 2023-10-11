class Chance:
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

    def choose_card(self):
        card = self.cards[self.top_card_idx]
        self.top_card_idx = (self.top_card_idx + 1) % len(self.cards)
        return card