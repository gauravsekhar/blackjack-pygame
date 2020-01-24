"""
These are the implementations of classes related to gameplay and graphics.
"""

# an instance of GameStats has attributes for values that need to be recorded
# or kept track of, and that will be reset each round
class GameStats:
    def __init__(self):
        self.in_round = False   # False if betting, True after dealing
        self.bet = 0    # stores bet of the round

        self.user_cards = 0     # number of cards in user's hand
        self.dealer_cards = 0   # number of cards in dealer's hand

        self.user_score = 0     # value of user's hand
        self.dealer_score = 0   # value of dealer's hand

        self.user_aces = 0      # number of aces in user's hand
        self.dealer_aces = 0    # number of aces in dealer's hand

        # stores the dealer's second card so that it can be reprinted
        # (uncovered) after the user's turn
        self.dealer_hidden = None


# an instance of this class has attributes for constants related to the size
# and position of graphics to be displayed
class Pixels:
    def __init__(self):
        self.valtext_x = 350    # x position of coffer/bet text
        self.valtext_y = 450    # y position of coffer/bet text

        self.card_h = 145       # heigh of card
        self.card_w = 100       # width of card
        self.card_x = 20        # x position of first card in each hand
        self.usercard_y = 285   # y position of cards in user hand
        self.dealercard_y = 20  # y position of cards in dealer hand

        self.midtext_x = 50     # x position of text that says who won
        self.midtext_y = 210    # y position of text that says who won

        self.move_x = 560       # x position of deal/hit button
        self.move_y = 200       # y position of deal/hit, stand, double buttons

        self.bet_x = 50         # x position of first bet button
        self.bet_y = 450        # y position of bet buttons

        self.button_w = 51      # button width
        self.button_h = 49      # button height
