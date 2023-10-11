class Utility:
    def __init__(self, name, price, rent_multiplier, rent_multiplier_two, loc):
        self.name = name
        self.price = price
        self.type = "Utility"
        self.rent_multipliers = [rent_multiplier, rent_multiplier_two]
        self.loc = loc
        self.owner = None

    def calculate_rent(self, dice_roll, utilities_owned):
        if self.owner:
            multipler = self.rent_multipliers[utilities_owned - 1]
            return multipler * dice_roll
        else:
            return 0