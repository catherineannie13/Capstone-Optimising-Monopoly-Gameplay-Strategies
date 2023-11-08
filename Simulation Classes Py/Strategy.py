class Strategy:
    """
    This class represents a base strategy for players playing a Monopoly game. It provides methods 
    for handling decisions such as whether or not to purchase a propery, whether or not to build on
    a property, and whether or not to pay to get out of jail.

    Attributes
    ----------
    strategy: str
        The type of strategy contained within the class.
    
    Methods
    -------
    __init__()
        Initialises the attributes of the class.
    decide_to_buy(player, space)
        This method makes the decision for a player to purchase/not purchase a given property.
    decide_sell_houses(player, money_needed)
        This method is responsible for determining which houses and hotels a player should sell to 
        raise money.
    decide_mortgage_properties(player, money_needed)
        This method determines which properties the player should mortgage to raise the required 
        amount of money.
    decide_to_leave_jail(player)
        This method makes the decision as to whether or not a player should leave jail (given that 
        they have a choice).
    decide_unmortgage_properties(player)
        This method makes the decision on whether or not to unmortgage properties.
    decide_build_on_properties(player, property_sets)
        This method determines whether the player should build houses or hotels on their owned 
        property sets.
    decide_to_build_house(player, street)
        This method evaluates whether the player should build a house on a given street property.
    decide_to_build_hotel(player, street)
        This method evaluates whether the player should build a hotel on a given street property.
    """

    def __init__(self):
        self.strategy = "Base strategy"

    def decide_to_buy(self, player, space):
        """
        This method makes the decision for a player to purchase/not purchase a given property.
        The method first checks if the player has sufficient funds to purchase the property. It
        then follows the strategy: if a player already has a property in a set, purchase the 
        property; if a player has fewer than 3 street properties, purchase the property; if the 
        property is a station or utility, purchase the property; otherwise do not purchase the 
        property.

        Parameters
        ----------
        player: obj
            An instance of the class Player.
        space: obj
            An instance of one of the classes Street/Station/Utility.

        Returns
        -------
        bool
            True/False value for whether the player should purchase the property or not.
        """
        # TO DO: ADD OPTION TO MORTGAGE/SELL HOUSES TO PURCHASE A PROPERTY
        if player.money >= space.price:

            # buy the property if they already have one in that set OR if they have 2 or fewer properties in total
            if space.type == "Street":
                if len(player.property_sets[space.group]) > 0:
                    return True
                elif len(player.properties) < 3:
                    return True
                else:
                    return False
                
            elif space.type == "Station":
                return True
            elif space.type == "Utility":
                return True
            else:
                return False

        else:
            return False
        
    def decide_sell_houses(self, player, money_needed):
        """
        This method This method is responsible for determining which houses and hotels a player should sell in 
        order to generate the necessary funds to cover their financial requirements. It prioritises selling 
        houses and hotels from property groups that have the most houses and hotels. The method iterates through 
        the player's property sets and evaluates each property group, starting with the one that has the most 
        houses and hotels in descending order. It continues to sell houses and hotels until the required money 
        is raised or until there are no more properties with houses or hotels in that group. The loop then 
        proceeds to the next property group. Hotels are sold before houses.

        Parameters
        ----------
        player: obj
            An instance of the Player class.
        money_needed: int
            The amount of money that the player needs.

        Returns
        -------
        None
        """
        money_raised = 0

        # get property groups that player owns & sort by number of houses & hotels in group
        property_sets = [(group, properties) for group, properties in player.property_sets.items()]
        property_sets.sort(key=lambda x: sum(prop.num_houses + prop.hotel for prop in x[1]), reverse=True)

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
        This method determines which properties the player should mortgage to raise the required amount of 
        money. This method helps the player raise the necessary funds by mortgaging properties they own. 
        It considers all the player's properties, including streets, stations, and utilities, without any 
        buildings (houses or hotels), and sorts them by mortgage value in ascending order. This ensures that 
        the least valuable properties are mortgaged first, preserving the more valuable ones. The method 
        iterates through the sorted list of properties, checking if each property is already mortgaged. 
        If a property is not mortgaged, it calculates the mortgage value and mortgages the property, adding 
        the proceeds to the player's available funds. The process continues until enough money has been 
        raised to meet the target or all eligible properties have been mortgaged.

        Parameters
        ----------
        player: obj
            An instance of the Player class.
        money_needed: int
            The amount of money that the player needs.

        Returns
        -------
        None
        """
        # combine all of the player's properties (streets, stations, and utilities) without buildings
        undeveloped_streets = [prop for prop in player.properties if prop.num_houses == 0]
        all_properties = undeveloped_streets + player.stations + player.utilities

        # sort combined list of properties by mortgage value (least valuable first)
        all_properties.sort(key = lambda prop: prop.calculate_mortgage_value(), reverse=False)

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
        This method makes the decision as to whether or not a player should leave jail (given that
        they have a choice). If the player has a 'Get out of Jail free.' card, they use it and leave 
        jail. Next, if the player has enough money to pay to leave jail, they do so. Otherwise, 
        they must remain in jail.

        Parameters
        ----------
        player: obj
            An instance of the class Player.

        Returns
        -------
        bool
            True/False value that denotes whether or not the player should choose to leave jail.
        """
        # TO DO: ADD OPTION TO MORTGAGE/SELL HOUSES TO LEAVE JAIL
        if player.jail_cards > 0:
            player.jail_cards -= 1
            return True
        elif player.money >= 50:
            player.pay(50)
            return True
        else:
            return False
        
    def decide_unmortgage_properties(self, player):
        """
        This method decides whether properties should be unmortgaged. It first picks out all 
        properties that are currently mortgaged, then sorts these in ascending order of price
        (cheaper properties are unmortgaged first). If the player has enough money to unmortgage
        a property, they do so.

        Parameters
        ----------
        player: obj
            An instance of the Player class

        Returns
        -------
        None
        """
        # get all mortgaged properties and sort by price
        mortgaged_streets = [prop for prop in player.properties if prop.is_mortgaged]
        mortgaged_stations = [station for station in player.stations if station.is_mortgaged]
        mortgaged_utilities = [utility for utility in player.utilities if utility.is_mortgaged]
        mortgaged_properties = mortgaged_streets + mortgaged_stations + mortgaged_utilities 
        mortgaged_properties.sort(key = lambda x: x.price)

        for prop in mortgaged_properties:
            unmortgage_cost = prop.calculate_unmortgage_price()
            
            # if the player has enough money to unmortgage the property, they do
            if player.money >= unmortgage_cost:
                player.pay(unmortgage_cost)
                prop.is_mortgaged = False
            else:
                break
        

    def decide_build_on_properties(self, player, property_sets):
        """
        This method determines whether the player should build houses or hotels on their owned 
        property sets. It iterates through all property groups in the provided property_sets 
        dictionary and checks if the entire set is owned by the player. If the player owns all 
        the properties within a group, they have the opportunity to develop those properties.
        For each street in the property group, the method calls two helper methods: 
        decide_to_build_house and decide_to_build_hotel. If it's determined that the player should 
        build a house, the method deducts the cost from the player's money and increases the number 
        of houses and houses count for the property. If building a hotel is recommended, a hotel 
        is added to the property, and the hotel count for the player is incremented. 

        Parameters
        ----------
        player: obj
            An instance of the Player class.
        property_sets: dict
            A dictionary containing all property sets on the Monopoly board, regardless of
            their owners'.

        Returns
        -------
        None
        """
        # TO DO: ADD OPTION TO MORTGAGE/SELL HOUSES TO BUILD ON PROPERTIES
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
        This method evaluates whether the player should build a house on a given street property.
        The decision-making process involves the following criteria:
        1. Ensure that the property allows for additional houses (less than 4 houses currently built).
        2. Confirm that the player has enough money to cover the cost of a house (house price).
        3. Examine neighbouring properties within the same property group and verify that there is no 
            more than a one-house difference between them.
        If all these conditions are met, the player should purchase a house on the property.

        Parameters
        ----------
        player: obj
            An instance of the class Player.
        space: obj
            An instance of the class Street.

        Returns
        -------
        bool
            True/False value for whether the player should build a house or not.
        """
        if street.num_houses < 4 and player.money >= street.house_price:

            # get neighboring properties in the same set
            neighbouring_properties = [prop for prop in player.property_sets[street.group] if prop != street]

            # check if there is no greater than 1 house difference on neighboring properties
            for neighbour_property in neighbouring_properties:
                if abs(street.num_houses - neighbour_property.num_houses) > 1:
                    return False 

            return True 
        
        else:
            return False
        
    def decide_to_build_hotel(self, player, street):
        """
        This method evaluates whether the player should build a hotel on a given street property.
        The decision-making process involves the following criteria:
        1. Ensure that the property allows for a hotel (4 houses currently built).
        2. Confirm that the player has enough money to cover the cost of a hotel (same as the house price).
        3. Examine neighbouring properties within the same property group and verify that there is no 
            more than a one-house difference between them.
        If all these conditions are met, the player should purchase a hotel on the property.

        Parameters
        ----------
        player: obj
            An instance of the class Player.
        space: obj
            An instance of the class Street.

        Returns
        -------
        bool
            True/False value for whether the player should build a hotel or not.
        """
        if street.num_houses == 4 and not street.hotel and player.money >= street.house_price:

            # get neighboring properties in the same set
            neighbouring_properties = [prop for prop in player.property_sets[street.group] if prop != street]

            # check if there is no greater than 1 house difference on neighboring properties
            for neighbour_property in neighbouring_properties:
                if abs(street.num_houses + street.hotel - neighbour_property.num_houses - neighbour_property.hotel) > 1:
                    return False  

            return True 
        
        else:
            return False