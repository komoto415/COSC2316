class Player:
    def __init__(self, name="Player", player_id=0):
        self.__hand = []
        self.__id = player_id
        self.__name = name

    @property
    def hand(self):
        return self.__hand

    @property
    def player_id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    def hand_as_faces(self):
        return [card.face_str() for card in self.hand]

    def add_card(self, card):
        self.hand.append(card)

    def __eq__(self, other):
        return self.hand == other.hand and self.player_id == other.player_id and self.name == other.name

    def __str__(self):
        hand = f"Player: {self.name} with ID: {self.player_id}\nHand: ["
        for card in self.hand:
            hand += str(card) + ", "

        return hand.rstrip(", ") + "]"
