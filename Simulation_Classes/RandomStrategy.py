import random
class RandomStrategy:
    """
    A class representing a random strategy for making decisions in Monopoly gameplay.

    Attributes
    ----------
    strategy : str
        The name of the strategy.

    Methods
    -------
    decide_to_buy(player, space)
        Determines whether the player should buy a space.
    decide_sell_houses(player, money_needed)
        Decides which houses to sell to raise the required amount of money.
    decide_mortgage_properties(player, money_needed)
        Determines which properties to mortgage to raise the required amount of money.
    decide_to_leave_jail(player)
        Decides whether the player should leave jail.
    decide_unmortgage_properties(player)
        Determines which properties to unmortgage.
    decide_build_on_properties(player, property_sets)
        Decides whether to build houses or hotels on properties.
    decide_to_build_house(player, street)
        Determines whether to build a house on a street.
    decide_to_build_hotel(player, street)
        Determines whether to build a hotel on a street.
    """

    def __init__(self):
        self.strategy = "Random strategy"

    def decide_to_buy(self, player, space):
        """
        Determines whether the player should buy a space.

        Parameters
        ----------
        player : Player
            The player making the decision.
        space : Space
            The space to be bought.

        Returns
        -------
        bool
            True if the player should buy the space, False otherwise.
        """
        if player.money >= space.price:
            return random.choice([True, False])
        else:
            return False
        
    def decide_sell_houses(self, player, money_needed):
        """
        Decides which houses to sell to raise the required amount of money.

        Parameters
        ----------
        player : Player
            The player selling houses.
        money_needed : int
            The amount of money needed.

        Returns
        -------
        None
        """
        money_raised = 0

        # get property groups that player owns
        property_sets = [(group, properties) for group, properties in player.property_sets.items()]
        random.shuffle(property_sets) 

        for group, properties in property_sets:
            while money_raised < money_needed:

                # get properties in group with houses & sort by number of houses & hotels
                properties_with_houses = [prop for prop in properties if (prop.num_houses + prop.hotel) > 0]
                properties_with_houses.sort(key = lambda x: x.num_houses + x.hotel, reverse = True)

                # sell house from property with most houses & hotels
                if properties_with_houses:
                    property_to_sell = properties_with_houses[0]

                    # sell hotel if possible
                    if property_to_sell.hotel:
                        property_to_sell.hotel = False

                        # 4 houses replace the hotel on the property
                        player.hotels -= 1
                        player.houses += 4

                    # if not, sell house
                    else:
                        property_to_sell.num_houses -= 1
                        player.houses -= 1

                    sale_value = property_to_sell.calculate_house_sale_value()
                    money_raised += sale_value
                    player.money += sale_value

                # no more houses in this group, move to next group
                else:
                    break

    def decide_mortgage_properties(self, player, money_needed):
        """
        Determines which properties to mortgage to raise the required amount of money.

        Parameters
        ----------
        player : Player
            The player mortgaging properties.
        money_needed : int
            The amount of money needed.

        Returns
        -------
        None
        """
        # combine all of the player's properties (streets, stations, and utilities) without buildings
        undeveloped_streets = [prop for prop in player.properties if prop.num_houses == 0]
        all_properties = undeveloped_streets + player.stations + player.utilities

        # sort combined list of properties by mortgage value (least valuable first)
        random.shuffle(all_properties)

        money_raised = 0

        # iterate through the player's properties and mortgage them until enough money is raised
        for prop in all_properties:
            if not prop.is_mortgaged:
                
                mortgage_value = prop.calculate_mortgage_value()

                prop.is_mortgaged = True
                money_raised += mortgage_value
                player.money += mortgage_value

            # check if enough money has been raised to meet the target
            if money_raised >= money_needed:
                break

    def decide_to_leave_jail(self, player):
        """
        Decides whether the player should leave jail.

        Parameters
        ----------
        player : Player
            The player in jail.

        Returns
        -------
        bool
            True if the player should leave jail, False otherwise.
        """
        if player.jail_cards > 0 and random.random() < 0.5:
            player.jail_cards -= 1
            return True
        elif player.money >= 50 and random.random() < 0.5:
            player.pay(50)
            return True
        else:
            return False
        
    def decide_unmortgage_properties(self, player):
        """
        Determines which properties to unmortgage.

        Parameters
        ----------
        player : Player
            The player unmortgaging properties.

        Returns
        -------
        None
        """
        # get all mortgaged properties
        mortgaged_streets = [prop for prop in player.properties if prop.is_mortgaged]
        mortgaged_stations = [station for station in player.stations if station.is_mortgaged]
        mortgaged_utilities = [utility for utility in player.utilities if utility.is_mortgaged]
        mortgaged_properties = mortgaged_streets + mortgaged_stations + mortgaged_utilities 
        random.shuffle(mortgaged_properties)

        for prop in mortgaged_properties:
            unmortgage_cost = prop.calculate_unmortgage_price()
            
            # if the player has enough money to unmortgage the property and randomly chosen
            if player.money >= unmortgage_cost and random.random() < 0.5:
                player.pay(unmortgage_cost)
                prop.is_mortgaged = False
            else:
                break
        

    def decide_build_on_properties(self, player, property_sets):
        """
        Decides whether to build houses or hotels on properties.

        Parameters
        ----------
        player : Player
            The player deciding to build.
        property_sets : dict
            A dictionary mapping property groups to their corresponding properties.

        Returns
        -------
        None
        """
        # look through all property groups
        for group, properties in property_sets.items():
            player_properties = player.property_sets[group]

            # determine if the entire set is owned
            if sorted(properties) == sorted(player_properties):
                for street in properties:
                    
                    # mortgaged properties cannot be built on
                    if street.is_mortgaged:
                        pass

                    # decision to develop property or not (house)
                    elif self.decide_to_build_house(player, street):
                        player.pay(street.house_price)
                        street.num_houses += 1
                        player.houses += 1

                    # decision to develop the property or not (hotel)
                    elif self.decide_to_build_hotel(player, street):
                        player.pay(street.house_price)
                        street.hotel = True

                        # 4 houses are replaced by a hotel on the property
                        player.hotels += 1
                        player.houses -= 4
                        
                    else:
                        pass

    def decide_to_build_house(self, player, street):
        """
        Determines whether to build a house on a street.

        Parameters
        ----------
        player : Player
            The player deciding to build.
        street : Street
            The street to build a house on.

        Returns
        -------
        bool
            True if the player should build a house, False otherwise.
        """
        if street.num_houses < 4 and player.money >= street.house_price:

            # get neighbouring properties in the same set
            neighbouring_properties = [prop for prop in player.property_sets[street.group] if prop != street]

            # check if there is no greater than 1 house difference on neighbouring properties
            for neighbour_property in neighbouring_properties:
                if abs(street.num_houses - neighbour_property.num_houses) > 1:
                    return False 

            # randomly decide whether to build or not
            if random.random() < 0.5:
                return True 
        
        else:
            return False
        
    def decide_to_build_hotel(self, player, street):
        """
        Determines whether to build a hotel on a street.

        Parameters
        ----------
        player : Player
            The player deciding to build.
        street : Street
            The street to build a hotel on.

        Returns
        -------
        bool
            True if the player should build a hotel, False otherwise.
        """
        if street.num_houses == 4 and not street.hotel and player.money >= street.house_price:

            # get neighbouring properties in the same set
            neighbouring_properties = [prop for prop in player.property_sets[street.group] if prop != street]

            # check if there is no greater than 1 house difference on neighbouring properties
            for neighbour_property in neighbouring_properties:
                if abs(street.num_houses + street.hotel - neighbour_property.num_houses - neighbour_property.hotel) > 1:
                    return False  

            # randomly decide whether to build or not
            if random.random() < 0.5:
                return True 
        
        else:
            return False