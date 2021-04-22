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
        self.__hand = [card for card in self.hand if card.face != face]

    def pick_card_to_ask(self):
        pass

    def __str__(self):
        return super().__str__()

class GoFishHuman(GoFishPlayer):
    def __init__(self):
        super().__init__()

    def pick_card_to_ask(self):
        [print(card) for card in self.hand]
        print("Ask for a card:")
        while True:
            print(">>>", end=" ")
            desired = input().lower().strip()
            if not desired in [card.face for card in self.hand]:
                print("You don't have a card of that value in your hand. Stupid.")
                [print(card) for card in self.hand]
                continue
            return desired

class GoFishComputer(GoFishPlayer):
    def __init__(self):
        super().__init__()
        self.last_asked = None

    def pick_card_to_ask(self):
        import random
        face_count = {}
        for card in self.hand:
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
                self.last_asked = desired
                return desired

class GoFish:
    def __init__(self):
        self.reset()

    def reset(self):
        self.__deck = Deck()
        self.__p1 = GoFishHuman()
        self.__p2 = GoFishComputer()
        self.__p1_points = 0
        self.__p2_points = 0

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

    def __add_point(self, player):
        if player == self.p1:
            self.__p1_points += 1
        elif player == self.p2:
            self.__p2_points += 1

    @staticmethod
    def found_four_of_a_kind(hand):
        count = {}
        for card in hand:
            count[card.face] = count.get(card.face, 0) + 1
        if 4 in count.values():
            return sorted(count.items(), key=lambda x: x[1])[-1][0]
        else:
            return None

    def play_game(self):
        game_done = False
        asker = self.p1
        askie = self.p2
        while not game_done:
            asker_asks_for = asker.pick_card_to_ask()
            if asker_asks_for in [card.face for card in askie.hand]:
                asker.add_card(askie.get_card_with_face(asker_asks_for))
            else:
                print("Go Fish")
                asker.add_card(self.__deck.deal())
            check_asker_hand = self.found_four_of_a_kind(asker.hand)
            check_askie_hand = self.found_four_of_a_kind(askie.hand)
            if not check_asker_hand is None:
                self.__add_point(asker)
                asker.remove_cards_with_face(check_asker_hand)
            if not check_askie_hand is None:
                self.__add_point(askie)
                askie.remove_cards_with_face(check_askie_hand)

            game_done = any([len(asker.hand) == 0, len(askie.hand) == 0])
            if not game_done:
                asker, askie = askie, asker

        if self.p1_points > self.p2_points:
            print("Human has wonnered")
        else:
            print("All your base are belong to us")

game = GoFish()
# while True:
# print("Player " + str(game.p1))
# print("Computer " + str(game.p2))
#
# game.comp_ask_for_card()
#
# print("Player " + str(game.p1))
# print("Computer " + str(game.p2))
# input()
