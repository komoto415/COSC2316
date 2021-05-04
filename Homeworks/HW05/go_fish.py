import random

import utils
from deck import *
from player import *

# from heapq import heappop, heappush, heapify

HAND_SIZE = 7
STANDARD_DECK_SIZE = 52

class GoFishPlayer(Player):

    def __init__(self, name, player_id=0):
        super().__init__(name=name, player_id=player_id)

    def decide_how_to_play_turn(self, players_list, visible_cards):
        return self.player_id, None

    def __eq__(self, other):
        return super().__eq__(other)

    def __str__(self):
        return super().__str__()

class GoFishHuman(GoFishPlayer):
    def __init__(self):
        super().__init__("Human")

    def decide_how_to_play_turn(self, players_list, visible_cards):
        askie_no, desired = super().decide_how_to_play_turn(players_list, visible_cards)

        attempts = 1
        valid_computer_id = False
        while not valid_computer_id:
            if attempts % 5 == 1:
                print("Your current hand:")
                [print(card, end=" ") for card in self.hand]
                print()
                print("Which computer would you like to ask a card for?")
                for computer_no in range(1, len(players_list)):
                    print(f"Computer {computer_no}")
            print(">>>", end=" ")
            try:
                askie_no = int(input().strip())
            except ValueError as _:
                print("You have to put an integer value. Please try again")
                attempts += 1
            else:
                valid_computer_id = askie_no in range(1, len(players_list))
                if not valid_computer_id:
                    print("That is not a valid computer player. Please try again")
                    attempts += 1
                    continue

        print("\nAsk for a card:")
        attempts = 1
        card_in_hand = False
        while not card_in_hand:
            if attempts % 5 == 1:
                print("Your current hand:")
                [print(card, end=" ") for card in self.hand]
                print()
            print(">>>", end=" ")
            desired = input().upper().strip()
            card_in_hand = desired in self.hand_as_faces()
            if not card_in_hand:
                print("You don't have a card of that value in your hand. Stupid.")
                attempts += 1
                continue

        assert askie_no != 0 and desired is not None, "Something went wrong"

        return askie_no, desired

    def __eq__(self, other):
        return super().__eq__(other)

    def __str__(self):
        return super().__str__()

class GoFishComputer(GoFishPlayer):
    def __init__(self, player_id):
        super().__init__("Computer", player_id=player_id)
        self.__last_asked = None

    def decide_how_to_play_turn(self, players_list, visible_cards):
        assert visible_cards is not None

        askie_no, desired = super().decide_how_to_play_turn(players_list, visible_cards)

        # Based off 'visible' cards
        """
        look through the set of visible hands,  
        look at my own hand and see if I can make a four of a kind
        """
        my_groups = utils.group_by_frequency_max_4(self.hand_as_faces())
        # print("last asked:", self.__last_asked)
        # print(my_groups)

        visible_groups = tuple(utils.group_by_frequency_max_4(hand) for hand in visible_cards)
        # print(visible_groups)

        early_exit = False
        """
        0 -> Cards that make pairs
        1 -> Cards that make trips
        2 -> Cards that make quads
        """
        can_ask = tuple(([], [], []) for _ in range(len(visible_groups)))
        has_something_to_ask_for = [False for _ in range(len(visible_groups))]
        for i, groups in enumerate(visible_groups):
            if i == self.player_id:
                # print("Skipping myself")
                ...
            else:
                # for me, other in zip(reversed(my_groups[:-1]), groups[:-1]):
                #     #    me goes 3,2,1
                #     # other goes 1,2,3
                #     makes_four = list(set(me).intersection(other))
                #     print(me, other)
                #     print(makes_four)
                #     if makes_four:
                #         can_ask[i].extend(makes_four)
                #         # askie_no = i
                #         # In the case that there are multiple cards that can make 4 with the current assessment
                #         # Flip?
                for j, me in enumerate(my_groups[:-1]):
                    for k, other in enumerate(groups[:-1]):
                        if j + k > 2:
                            continue

                        # print(j, me)
                        # print(k, other)
                        like_cards = list(set(me).intersection(other))
                        if like_cards and has_something_to_ask_for[i] is not None:
                            has_something_to_ask_for[i] = True
                        can_ask[i][j + k].extend(like_cards)
            #             print()
            #         print()
            # print()

        # print(can_ask)
        # print(has_something_to_ask_for)

        """
        0 -> Quad
        1 -> Trip
        2 -> Pair
        """
        if any(has_something_to_ask_for):
            best_at = 3
            askie_no = self.player_id
            for i, groups in enumerate(can_ask):
                if i == self.player_id:
                    # print("Skipping myself")
                    ...
                else:
                    for j, group in enumerate(reversed(groups)):
                        if group and best_at > j:
                            desired = self.__get_desired_from_group(group)
                            askie_no = i
        else:
            # print("no pairs trips or quads found")
            # Random Player selection. THIS WORKS
            while askie_no == self.player_id:
                askie_no = random.randint(0, len(players_list) - 1)

            for group in reversed(my_groups):
                if group:
                    try:
                        group.remove(self.__last_asked)
                    except ValueError as _:
                        pass
                    break
            # print(my_groups)

            for group in reversed(my_groups):
                if group:
                    desired = self.__get_desired_from_group(group)

        self.__last_asked = desired

        assert askie_no != self.player_id and desired is not None, "Something went wrong"

        return askie_no, desired

    @staticmethod
    def __get_desired_from_group(group):
        if len(group) == 1:
            flip = 0
        else:
            flip = random.randint(0, len(group) - 1)
        # print("flip:", flip)
        return group[flip]



    def __eq__(self, other):
        return super().__eq__(other)

    def __str__(self):
        return super().__str__()

