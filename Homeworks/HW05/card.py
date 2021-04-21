import enum

class Card:
    class Suit(enum.IntEnum):
        Diamonds = 0,
        Clubs = 1,
        Hearts = 2,
        Spades = 3

        def symbol(self):
            if self.value == 0:
                return "D"
            if self.value == 1:
                return "C"
            if self.value == 2:
                return "H"
            if self.value == 3:
                return "S"

    def __init__(self, face, suit):
        assert 2 <= face <= 14
        self.__face = face
        self.__suit = suit

    @property
    def face(self):
        return self.__face

    @property
    def suit(self):
        return self.__suit

    def __gt__(self, other):
        if self.face > other.face:
            return True
        elif self.face == other.face:
            return self.suit > other.suit
        else:
            return False

    def __eq__(self, other):
        return self.face == other.face and self.suit == other.face

    def __repr__(self):
        return f"Card({self.face}, {self.Suit})"

    def __str__(self):
        face_str = self.face
        if self.face == 11:
            face_str = "J"
        elif self.face == 12:
            face_str = "Q"
        elif self.face == 13:
            face_str = "K"
        elif self.face == 14:
            face_str = "A"

        return f"{face_str}{self.suit.symbol()}"