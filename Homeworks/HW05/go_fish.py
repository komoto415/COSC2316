from deck import *
from player import *

class GoFishPlayer(Player):
    def __init__(self):
        super().__init__()

    def get_card_with_face(self, face):
        for card in self.hand:
            if card.face == face:
                self.hand.remove(card)
                return card
        raise

    def remove_cards_with_face(self, face):
        self.hand = [card for card in self.hand if card.face != face]

    def __str__(self):
        return super().__str__()

# VALID = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "a", "jack", "queen", "king", "ace"]
#
# VALIDS = {
#     "2": 2,
#     "3":
#     }


class GoFish:
    def __init__(self):
        self.reset()

    def reset(self):
        self.__deck = Deck()
        self.__p1 = GoFishPlayer()
        self.__p2 = GoFishPlayer()
        self.__p1_points = 0
        self.__p2_points = 1
        self.last_asked = None

        for _ in range(7):
            self.__p1.add_card(self.__deck.deal())
            self.__p2.add_card(self.__deck.deal())

    @property
    def p1(self):
        return self.__p1

    @property
    def p2(self):
        return self.__p2

    @property
    def p1_points(self):
        return self.__p1_points

    @property
    def p2_points(self):
        return self.__p2_points

    def add_point(self, player):
        if player == self.p1:
            self.__p1_points += 1
        elif player == self.p2:
            self.__p2_points += 1

    def comp_ask_for_card(self):
        import random
        face_count = {}
        for card in self.p2.hand:
            face_count[card.face] = face_count.get(card.face, 0) + 1

        groups = ([], [], [], [])

        for face, count in face_count.items():
            groups[count - 1].append(face)

        print(groups)
        print("last asked:", self.last_asked)
        for group in reversed(groups):
            if group:
                try:
                    group.remove(self.last_asked)
                except ValueError as _:
                    pass
                break
        print(groups)

        for group in reversed(groups):
            if group:
                if len(group) == 1:
                    flip = 0
                else:
                    flip = random.randint(0, len(group) - 1)
                print("flip:", flip)
                desired = group[flip]
                print("desired:", desired)

                if desired in [card.face for card in self.p1.hand]:
                    self.p2.add_card(self.p1.get_card_with_face(desired))
                else:
                    print("Go Fish")
                    self.p2.add_card(self.__deck.deal())

                self.last_asked = desired

                break

    def ask_for_card(self):
        [print(card) for card in self.p1.hand]
        print("Ask for a card:")
        while True:
            print(">>>", end=" ")
            desired = input().lower().strip()
            if not desired in [card.face for card in self.p1.hand]:
                print("You don't have a card of that value in your hand. Stupid.")
                continue
            else:
                if desired in [card.face for card in self.p2.hand]:
                    self.p1.add_card(self.p2.get_card_with_face(desired))
                else:
                    print("Go Fish")
                    self.p1.add_card(self.__deck.deal())
                    break

    def play_game(self):
        game_done = False
        while not game_done:
            self.ask_for_card()
            check_p1_hand = self.found_four_of_a_kind(self.p1.hand)
            if not check_p1_hand is None:
                self.add_point(self.p1)
                self.p1.remove_cards_with_face(check_p1_hand)
            self.comp_ask_for_card()
            check_p2_hand = self.found_four_of_a_kind(self.p2.hand)
            if not check_p2_hand is None:
                self.add_point(self.p2)
                self.p2.remove_cards_with_face(check_p2_hand)
            game_done = len(self.p1.hand) == 0 or len(self.p2.hand) == 0

        if self.p1_points > self.p2_points:
            print("Human has wonnered")
        else:
            print("All your base are belong to us")

    @staticmethod
    def found_four_of_a_kind(hand):
        count = {}
        for card in hand:
            count[card.face] = count.get(card.face, 0) + 1
        if 4 in count.values():
            return sorted(count.items(), key=lambda x: x[1])[-1][0]
        else:
            return None

game = GoFish()
while True:
    print("Player " + str(game.p1))
    print("Computer " + str(game.p2))

    game.comp_ask_for_card()

    print("Player " + str(game.p1))
    print("Computer " + str(game.p2))
    input()
