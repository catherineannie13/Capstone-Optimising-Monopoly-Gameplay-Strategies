class Street:
    """
    This class represents a street property in a Monopoly game. It includes attributes to 
    track the property's name, price, house price, rent, number of houses, hotel status, 
    location, property group, number in the group, owner, and mortgage status.

    Attributes
    ----------
    name: str
        The name of the street property.
    price: float
        The purchase price of the property.
    house_price: float
        The price to build a house on the property.
    type: str
        The type of property (set to 'Street').
    rent: int
        The base rent of the property.
    double_rent: int
        The double rent if the owner owns the entire group.
    house_rent: lst
        A list of rents based on the number of houses (1-4).
    hotel_rent: int
        The rent when a hotel is built on the property.
    num_houses: int
        The number of houses built on the property.
    hotel: bool
        A flag indicating whether a hotel is built on the property.
    loc: int
        The position of the property on the Monopoly board.
    group: str
        The group to which the property belongs.
    num_in_group: int
        The number of properties in the group.
    owner: Player
        The player who currently owns the property.
    is_mortgaged: bool
        A flag indicating whether the property is mortgaged.

    Methods
    -------
    __init__(name, price, house_price, rent, one_house, two_houses, three_houses, four_houses, 
    hotel, loc, group, num_in_group)
        Initialises the attributes of the street property.
    __repr__()
        Provides a string representation of the street property, including relevant attributes.
    __lt__(other)
        Compares two properties based on their locations on the Monopoly board.
    calculate_rent()
        Calculates the amount of rent that must be paid on this street property.
    calculate_mortgage_value()
        Calculates the mortgage value of the property.
    calculate_house_sale_value()
        Calculates the house sale value on this property.
    calculate_unmortgage_price()
        Calculates the cost of unmortgaging this property.
    """

    def __init__(self, name, price, house_price, rent, one_house, two_houses, three_houses, four_houses, hotel, loc, group, num_in_group):
        self.name = name
        self.price = price
        self.house_price = house_price
        self.type = "Street"
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
        self.is_mortgaged = False

    def __repr__(self):
        """
        This method provides a string representation of the Street class, including all
        relevant attributes. This ensures that a printed street object displays something
        that is interpretable (printed string).
        
        Parameters
        ----------
        None

        Returns
        -------
        str
            String representation of class.
        """
        return f'{self.name} is one of the {self.num_in_group} properties in the {self.group} set located at position {self.loc} on the Monopoly board \
                \n and can be purchased for ${self.price} with a house price of ${self.house_price}. Rent prices are as follows: \n Rent: {self.rent} \n Double rent: {self.double_rent} \
                \n Rent 1 house: {self.house_rent[0]} \n Rent 2 houses: {self.house_rent[1]} \n Rent 3 houses: {self.house_rent[2]} \n Rent 4 houses: {self.house_rent[3]} \
                \n Rent hotel: {self.hotel_rent} \n The property is currently owned by {self.owner.name if self.owner else "no-one"} and has {self.num_houses} houses and {1 if self.hotel else 0} hotels.'

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
    
    def calculate_rent(self):
        """
        Calculates the amount of rent that must be paid on this street. If there is no 
        owner, no rent needs to be paid. Otherwise, if the street property
        is mortgaged, no rent needs to be paid. If the owner owns the entire group of 
        properties, double rent must be paid. If the property has houses/hotels built on it,
        the corresponding rent must be paid to the number of houses/hotels.

        Parameters
        ----------
        None

        Returns
        -------
        int
            The rent that must be paid on the property to the owner.
        """
        if self.owner:

            # player can't collect rent when mortgaged
            if self.is_mortgaged:
                return 0

            elif self.num_houses == 0:

                # double rent if the owner owns the entire group
                if len(self.owner.property_sets[self.group]) == self.num_in_group:
                    return self.double_rent
                else:
                    return self.rent
                
            # hotel rent if hotel on property
            elif self.hotel:
                return self.hotel_rent
            
            # corresponding rent according to the number of owned houses
            else:
                return self.house_rent[self.num_houses - 1]
        else:
            return 0
    
    def calculate_mortgage_value(self):
        """
        This method calculates the mortgage value of the property.

        Parameters
        ----------
        None

        Returns
        -------
        float
            The mortgage price of the property.
        """
        return self.price/2

    def calculate_house_sale_value(self):
        """
        This method calculates the house sale value on this property.

        Parameters
        ----------
        None

        Returns
        -------
        float
            The house sale value of the property.
        """
        return self.house_price/2
    
    def calculate_unmortgage_price(self):
        """
        This method calculates the cost of unmortgaging this property, 
        given that it is mortgaged to begin with.

        Parameters
        ----------
        None

        Returns
        -------
        float
            The price to unmortgage this property.
        """
        return (self.price/2)*1.1