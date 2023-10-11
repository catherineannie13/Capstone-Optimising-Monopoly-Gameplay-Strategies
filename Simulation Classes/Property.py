class Property:
    def __init__(self, name, price, house_price, rent, one_house, two_houses, three_houses, four_houses, hotel, loc, group, num_in_group):
        self.name = name
        self.price = price
        self.house_price = house_price
        self.type = "Property"
        self.rent = rent
        self.double_rent = self.rent * 2
        self.house_rent = [one_house, two_houses, three_houses, four_houses]
        self.hotel_rent = hotel
        self.num_houses = 0
        self.hotel = False
        self.loc = loc
        self.group = group
        self.num_in_group = num_in_group
        self.owner = None

    def calculate_rent(self):
        if self.owner:
            if self.num_houses == 0:
                return self.rent
            elif self.hotel:
                return self.hotel_rent
            else:
                return self.house_rent[self.num_houses - 1]
        else:
            return 0