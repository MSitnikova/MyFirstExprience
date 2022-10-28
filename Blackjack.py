# Mini-project #6 - Blackjack

import simpleguitk as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print
            "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        string = "Hand has"
        for i in self.hand:
            string += " " + str(i)
        return string

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        Ace = False
        hand_value = 0
        for card in self.hand:
            rank = card.get_rank()
            hand_value += VALUES[rank]
            if rank == "A":
                Ace = True
        if Ace:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
        else:
            return hand_value

    def draw(self, canvas, pos):
        for card in self.hand:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]


# define deck class
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        string = "Deck contains "
        for i in self.deck:
            string += " " + str(i)
        return string


# define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, score
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    if in_play:
        score -= 1

    in_play = True
    outcome = "Hit or stand?"


def hit():
    # replace with your code below
    global in_play, outcome, score, player, deck, card
    if in_play:
        outcome = "Hit or stand?"
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            outcome = "You have busted. New deal?"
            in_play = False
            score -= 1


def stand():
    # replace with your code below
    global in_play, dealer, player, outcome, deck, score
    if in_play:
        if dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            outcome = "The dealer has busted. New deal?"
            score += 1
            in_play = False
        elif player.get_value() <= dealer.get_value():
            outcome = "The dealer wins. New deal?"
            score -= 1
            in_play = False
        else:
            outcome = "The player wins. New deal?"
            score += 1
            in_play = False


# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, in_play, dealer, player, score
    canvas.draw_text(outcome, (20, 300), 25, "Red")

    dealer_pos = [10, 145]
    player_pos = [10, 380]
    if in_play:
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0], CARD_CENTER[1] + CARD_SIZE[1])
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [dealer_pos[0] + CARD_CENTER[0],
                                                              dealer_pos[1] + CARD_CENTER[1]], CARD_SIZE)
    else:
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0], CARD_CENTER[1] + CARD_SIZE[1])

        canvas.draw_image(card_images, card_loc, CARD_SIZE, [dealer_pos[0] + CARD_CENTER[0],
                                                             dealer_pos[1] + CARD_CENTER[1]], CARD_SIZE)
        canvas.draw_image(card_images, CARD_CENTER, CARD_SIZE, [player_pos[0] + CARD_CENTER[0],
                                                                player_pos[1] + CARD_CENTER[1]], CARD_SIZE)
    canvas.draw_text("Dealer", (20, 120), 35, "Blue")
    canvas.draw_text("Player", (30, 370), 35, "Blue")
    player.draw(canvas, [player_pos[0], player_pos[1]])
    player.draw(canvas, [player_pos[0] + CARD_SIZE[0], player_pos[1]])
    dealer.draw(canvas, [dealer_pos[0] + CARD_SIZE[0], dealer_pos[1]])
    canvas.draw_text("Blackjack", (200, 50), 40, "Black")

    canvas.draw_text("Score: " + str(score), (400, 120), 20, "Red")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Pink")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric