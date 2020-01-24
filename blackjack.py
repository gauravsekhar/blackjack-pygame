"""

CMPUT 275 Winter 2018 - Final Project: blackjack

This is a version of the classic casino card game blackgack. The game features
betting, hitting, standing, and doubling. The player plays against a computer
player dealer. The game ends when the player's coffer is empty and the player
can no longer bet. See README for more details and rules.
"""

import pygame
import os
import sys
import deck
from game import *
from pygame.locals import *

card_deck = deck.Deck()     # initialize card deck
stats = GameStats()         # game stats
const = Pixels()            # graphical constants
user_coffer = 1000          # user money


# load and return an image in a specified directory within the working directory
def image_load(filename, dir, scale_x=None, scale_y=None):
    path = os.path.join("images", dir, filename)
    image = pygame.image.load(path)

    # if needed, scale the image
    if scale_x is not None and scale_y is not None:
        image = pygame.transform.scale(image, (scale_x, scale_y))
    return image


# print text to screen after clearing existing text in that spot
def disp_text(text, x, y, isbold=False, size=30, colour=(255, 203, 14)):
    pygame.draw.rect(screen, (0, 100, 0), (x, y, 300, size))
    font = pygame.font.SysFont("Tahoma", size)
    font.set_bold(isbold)

    text = font.render(text, True, colour)
    screen.blit(text, (x, y))


# reset stats and deck
def new_round():
    global stats
    global card_deck
    stats = GameStats()         # reset all stats
    card_deck = deck.Deck()     # initalize a complete, ordered deck
    disp_text("Current bet: $0".format(stats.bet), const.valtext_x, const.valtext_y, False, 20)
    disp_text("Coffer: ${}".format(user_coffer), const.valtext_x, const.valtext_y+30, False, 20)
    print("user: {}".format(user_coffer))


# pop and return a card from the deck
def get_card(deck):
    card = deck.cards.pop(len(deck.cards) - 1)
    return card


# deal a card from the deck and display it at given coordinates
def draw_card(player, x, y):
    draw_card = get_card(card_deck)
    card_image = image_load(draw_card.image, "cards", const.card_w, const.card_h)
    screen.blit(card_image, (x, y))

    # if an ace is dealt, keep track of how many aces are in the hand
    if draw_card.points == 11:
        if player == "user":
            stats.user_aces += 1
        elif player == "dealer":
            stats.dealer_aces += 1
    return draw_card


# deal the first two cards of the user's hand, update the user's score based
# on the two cards, and track the number of cards in the user's hand
def user_hand():
    stats.user_score += draw_card("user", const.card_x, const.usercard_y).points
    stats.user_score += draw_card("user", const.card_x+const.card_w+20, const.usercard_y).points
    stats.user_cards = 2


# deal the first two cards of the dealer's hand, update the dealer's score based
# on the two cards, and track the number of cards in the dealer's hand
def dealer_hand():
    stats.dealer_score += draw_card("dealer", const.card_x, const.dealercard_y).points
    # store the dealer's second card so that it can be covered and revealed later
    stats.dealer_hidden = draw_card("dealer", const.card_x+const.card_w+20, const.dealercard_y)
    stats.dealer_score += stats.dealer_hidden.points
    stats.dealer_cards = 2

    # cover the dealer's second card
    cover = image_load("back.png", "cards", const.card_w, const.card_h)
    screen.blit(cover, (const.card_x+const.card_w+20, const.dealercard_y))


# reveal the dealer's second card
def flip():
    hidden = image_load(stats.dealer_hidden.image, "cards", const.card_w, const.card_h)
    screen.blit(hidden, (const.card_x+const.card_w+20, const.dealercard_y))


# update the coffer
def user_win(blackjack=False):
    global user_coffer
    # if the user has a blackjack, the user receives triple the bet
    if blackjack:
        user_coffer += 3*stats.bet
        disp_text("Coffer: ${}".format(user_coffer), const.valtext_x, const.valtext_y+30, False, 20)
    # on a regular win, the user receives double the bet
    else:
        user_coffer += 2*stats.bet
        disp_text("Coffer: ${}".format(user_coffer), const.valtext_x, const.valtext_y+30, False, 20)

    print("dealer score: {}, user score: {}".format(stats.dealer_score, stats.user_score))
    new_round()


