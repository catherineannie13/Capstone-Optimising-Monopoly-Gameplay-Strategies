class Station:
    def __init__(self, name, price, rent_one, rent_two, rent_three, rent_four, loc):
        self.name = name
        self.price = price
        self.type = "Station"
        self.rents = [rent_one, rent_two, rent_three, rent_four]
        self.loc = loc
        self.owner = None

    def calculate_rent(self, stations_owned):
        if self.owner:
            return self.rents[stations_owned - 1]
        else:
            return 0