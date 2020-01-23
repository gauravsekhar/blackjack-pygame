"""
These are the implementations of classes related to the cards and deck.
"""

import random
import os

# card class that has attributes for rank, suit, and the image associated with
# the card
class Card:
    # possible suits
    suits = {1: "Hearts", 2: "Diamonds", 3: "Clubs", 4: "Spades"}
    # possible ranks
    values = {
        1: "Ace", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
        7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen",
        13: "King"
        }

    # create an instance of a card by specifying the key associated with a suit
    # and rank
    def __init__(self, value, suit):
        self.value = self.values[value]
        self.suit = self.suits[suit]
        # image file corresponding to specified suit and rank
        self.image = os.path.join("{}{}.png".format(self.value, self.suit))

        # aces have an initial in-game value of 11
        if value == 1:
            self.points = 11
        # face cards have an in-game value of 10, other cards except ace have
        # the same value as their rank
        else:
            self.points = value if value <= 10 else 10


# deck class that has a shuffle function and an attribute that is a list of
# card objects
class Deck:
    def __init__(self):
        self.cards = []     # cards in the deck

        # initially deck is ordered
        for i in range(1, 14):
            self.cards.append(Card(i, 1))
            self.cards.append(Card(i, 2))
            self.cards.append(Card(i, 3))
            self.cards.append(Card(i, 4))

    # implementation of Fisher-Yates shuffle algorithm. random.shuffle uses this,
    # but we wanted to implement it ourselves!
    def shuffle(self):
        # Fisher-Yates shuffle algorithm
        for i in range(51, 0, -1):
            j = random.randint(0, i)
            # print(i, j)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