class GoFish:
    def __init__(self, num=1):
        assert num > 0, "Can't play by yourself, loser"
        self.__num_computers = num
        self.reset()

    def reset(self):
        self.__players_list = [GoFishHuman()]
        self.__players_list.extend([GoFishComputer(i) for i in range(1, self.num_computers + 1)])
        self.__player_points = [0 for _ in range(self.num_computers)]
        self.__visible_hand = tuple([] for _ in range(len(self.players_list)))
        self.__deck = Deck(num_decks=self.__adjust_deck_size_to_player_count())
        # ACTUAL CARD DEALING
        for _ in range(HAND_SIZE):
            for player in self.players_list:
                player.add_card(self.__deck.deal())

        # FIXED HANDS FOR TESTING ONLY
        # for i in range(2, HAND_SIZE + 2):
        #     for player in self.players_list:
        #         player.add_card(Card(i, Card.Suit.Spades))

    @property
    def num_computers(self):
        return self.__num_computers

    @property
    def players_list(self):
        return self.__players_list

    @property
    def player_points(self):
        return self.__player_points

    @property
    def visible_hand(self):
        return self.__visible_hand

    def __adjust_deck_size_to_player_count(self):
        min_cards_for_player_count = len(self.players_list) * HAND_SIZE
        return min_cards_for_player_count // STANDARD_DECK_SIZE + 1

    def __add_point(self, player_no):
        self.__player_points[player_no] = self.__player_points[player_no] + 1

    def associate_player_with_n_face(self, player_id, face, n=1):
        self.__visible_hand[player_id].extend([face] * n)

    def clear_player_of_face(self, player_id, face):
        while face in self.__visible_hand[player_id]:
            self.__visible_hand[player_id].remove(face)

    def clear_player_of_n_face(self, player_id, face, n):
        cards_of_face_found = 0
        while cards_of_face_found < n and self.__visible_hand[player_id]:
            self.__visible_hand[player_id].remove(face)
            cards_of_face_found += 1

    def score_four_of_a_kinds(self, player):
        faces = utils.get_four_of_a_kind_faces(player.hand_as_faces())

        if faces:
            for face in faces:
                self.__add_point(player.player_id)
                player.discard_four_of_a_kind_with_face(face)

    def play_game(self):
        game_done = False
        for player in self.players_list:
            self.score_four_of_a_kinds(player)
        asker_no = 0
        while not game_done:
            asker_no = asker_no % len(self.players_list)
            asker = self.players_list[asker_no]
            asker_pretty = f"{asker.name}-{asker.player_id}"
            print(f"{asker_pretty}'s turn")

            askie_no, asker_asks_for = asker.decide_how_to_play_turn(self.players_list, self.visible_hand)
            askie = self.players_list[askie_no]
            askie_pretty = f"{askie.name}-{askie.player_id}"

            print(f"{asker_pretty} asks {askie_pretty} for a {asker_asks_for}")
            # print("HANDS BEFORE")
            # print(asker)
            # print(askie)
            # print()

            steals = asker_asks_for in [card.face_str() for card in askie.hand]
            self.associate_player_with_n_face(asker_no, asker_asks_for)
            # print(self.visible_hand)
            if steals:
                stolen_cards = utils.give_up_all_cards_with_face(askie.hand, asker_asks_for)
                print(f"{askie_pretty} gives over {len(stolen_cards)} {asker_asks_for}"
                      f"{'' if len(stolen_cards) == 1 else 's'} to {asker_pretty}")
                for card in stolen_cards:
                    asker.add_card(card)
                self.associate_player_with_n_face(asker_no, asker_asks_for, len(stolen_cards))
                self.clear_player_of_face(askie_no, asker_asks_for)
            else:
                print("Go Fish")
                asker.add_card(self.__deck.deal())
            print()
            # print("HANDS AFTER")
            # print(asker)
            # print(askie)
            # print()
            #
            # print("VISIBLE HAND")
            # print(self.visible_hand)

            game_done = any([len(asker.hand) == 0, len(askie.hand) == 0])
            if not game_done:
                asker_no += 1

        winners = [self.players_list[player_no] for player_no, points in enumerate(self.player_points)
                   if points == max(self.player_points)]

        if len(winners) == 1:
            winner = winners[0]
            print(f"{winner.name}{winner.player_id} won")
        else:
            for i, winner in enumerate(winners):
                print(f"{winner.name}{winner.player_id}", end="")
                if i != len(winners) - 1:
                    if i == len(winners) - 2:
                        print(" and", end=" ")
                    else:
                        print(",", end=" ")
            else:
                print(" won")

def main():
    num_computers = 2
    game = GoFish(num_computers)
    game.play_game()

if __name__ == "__main__":
    main()