# the case of a tie between user and dealer
def push():
    global user_coffer
    user_coffer += stats.bet    # return the bet back to the coffer
    disp_text("Coffer: ${}".format(user_coffer), const.valtext_x, const.valtext_y+30, False, 20)


# user is dealt a card
def user_turn():
    stats.user_score += draw_card("user", 20+(stats.user_cards*(const.card_w+20)), const.usercard_y).points
    stats.user_cards += 1
    if stats.user_score > 21:
        # if the user busts but has aces, change the value of the aces from 11
        # to 1 so that the user can keep playing
        if stats.user_aces:
            stats.user_score -= stats.user_aces*10
            stats.user_aces = 0
        else:
            flip()
            disp_text("You bust!", const.midtext_x, const.midtext_y, True)
            print("You bust")
            new_round()


# dealer behaviour
def dealer_turn():

    flip()      # uncover dealer's second card

    # if the dealer has a blackjack
    if stats.dealer_score == 21:
        disp_text("Dealer blackjack!", const.midtext_x, const.midtext_y, True)
        print("Dealer blackjack")
        new_round()
    else:
        # keep drawing cards until the dealer has a score of at least 16
        while stats.dealer_score < 16:
            stats.dealer_score += draw_card("dealer", 20+(stats.dealer_cards*(const.card_w+20)), const.dealercard_y).points
            stats.dealer_cards += 1

        # the dealer can only see the first two cards of the user's hands,
        # so if the dealer is above 16 but below the visible user score,
        # the dealer wants to keep hitting for a chance to win
        if stats.user_cards == 2 and stats.user_score > stats.dealer_score:
            stats.dealer_score += draw_card("dealer", 20+(stats.dealer_cards*(const.card_w+20)), const.dealercard_y).points
            stats.dealer_cards += 1

        while stats.dealer_score > 21:
            # if dealer went bust and has aces, change value of aces from 11 to
            # 1 so that the dealer can stay in the game
            if stats.dealer_aces:
                stats.dealer_score -= stats.dealer_aces*10
                stats.dealer_aces = 0
                # draw cards till hand has a value of atleast 16
                while stats.dealer_score < 16:
                    stats.dealer_score += draw_card("dealer", 20+(stats.dealer_cards*(const.card_w+20)), const.dealercard_y).points
                    stats.dealer_cards += 1
            # if dealer went bust and has no aces
            else:
                disp_text("Dealer bust!", const.midtext_x, const.midtext_y, True)
                print("Dealer bust")
                user_win()
                break


# if both dealer and user didn't bust, compare hands
def compare_scores():
    # user's hand is more than dealer's hand -> user win
    if stats.user_score > stats.dealer_score:
        disp_text("User wins!", const.midtext_x, const.midtext_y, True)
        print("User wins")
        user_win()
    # dealer's hand is more than user's hand -> dealer win
    elif stats.user_score < stats.dealer_score:
        disp_text("Dealer wins!", const.midtext_x, const.midtext_y, True)
        print("Dealer wins")
        new_round()
    elif stats.user_score == stats.dealer_score:    # hands are equal -> push
        disp_text("Push!", const.midtext_x, const.midtext_y, True)
        push()
        new_round()


# to check if user has blackjack
def check_user_blackjack():
    if stats.user_score == 21:
        flip()          # uncover dealer's second card to compare
        if stats.dealer_score == 21:        # if dealer also has blackjack
            disp_text("Push!", const.midtext_x, const.midtext_y)
            push()
            new_round()
        else:
            disp_text("User blackjack!", const.midtext_x, const.midtext_y, True)
            print("User blackjack")
            user_win(True)


