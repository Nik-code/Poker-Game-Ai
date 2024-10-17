# card.py

class Card:
    """
    Represents a single playing card.
    """
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
             'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, suit, rank):
        self.suit = suit  # Hearts, Diamonds, Clubs, Spades
        self.rank = rank  # 2-10, Jack, Queen, King, Ace

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def get_value(self):
        """
        Returns the numerical value of the card for comparison.
        """
        return self.RANKS.index(self.rank)
