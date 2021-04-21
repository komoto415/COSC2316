from card import *

def shuffle(stuff):
    import random
    for _ in range(5):
        random.shuffle(stuff)

class Deck:
    def __init__(self):
        self.__deck = []
        faces = range(2, 15)
        suits = [Card.Suit.Diamonds, Card.Suit.Clubs, Card.Suit.Hearts, Card.Suit.Spades]
        for suit in suits:
            for face in faces:
                self.__deck.append(Card(face=face, suit=suit))

        assert len(self.__deck) == 52

        shuffle(self.__deck)

    @property
    def deck(self):
        return self.__deck

    def deal(self):
        try:
            return self.__deck.pop()
        except IndexError as _:
            print("The deck is currently empty")
            raise

    def __str__(self):
        deck_str = ""
        for card in self.deck:
            deck_str += str(card) + '\n'

        return deck_str.strip()
