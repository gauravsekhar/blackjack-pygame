# blackjack-pygame
Blackjack, or Twenty-One, using pygame.

## Introduction:
This project was aimed at the implementation of the popular casino card game
**Blackjack**.

The game is played on an individual table consisting of just 1 player (the user)
and 1 dealer (the computer). The user is given a starting coffer of $1000 to
beat the dealer in the several rounds.
While the game seems rather straight forward to play, the game logic required
great attention due to the several situations that can occur during the game.
On testing, bugs and rare instances were fixed to implement the game to
perfection.

## Game Description:

### Rules:
The aim of a round of blackjack is to achieve a hand value as close to 21
without going over. Each card in the deck has a value of 1-11.
- 2 - 10 have values equivalent to their face values
- Face cards (J, Q, K) have values of 10
- Ace can have a value of 11 or 1, depending upon the hand

The best hand in a round of blackjack is 'Blackjack'. Blackjack is obtained
if and only if the value of the initial 2-card hand is exactly 21.

The user is able to see the first card of the dealer while the dealer is able
to see the first 2 cards of the user and base his moves on the initial value
of the user's hand.

### Moves:
Hit: Draw a new card to increase value of hand  
Stand: Stay at your current hand, causing the dealer to play his turn  
Double: Draw 1 card while doubling your bet, allowing dealer to play his turn  

### Money Conditions:
The user is only permitted to play if he places a bet. A win pays 2 to 1,
blackjack pays 3 to 1, push returns your bet. If the user empties his coffer,
the game is over since the user cannot deal unless a bet is made. The user is
also permitted to double only if his coffer contains enough money to double his
bet.

### Further Description:
The Ace is given a default value of 11, and while the current value of the hand
is below 21, the value of the ace stays at 11. However, upon going over 21, the
value of the ace is changed to 1, to reduce the value of the hand to below 21 to
prevent an instant loss, giving the user another chance to hit/stand.

When the user is done playing his turn, the dealer decides to hit/stand based
on the current value of his hand and the value of the user's first 2 cards.
The dealer can only see the user's first hand (rules of blackjack)
If the value of the dealer's hand is below 16, the dealer hits. Else, he stands.
However, if the value of the dealer is greater than 16 but still lower than
the value of the user's first 2 cards, the dealer hits for a chance to beat
the user in the round.

## References:
1. Card faces from:  
  - https://opengameart.org/content/playing-cards-vector-png
2. Buttons from:  
  - http://images.all-free-download.com/
3. Card back image from:  
  - https://i.pinimg.com/
