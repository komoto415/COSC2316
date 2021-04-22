import random

from deck import *
from player import *

HAND_SIZE = 7
STANDARD_DECK_SIZE = 52

class GoFishPlayer(Player):
    def __init__(self, name, player_id=0):
        super().__init__(name=name, player_id=player_id)

    def get_card_with_face(self, face):
        for card in self.hand:
            if card.face == face:
                self.__hand.remove(card)
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
        super().__init__("Human")

    def pick_card_to_ask(self):
        print("Your current hand:")
        [print(card, end=" ") for card in self.hand]
        print("\nAsk for a card:")
        attempts = 1
        card_in_hand = False
        while not card_in_hand:
            print(">>>", end=" ")
            desired = input().lower().strip()
            card_in_hand = desired in [str(card.face_str()).lower() for card in self.hand]
            if not card_in_hand:
                print("You don't have a card of that value in your hand. Stupid.")
                if attempts % 5 == 1 and attempts != 1:
                    [print(card, end=" ") for card in self.hand]
                    print()
                attempts += 1
                continue
            return desired

    def __str__(self):
        return super().__str__()

class GoFishComputer(GoFishPlayer):
    def __init__(self, player_id):
        super().__init__("Computer", player_id=player_id)
        self.last_asked = None

    def pick_card_to_ask(self):
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

    def __str__(self):
        return super().__str__()

class GoFish:
    def __init__(self, num=1):
        assert num > 0, "Can't play by yourself, loser"
        self.__num_computers = num
        self.reset()

    def reset(self):
        self.__players = [GoFishHuman()]
        self.__players.extend([GoFishComputer(i) for i in range(1, self.num_computers + 1)])
        self.__player_points = [0 for _ in range(self.num_computers)]
        self.__deck = Deck(num_decks=self.__adjust_deck_size_to_player_count())
        for _ in range(HAND_SIZE):
            for player in self.players:
                player.add_card(self.__deck.deal())

    @property
    def num_computers(self):
        return self.__num_computers

    @property
    def players(self):
        return self.__players

    def __adjust_deck_size_to_player_count(self):
        min_cards_for_player_count = len(self.players) * HAND_SIZE
        return min_cards_for_player_count // STANDARD_DECK_SIZE + 1

    def __add_point(self, player_no):
        self.__player_points[player_no] = self.__player_points[player_no] + 1

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
        while not game_done:
            for player_no, player in enumerate(self.players):
                asker = player
                askie_no = player_no
                if isinstance(asker, GoFishHuman):
                    print("Which computer would you like to ask a card for?")
                    [print(f"Computer {computer_no}") for computer_no in range(1, self.num_computers + 1)]
                    attempts = 1
                    valid_computer_id = False
                    while not valid_computer_id:
                        try:
                            print(">>>", end=" ")
                            askie_no = int(input().strip())
                            valid_computer_id = askie_no in range(1, self.num_computers + 1)
                            if not valid_computer_id:
                                print("That is not a valid computer player. Please try again")
                                if attempts % 5 == 1 and attempts != 1:
                                    [print(f"Computer {computer_no}") for computer_no in
                                     range(1, self.num_computers + 1)]
                                attempts += 1
                                continue
                        except ValueError as _:
                            print("You have to put an integer value. Please try again")
                else:
                    while askie_no == player_no:
                        askie_no = random.randint(0, len(self.players) - 1)
                print(f"{asker.name}{asker.player_id}'s turn")
                askie = self.players[askie_no]
                asker_asks_for = asker.pick_card_to_ask()
                print(asker)
                print(askie)
                print(f"{asker.name}{asker.player_id} asks {askie.name}{askie.player_id} for a {asker_asks_for}")
                input("Slowing down just to see each turn")
                print()
                if asker_asks_for in [str(card.face).lower for card in askie.hand]:
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

        # if self.p1_points > self.p2_points:
        #     print("Human has wonnered")
        # else:
        #     print("All your base are belong to us")

def main():
    num_computers = 2
    game = GoFish(num_computers)
    game.play_game()

if __name__ == "__main__":
    main()

# while True:
# print("Player " + str(game.p1))
# print("Computer " + str(game.p2))
#
# game.comp_ask_for_card()
#
# print("Player " + str(game.p1))
# print("Computer " + str(game.p2))
# input()