# displays "inactive" buttons
def init_graphics():
    grey = image_load("greybutton.png", "buttons", const.button_w, const.button_h)

    # deal/hit, stand, double buttons
    screen.blit(grey, (const.move_x, const.move_y))
    screen.blit(grey, (const.move_x+70, const.move_y))
    screen.blit(grey, (const.move_x+140, const.move_y))
    pygame.draw.rect(screen, (0, 100, 0), (const.move_x, const.move_y+55, 300, 30))

    # betting buttons
    screen.blit(grey, (const.bet_x, const.bet_y))
    screen.blit(grey, (const.bet_x+100, const.bet_y))
    screen.blit(grey, (const.bet_x+200, const.bet_y))

    two_fifty = image_load("250.png", "text")
    one_hundred = image_load("100.png", "text")
    fifty = image_load("50.png", "text")

    # text for values of each betting button
    screen.blit(two_fifty, (const.bet_x, const.bet_y+40))
    screen.blit(one_hundred, (const.bet_x+100, const.bet_y+40))
    screen.blit(fifty, (const.bet_x+200, const.bet_y+40))


# constantly detecting button selection based on mouse position/click state
def check_button(x, y, buttontype, range):
    mouse = pygame.mouse.get_pos()          # get position of mouse
    click = pygame.mouse.get_pressed()      # get mouse button state
    global user_coffer

    if buttontype == "deal":
        if x < mouse[0] < x + range and y < mouse[1] < y + range:
            # green upon hovering over button
            green = image_load("greenbutton.png", "buttons", const.button_w, const.button_h)
            screen.blit(green, (const.move_x, const.move_y))
            deal = image_load("deal.png", "text")   # display text on hover
            screen.blit(deal, (const.move_x, const.move_y+55))

            if click[0] == 1:
                # blue upon clicking
                pygame.draw.rect(screen, (0, 100, 0), (0, 0, 650, 430))
                init_graphics()
                blue = image_load("bluebutton.png", "buttons", const.button_w, const.button_h)
                screen.blit(blue, (const.move_x, const.move_y))
                card_deck.shuffle()     # shuffle deck before dealing
                user_hand()             # deal user hand
                dealer_hand()           # deal dealer hand
                stats.in_round = True   # now the round has begun

                check_user_blackjack()  # check for user blackjack instantly

    elif buttontype == "hit":
        if x < mouse[0] < x + range and y - range < mouse[1] < y + range:
            # green upon hovering over button
            green = image_load("greenbutton.png", "buttons", const.button_w, const.button_h)
            screen.blit(green, (const.move_x, const.move_y))
            hit = image_load("hit.png", "text")     # display text on hover
            screen.blit(hit, (const.move_x, const.move_y+55))

            if click[0] == 1:
                # blue upon clicking
                blue = image_load("bluebutton.png", "buttons", const.button_w, const.button_h)
                screen.blit(blue, (const.move_x, const.move_y))
                user_turn()         # draw card and update user_score

    elif buttontype == "stand":
        if x < mouse[0] < x + range and y < mouse[1] < y + range:
            # green upon hovering over button
            green = image_load("greenbutton.png", "buttons", const.button_w, const.button_h)
            screen.blit(green, (const.move_x+70, const.move_y))
            stand = image_load("stand.png", "text")     # display text on hover
            screen.blit(stand, (const.move_x+70, const.move_y+55))

            if click[0] == 1:
                # blue upon clicking
                blue = image_load("bluebutton.png", "buttons", const.button_w, const.button_h)
                screen.blit(blue, (const.move_x, const.move_y))
                dealer_turn()       # user turn over, dealer's turn now
                if stats.in_round == 1:
                    compare_scores()        # if user and dealer didn't bust

    elif buttontype == "double":
        if x < mouse[0] < x + range and y < mouse[1] < y + range:
            # green upon hovering over button
            green = image_load("greenbutton.png", "buttons", const.button_w, const.button_h)
            screen.blit(green, (const.move_x+140, const.move_y))
            double = image_load("double.png", "text")   # display text on hover
            screen.blit(double, (const.move_x+140, const.move_y+55))

            # double is only possible if coffer has enough money to double bet
            if click[0] == 1 and user_coffer >= stats.bet:
                # blue upon clicking
                blue = image_load("bluebutton.png", "buttons", const.button_w, const.button_h)
                screen.blit(blue, (const.move_x+140, const.move_y))
                user_coffer -= stats.bet
                stats.bet *= 2  # doubling the bet
                user_turn()     # 1 card drawn when bet is doubled

                if stats.in_round:      # if user didn't bust
                    dealer_turn()

                if stats.in_round:      # if dealer didn't bust
                    compare_scores()

    elif buttontype == "250":
        if x < mouse[0] < x + range and y < mouse[1] < y + range:
            green = image_load("greenbutton.png", "buttons", const.button_w, const.button_h)
            screen.blit(green, (const.bet_x, const.bet_y))

            if click[0] == 1 and user_coffer >= 250:
                blue = image_load("bluebutton.png", "buttons", const.button_w, const.button_h)
                screen.blit(blue, (const.bet_x, const.bet_y))
                stats.bet += 250        # increase bet and decrease coffer
                user_coffer -= 250
                disp_text("Current bet: ${}".format(stats.bet), const.valtext_x, const.valtext_y, False, 20)
                disp_text("Coffer: ${}".format(user_coffer), const.valtext_x, const.valtext_y+30, False, 20)

    elif buttontype == "100":
        if x < mouse[0] < x + range and y < mouse[1] < y + range:
            green = image_load("greenbutton.png", "buttons", const.button_w, const.button_h)
            screen.blit(green, (const.bet_x+100, const.bet_y))

            if click[0] == 1 and user_coffer >= 100:
                blue = image_load("bluebutton.png", "buttons", const.button_w, const.button_h)
                screen.blit(blue, (const.bet_x+100, const.bet_y))
                stats.bet += 100        # increase bet and decrease coffer
                user_coffer -= 100
                disp_text("Current bet: ${}".format(stats.bet), const.valtext_x, const.valtext_y, False, 20)
                disp_text("Coffer: ${}".format(user_coffer), const.valtext_x, const.valtext_y+30, False, 20)

    elif buttontype == "50":
        if x < mouse[0] < x + range and y < mouse[1] < y + range:
            green = image_load("greenbutton.png", "buttons", const.button_w, const.button_h)
            screen.blit(green, (const.bet_x+200, const.bet_y))

            if click[0] == 1 and user_coffer >= 50:
                blue = image_load("bluebutton.png", "buttons", const.button_w, const.button_h)
                screen.blit(blue, (const.bet_x+200, const.bet_y))
                stats.bet += 50         # increase bet and decrease coffer
                user_coffer -= 50
                disp_text("Current bet: ${}".format(stats.bet), const.valtext_x, const.valtext_y, False, 20)
                disp_text("Coffer: ${}".format(user_coffer), const.valtext_x, const.valtext_y+30, False, 20)


