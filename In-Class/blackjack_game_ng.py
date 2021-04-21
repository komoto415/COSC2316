# Dr Michaels
# blackjack_game.py
# 4/14/21
# This file contains information on a card and deck class.
# Together we will build a player class
# Then begin designing rules for a game

# Global variables used to create a new deck
face = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
suit = ["Clubs", "Diamonds", "Hearts", "Spades"]

import random

class Card:
    # Constructor method for Card.
    # Takes as input a face and suit value. 
    # If they are not found in the global variables above, the card will be set to a 2 of clubs
    def __init__(self, the_face, the_suit):
        global face, suit
        if (the_face in face and the_suit in suit):
            self.face = the_face
            self.suit = the_suit
        else:
            # print("Illegal card value, creating a 2 of Clubs")
            self.face = -1
            self.suit = "ILLEGAL CARD"

    # Retuns the suit value of the calling card
    def get_suit(self):
        return self.suit

    # Returns the face value of the calling card
    def get_face(self):
        return self.face

    # Compares the face and suit attributes of other_card to those possessed by the calling card
    def __eq__(self, other_card):
        return (self.face == other_card.get_face()) and (self.suit == other_card.get_suit())

    # Returns the value of self > other_card
    # The first comparison is on face value. If the faces are different, we return the result of
    # self.face > other_card.get_face()
    # If they are tied, we return the result of self.suit > other_card.get_suit()
    def __gt__(self, other_card):
        if self.face > other_card.get_face():
            return True
        elif (self.face == other_card.get_face()):
            return self.suit > other_card.get_suit()
        else:
            return False

    # Card tostring. Will return the card in the format "Face of Suit"
    def __str__(self):
        face_str = self.face
        if self.face == 11:
            face_str = "Jack"
        elif self.face == 12:
            face_str = "Queen"
        elif self.face == 13:
            face_str = "King"
        elif self.face == 14:
            face_str = "Ace"

        return f"{face_str} of {self.suit}"

class Deck:

    # The constructor method for the Deck.
    # It takes no parameters.
    # It fills a deck with 52 unique card, and then uses random.shuffle to randomly order the deck
    # The counter will be used to indicate which card is at the "top" of the deck
    # i.e. all cards above counter will have been dealt
    def __init__(self):
        self.deck = []
        self.counter = 0
        global face
        global suit
        for the_face in face:
            for the_suit in suit:
                self.deck.append(Card(the_face, the_suit))
        for i in range(7):
            random.shuffle(self.deck)

    # Returns the top card of the deck if it exists (if we have not previously dealt 52 cards)
    # We could add in a method to automatically shuffle the deck if we reach this point
    def deal(self):
        if self.counter < 52:
            result = self.deck[self.counter]
            self.counter += 1
            return result

    # Randomly shuffles the deck array seven times.
    def shuffle(self):
        self.counter = 0
        for i in range(7):
            random.shuffle(self.deck)

    # tostring method for deck class.
    # Prints out all 52 cards in the deck, one per line.
    # We indicate with an X cards that have been dealt
    # << Current Top Card indicates which card is the current top of the deck.
    def __str__(self):
        result = ""
        for i in range(52):
            if i == self.counter:
                result += "%s << Current Top Card\n" % self.deck[i]
            elif i < self.counter:
                result += "%s X\n" % self.deck[i]
            else:
                result += "%s\n" % self.deck[i]
        return result

class Blackjack_Player:

    def __init__(self):
        self.hand = []

    def first_card(self):
        if (len(self.hand) > 0):
            return self.hand[0]
        else:
            return "Game not started"

    def add_card(self, card):
        self.hand.append(card)

    def get_hand(self):
        return self.hand

    @staticmethod
    def calc_score(hand):
        score = 0
        for card in hand:
            if card.get_face() > 9:
                add_me = 10
                if card.get_face() == 14:
                    print("Current hand: ", end="")
                    [print(card, end=" ") for card in hand]
                    print()
                    while True:
                        print("Would you like your Ace to be an 11 or 1? ", end="")
                        try:
                            add_me = int(input("").strip())
                            if add_me != 11 and add_me != 1:
                                print("The only valid values are 11 or 1. Please try again")
                                continue
                            break
                        except ValueError as _:
                            print("You have to put an integer value. Please try again")
                score += add_me
            else:
                score += card.get_face()

        return score

    def __str__(self):
        # Change the tostring to include the value calculation!
        if (len(self.hand) == 0):
            return "No cards in hand"
        else:
            result = "%s" % self.hand[0]
            for i in range(1, len(self.hand)):
                result += ", %s" % self.hand[i]
            score = self.calc_score(self.hand)
            result = f"{result}\nHand Score: {score}"
            return result

class Blackjack_Game:

    def __init__(self):
        self.player = Blackjack_Player()
        self.dealer = Blackjack_Player()
        self.Deck = Deck()

    def play_game(self):
        game_done = False
        for _ in range(2):
            self.player.add_card(self.Deck.deal())
            self.dealer.add_card(self.Deck.deal())

        while (not game_done):
            print("This is your current hand: %s" % self.player)
            print("This is what you see of the dealer: %s" % self.dealer.first_card())
            val = input("Do you want to get another card? (Y/N)")
            if (val == "Y" or val == "y"):
                # Deal another card to the player here
                self.player.add_card(self.Deck.deal())
                print(f"You current hand:\n{self.player}")
                if self.player.calc_score(self.player.get_hand()) > 21:
                    print("You have busted. Better luck next time")
                    return False
            else:
                game_done = True

        player_score = self.player.calc_score(self.player.get_hand())
        dealer_score = self.dealer.calc_score(self.dealer.get_hand())
        print(f"Dealer's Current Hand:\n{self.dealer}")
        while dealer_score < 17 and player_score <= 21:
            self.dealer.add_card(self.Deck.deal())
            dealer_score = self.dealer.calc_score(self.dealer.get_hand())
            print(f"Dealer's Current Hand:\n{self.dealer}")
            if dealer_score > 21:
                print("Player wins because dealer busted")
                return True

        print("\n" * 4)
        # Present player score and then play the dealer and decide who wins
        print(f"Your current hand:\n{self.player}")
        print(f"Dealer's Current Hand:\n{self.dealer}")
        if player_score > dealer_score:
            print("Player wins because they're hand is greater")
            return True
        else:
            print("Dealer wins because they're hand is greater")
            return False

    def __str__(self):
        return "Nothing to see here!"

def gameplay_loop(x):
    player_wins = 0
    dealer_wins = 0
    for _ in range(x):
        blackjack_game = Blackjack_Game()
        if blackjack_game.play_game():
            player_wins += 1
        else:
            dealer_wins += 1

    print(f"Player has won {player_wins} time{'' if player_wins == 1 else 's'}")
    print(f"Dealer has won {dealer_wins} time{'' if dealer_wins == 1 else 's'}")

def main():
    print("This will be our blackjack simulator!")
    my_game = Blackjack_Game()
    print("Let us test the game!")
    my_game.play_game()
    #
    # Test players
    # player = Blackjack_Player()
    # hand = [Card(3, "Clubs"), Card(3, "Spades"), ]
    # for card in hand:
    #     player.add_card(card)
    # print(player)

main()
