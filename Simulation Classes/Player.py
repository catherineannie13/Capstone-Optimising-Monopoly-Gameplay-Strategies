class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.properties = []
        self.stations = []
        self.utilities = []
        self.property_sets = {"brown":[], "lightblue":[], "pink":[], "orange":[], 
                              "red":[], "yellow":[], "green":[], "darkblue":[]}
        self.bankrupt = False
        self.in_jail = False
        self.turns_in_jail = 0
        self.jail_cards = 0
        self.houses = 0
        self.hotels = 0

    def move(self, steps):
        self.position = (self.position + steps) % 40

    def pay(self, amount):
        self.money -= amount

    def receive(self, amount):
        self.money += amount

    def buy_property(self, property):
        if property.owner is None and self.money >= property.price:
            self.properties.append(property)
            self.property_Sets[property.group].append(property)
            self.pay(property.price)
            property.owner = self
            return True
        return False
    
    def buy_station(self, station):
        if station.owner is None and self.money >= station.price:
            self.stations.append(station)
            self.pay(station.price)
            station.owner = self
            return True
        return False

    def buy_utility(self, utility):
        if utility.owner is None and self.money >= utility.price:
            self.utilities.append(utility)
            self.pay(utility.price)
            utility.owner = self
            return True
        return False