if __name__ == "__main__":
    pygame.init()   # starts pygame window
    pygame.font.init()  # for printing text
    screen = pygame.display.set_mode((800, 550))    # window size
    pygame.display.set_caption('Blackjack')     # window caption
    screen.fill((0, 100, 0))            # background colour
    disp_text("Current bet: $0", const.valtext_x, const.valtext_y, False, 20)
    disp_text("Coffer: $1000", const.valtext_x, const.valtext_y+30, False, 20)

    while True:     # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:      # if close window is clicked, quit
                pygame.quit()
                sys.exit()

            init_graphics()     # draw initial buttons and text

            # check buttons relating to moves
            if stats.in_round:
                check_button(const.move_x, const.move_y, "hit", const.button_h)
                check_button(const.move_x+70, const.move_y, "stand", const.button_h)
                check_button(const.move_x+140, const.move_y, "double", const.button_h)

            # check buttons relating to bet and deal (but only if a bet has
            # been made)
            else:
                check_button(const.bet_x, const.bet_y, "250", const.button_h)
                check_button(const.bet_x+100, const.bet_y, "100", const.button_h)
                check_button(const.bet_x+200, const.bet_y, "50", const.button_h)

                # if coffer is empty can't deal->game over
                if stats.bet != 0 and user_coffer >= 0:
                    check_button(const.move_x, const.move_y, "deal", const.button_h)

            pygame.display.update()     # update all events
