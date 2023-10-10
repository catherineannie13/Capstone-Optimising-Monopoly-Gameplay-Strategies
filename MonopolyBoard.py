class MonopolyBoard:
    def __init__(self):
        self.players = []
        self.board = [None]*40
        self.properties = []
        self.stations = []
        self.utilities = []
        self.tax = []
        self.property_sets = {"brown":[], "lightblue":[], "pink":[], "orange":[], 
                              "red":[], "yellow":[], "green":[], "darkblue":[]}

        self.create_properties()
        self.create_stations()
        self.create_utilities()
        self.create_chance()
        self.create_community_chest()
        self.create_tax()
        self.create_go()
        self.create_jail()
        self.create_free_parking()
        self.create_go_to_jail()

    def create_properties(self):
        property_data = [
            ("Old Kent Road", 60, 50, 2, 10, 30, 90, 160, 250, 1, "brown", 2),
            ("Whitechapel Road", 60, 50, 4, 20, 60, 180, 320, 450, 3, "brown", 2),
            ("The Angel Islington", 100, 50, 6, 30, 90, 270, 400, 550, 6, "lightblue", 3),
            ("Euston Road", 100, 50, 6, 30, 90, 270, 400, 550, 8, "lightblue", 3),
            ("Pentonville Road", 120, 50, 8, 40, 100, 300, 450, 600, 9, "lightblue", 3),
            ("Pall Mall", 140, 100, 10, 50, 150, 450, 625, 750, 11, "pink", 3),
            ("Whitehall", 140, 100, 10, 50, 150, 450, 625, 750, 13, "pink", 3),
            ("Northumberland Avenue", 160, 100, 12, 60, 180, 500, 700, 900, 14, "pink", 3),
            ("Bow Street", 180, 100, 14, 70, 200, 550, 750, 950, 16, "orange", 3),
            ("Marlborough Street", 180, 100, 14, 70, 200, 550, 750, 950, 18, "orange", 3),
            ("Vine Street", 200, 100, 16, 80, 220, 600, 800, 1000, 19, "orange", 3),
            ("The Strand", 220, 150, 18, 90, 250, 700, 875, 1050, 21, "red", 3),
            ("Fleet Street", 220, 150, 18, 90, 250, 700, 875, 1050, 23, "red", 3),
            ("Trafalgar Square", 240, 150, 20, 100, 300, 750, 925, 1100, 24, "red", 3),
            ("Leicester Square", 260, 150, 22, 110, 330, 800, 975, 1150, 26, "yellow", 3),
            ("Coventry Street", 260, 150, 22, 110, 330, 800, 975, 1150, 27, "yellow", 3),
            ("Piccadilly", 280, 150, 24, 120, 360, 850, 1025, 1200, 29, "yellow", 3),
            ("Regent Street", 300, 200, 26, 130, 390, 900, 1100, 1275, 31, "green", 3),
            ("Oxford Street", 300, 200, 26, 130, 390, 900, 1100, 1275, 32, "green", 3),
            ("Bond Street", 320, 200, 28, 150, 450, 1000, 1200, 1400, 34, "green", 3),
            ("Park Lane", 350, 200, 35, 175, 500, 1100, 1300, 1500, 37, "darkblue", 2),
            ("Mayfair", 400, 200, 50, 200, 600, 1400, 1700, 2000, 39, "darkblue", 2)
        ]

        for name, price, house_price, rent, one_house, two_houses, three_houses, four_houses, hotel, loc, group, num_in_group in property_data:
            property = Property(name, price, house_price, rent, one_house, two_houses, three_houses, four_houses, hotel, loc, group, num_in_group)
            self.properties.append(property)
            self.board[loc] = property
            self.property_sets[group].append(property)

    def create_stations(self):
        station_data = [
            ("King's Cross Station", 200, 25, 50, 100, 200, 5),
            ("Marylebone Station", 200, 25, 50, 100, 200, 15),
            ("Fenchurch St. Station", 200, 25, 50, 100, 200, 25),
            ("Liverpool St. Station", 200, 25, 50, 100, 200, 35)
        ]
        
        for name, price, rent_one, rent_two, rent_three, rent_four, loc in station_data:
            station = Station(name, price, rent_one, rent_two, rent_three, rent_four, loc)
            self.stations.append(station)
            self.board[loc] = station

    def create_utilities(self):
        utility_data = [
            ("Electric Company", 150, 4, 10, 12),
            ("Water Works", 150, 4, 10, 28)
        ]
        
        for name, price, rent_multiplier, rent_multiplier_two, loc in utility_data:
            utility = Utility(name, price, rent_multiplier, rent_multiplier_two, loc)
            self.utilities.append(utility)
            self.board[loc] = utility

    def create_chance(self):
        chance_locs = [7, 22, 36]

        chance = Chance(chance_locs)
        self.chance = chance

        for loc in chance_locs:
            self.board[loc] = chance

    def create_community_chest(self):
        community_chest_locs = [2, 17, 33]

        community_chest = CommunityChest(loc)
        self.community_chest = community_chest

        for loc in community_chest_locs:
            self.board[loc] = community_chest

    def create_tax(self):
        tax_data = [
            ("Income Tax", 200, 4),
            ("Super Tax", 100, 38)
        ]

        for name, amount, loc in tax_data:
            tax = Tax(name, amount, loc)
            self.tax.append(tax)
            self.board[loc] = tax

    def create_go(self):
        loc = 0
        go = Go(200, loc)
        self.board[loc] = go

    def create_jail(self):
        loc = 10
        jail = Jail(loc)
        self.board[loc] = jail

    def create_free_parking(self):
        loc = 20
        free_parking = FreeParking(loc)
        self.board[loc] = free_parking

    def create_go_to_jail(self):
        loc = 30
        go_to_jail = GoToJail(loc)
        self.board[loc] = go_to_jail

    def add_player(self, player):
        self.players.append(player)

    def play_game(self):
        while len(self.players) > 1:
            for player in self.players:
                self.take_turn(player)

    def take_turn(self, player, doubles = 0):
        # TO DO: PLAYER DECIDES WHETHER TO BUILD ON PROPERTIES IF POSSIBLE
        self.build_on_properties(player)

        # player rolls the dice
        a_roll = random.randint(1, 6)
        b_roll = random.randint(1, 6)
        dice_roll = a_roll + b_roll

        # if the player is in jail
        if player.in_jail:
            player.turns_in_jail += 1

            # player must leave jail after 3 rounds
            if player.turns_in_jail > 2:
                if a_roll == b_roll:
                    pass
                elif player.jail_cards > 0:
                    player.jail_cards -= 1
                else:
                    player.pay(50)
                
                player.in_jail = False

            # decide whether or not to leave jail before 3 rounds
            elif self.decide_to_leave_jail():
                    player.in_jail = False

            # not leaving jail so turn is over
            else:
                return

        # count consecutive doubles for player
        if a_roll == b_roll:
            doubles += 1

        # go to jail if third double in a row and end turn
        if doubles > 2:
            player.position = 10
            player.in_jail = True
            return
            
        # player moves the number of spaces shown on the two dice combined
        previous_space = self.board[player.position]
        player.move(dice_roll)
        space = self.board[player.position]

        # if the player passed go, collect the Go income
        if previous_space > space:
            player.receive(self.board[0].income)

        if space.type == "Property":
            # pay rent if owned, if not decide to purchase/not
            if space.owner:
                rent = space.calculate_rent()
                player.pay(rent)
                space.owner.receive(rent)
            elif self.decide_to_buy(player, space):
                space.owner = player
                player.properties.append(space)
                player.pay(space.price)
            else:
                pass

        elif space.type == "Station":
            # pay rent if owned, if not decide to purchase/not
            if space.owner:
                rent = space.calculate_rent(len(space.owner.stations))
                player.pay(rent)
                space.owner.receive(rent)
            elif self.decide_to_buy(player, space):
                space.owner = player
                player.properties.append(space)
                player.pay(space.price)
            else:
                pass

        elif space.type == "Utility":
            # pay rent if owned, if not decide to purchase/not
            if space.owner:
                rent = space.calculate_rent(dice_roll, len(space.owner.utilities))
                player.pay(rent)
                space.owner.receive(rent)
            elif self.decide_to_buy(player, space):
                space.owner = player
                player.properties.append(space)
                player.pay(space.price)
            else:
                pass
        
        # handle chance card outcomes
        elif space.type == "Chance":
            self.perform_chance(player, dice_roll)

        # handle community chest card outcomes
        elif space.type == "Community Chest":
            self.perform_community_chest(player)

        # player pays the tax amount to the bank and no further action is taken
        elif space.type == "Tax":
            player.pay(self.board[space].amount)

        # no action is taken if the player lands on Go
        elif space.type == "Go":
            pass
        
        # no action is taken if the player lands on jail since they are just visiting
        elif space.type == "Jail":
            pass

        # no action is taken if the player lands on free parking
        elif space.type == "Free Parking":
            pass
        
        # player goes to jail and revoke pass go money immediately
        elif space.type == "Go To Jail":
            player.position = 10
            player.in_jail = True

            # in the case that the player goes to jail, they don't collect go money
            player.pay(self.board[0].income)

        else:
            raise TypeError("Space of incorrect type found on board. Type: " + space)
        
        # player takes another turn if they roll a double
        if a_roll == b_roll:
            self.take_turn(player, doubles)
        else:
            return
        
    def perform_chance(self, player, dice_roll):
        chance_card = self.chance.choose_card()

        if chance_card == "Advance to Go.":
            player.position = 0
            player.receive(200)

        elif chance_card == "Advance to Trafalgar Square. If you pass Go, collect £200.":
            previous_position = player.position
            traf_position = 24
            player.position = traf_position

            # collect pass go money
            if previous_position > traf_position:
                player.receive(200)

            # pay rent if owned, if not decide to purchase/not
            property = self.board[traf_position]
            if property.owner:
                rent = property.calculate_rent()
                player.pay(rent)
                property.owner.receive(rent)
            elif self.decide_to_buy(player, property):
                property.owner = player
                player.properties.append(property)
                player.pay(property.price)
            else:
                pass

        elif chance_card == "Advance to Mayfair. If you pass Go, collect £200.":
            previous_position = player.position
            mayf_position = 39
            player.position = mayf_position

            # collect pass go money
            if previous_position > mayf_position:
                player.receive(200)

            # pay rent if owned, if not decide to purchase/not
            property = self.board[mayf_position]
            if property.owner:
                rent = property.calculate_rent()
                player.pay(rent)
                property.owner.receive(rent)
            elif self.decide_to_buy(player, property):
                property.owner = player
                player.properties.append(property)
                player.pay(property.price)
            else:
                pass

        elif chance_card == "Advance to Pall Mall. If you pass Go, collect £200.":
            previous_position = player.position
            pall_position = 11
            player.position = pall_position

            # collect pass go money
            if previous_position > pall_position:
                player.receive(200)

            # pay rent if owned, if not decide to purchase/not
            property = self.board[pall_position]
            if property.owner:
                rent = property.calculate_rent()
                player.pay(rent)
                property.owner.receive(rent)
            elif self.decide_to_buy(player, property):
                property.owner = player
                player.properties.append(property)
                player.pay(property.price)
            else:
                pass

        elif chance_card == "Advance to the nearest Station. If unowned, you may buy it from the Bank. \
            If owned, pay the owner twice the rental to which they are otherwise entitled.":
            # TO DO: SHOULD YOU GET MONEY FOR PASSING GO???
            if 5 <= player.position <= 14:
                idx = 15
                player.position = idx
            elif 15 <= player.position <= 24:
                idx = 25
                player.position = idx
            elif 25 <= player.position <= 34:
                idx = 35
                player.position = idx
            else:
                idx = 5
                player.position = idx

            # pay rent if owned, if not decide to purchase/not
            station = self.board[idx]
            if station.owner:
                rent = station.calculate_rent(len(station.owner.stations))
                player.pay(rent)
                station.owner.receive(rent)
            elif self.decide_to_buy(player, station):
                station.owner = player
                player.stations.append(station)
                player.pay(station.price)
            else:
                pass

        elif chance_card == "Advance token to nearest Utility. If unowned, you may buy it from the Bank. \
            If owned, throw dice and pay owner a total ten times the amount thrown.":
            # TO DO: SHOULD YOU GET MONEY FOR PASSING GO???
            if 12 <= player.position <= 27:
                idx = 28
                player.position = idx
            else:
                idx = 12
                player.position = idx

            # pay rent if owned, if not decide to purchase/not
            utility = self.board[idx]
            if utility.owner:
                rent = utility.calculate_rent(dice_roll, len(utility.owner.stations))
                player.pay(rent)
                utility.owner.receive(rent)
            elif self.decide_to_buy(player, utility):
                utility.owner = player
                player.utilities.append(utility)
                player.pay(utility.price)
            else:
                pass

        elif chance_card == "Bank pays you a dividend of £50.":
            player.receive(50)

        elif chance_card == "Get Out of Jail Free.":
            player.jail_cards += 1

        elif chance_card == "Go back 3 Spaces.":
            player.move(-3)

            # position of player is either community chest, vine street or income tax
            if player.position == 4:
                # pay income tax
                player.pay(self.board[4].amount)

            elif player.position == 19:
                # pay rent if owned, if not decide to purchase/not
                property = self.board[19]
                if property.owner:
                    rent = property.calculate_rent()
                    player.pay(rent)
                    property.owner.receive(rent)
                elif self.decide_to_buy(player, property):
                    property.owner = player
                    player.properties.append(property)
                    player.pay(property.price)
                else:
                    pass

            elif player.position == 33:
                # perform community chest actions
                self.perform_community_chest(player)
            else:
                pass

        elif chance_card == "Go to Jail. Go directly to Jail, do not pass Go, do not collect £200.":
            player.position = 10
            player.in_jail = True

        elif chance_card == "Make general repairs on all your property. For each house pay £25. For each hotel pay £100":
            player.pay(25*player.houses + 100*player.hotels)

        elif chance_card == "Speeding fine £15.":
            player.pay(15)

        elif chance_card == "Take a trip to King's Cross Station. If you pass Go, collect £200.":
            previous_position = player.position
            king_position = 5
            player.position = king_position

            # collect pass go money
            if previous_position > king_position:
                player.receive(200)

            # pay rent if owned, if not decide to purchase/not
            station = self.board[king_position]
            if station.owner:
                rent = station.calculate_rent(len(station.owner.stations))
                player.pay(rent)
                station.owner.receive(rent)
            elif self.decide_to_buy(player, station):
                station.owner = player
                player.stations.append(property)
                player.pay(station.price)
            else:
                pass

        elif chance_card == "You have been elected Chairman of the Board. Pay each player £50.":
            for opponent in self.players:
                player.pay(50)
                opponent.receive(50)

        elif chance_card == "Your building loan matures. Collect £150.":
            player.receive(150)

        else:
            return
            
    def perform_community_chest(self, player):
        community_chest_card = self.community_chest.choose_card()

        if community_chest_card == "Advance to Go.":
            player.position = 0
            player.receive(200)

        elif community_chest_card == "Bank error in your favor. Collect £200.":
            player.receive(200)
        
        elif community_chest_card == "Doctor’s fee. Pay £50.":
            player.pay(50)
        
        elif community_chest_card == "From sale of stock you get £50.":
            player.receive(50)
        
        elif community_chest_card == "Get Out of Jail Free.":
            player.jail_cards += 1
        
        elif community_chest_card == "Go to Jail. Go directly to jail, do not pass Go, do not collect £200.":
            player.position = 10
            player.in_jail = True
        
        elif community_chest_card == "Holiday fund matures. Receive £100.":
            player.receive(100)
        
        elif community_chest_card == "Income tax refund. Collect £20.":
            player.receive(20)
        
        elif community_chest_card == "It is your birthday. Collect £10 from every player.":
            for opponent in self.players:
                opponent.pay(10)
                player.recieve(10)
        
        elif community_chest_card == "Life insurance matures. Collect £100.":
            player.receive(100)
        
        elif community_chest_card == "Pay hospital fees of £100.":
            player.pay(100)
        
        elif community_chest_card == "Pay school fees of £50.":
            player.pay(50)
        
        elif community_chest_card == "Receive £25 consultancy fee.":
            player.receive(25)
        
        elif community_chest_card == "You are assessed for street repairs. £40 per house. £115 per hotel.":
            player.pay(40*player.houses + 115*player.hotels)
        
        elif community_chest_card == "You have won second prize in a beauty contest. Collect £10.":
            player.receive(10)
        
        elif community_chest_card == "You inherit £100.":
            player.receive(100)
        
        else:
            return

    def decide_to_buy(self, player, property):
        # TO DO: MAKE THIS REFLECT A BASE STRATEGY FOR BUYING/NOT BUYING A PROPERTY
        return True
    
    def decide_to_leave_jail(self, player):
        # TO DO: MAKE THIS REFLECT BASE STRATEGY FOR LEAVING/NOT LEAVING JAIL
        # TO DO: ENCOMPASS KNOWLEDGE ABOUT GET OUT OF JAIL CARDS AND MONEY
        return True
    
    def build_on_properties(self, player):
        
        # look through all property groups
        for group, properties in enumerate(self.property_sets):
            player_properties = player.property_sets[group]

            # determine if the entire set is owned
            if sorted(properties) == sorted(player_properties):
                for property in properties:
                    
                    # decision to develop property or not
                    if self.decide_to_build(player):
                        player.pay(property.house_price)
                        property.num_houses += 1

    def decide_to_build(self, player):
        # TO DO: MAKE THIS REFLECT BASE STRATEGY FOR BUILDING ON PROPERTIES
        return True