
class Player:
    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def __str__(self):
        hand = "Hand: ["
        for card in self.hand:
            hand += str(card) + ", "

        return hand.strip(", ") + "]"