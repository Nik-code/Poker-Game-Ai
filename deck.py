# deck.py

import random
from card import Card

class Deck:
    """
    Represents a standard deck of 52 playing cards.
    """

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    def shuffle(self):
        """
        Shuffles the deck.
        """
        random.shuffle(self.cards)

    def deal(self, num):
        """
        Deals 'num' cards from the deck.
        """
        dealt_cards = self.cards[:num]
        self.cards = self.cards[num:]
        return dealt_cards
