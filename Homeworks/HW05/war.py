from deck import *
from player import *

class WarPlayer(Player):

    def __init__(self):
        super().__init__()
        self.__disc = []

    @property
    def disc(self):
        return self.__disc

    def discard_to_hand(self):
        self.__hand.extend(self.__disc)
        self.__disc = []
        shuffle(self.__hand)

    def field_to_disc(self, field):
        self.__disc.extend(field)

    def __str__(self):
        curr = super().__str__() + "\n" + "Discard: ["

        for card in self.disc:
            curr += str(card) + " "

        return curr.strip(", ") + "]"

class War:
    def __init__(self):
        self.reset()

    def reset(self):
        self.__deck = Deck()
        self.__p1 = WarPlayer()
        self.__p2 = WarPlayer()
        self.__field = []

        for _ in range(26):
            self.__p1.add_card(self.__deck.deal())
            self.__p2.add_card(self.__deck.deal())

        self.found_winner = False
        self.last_won = None
        self.first = True

    @property
    def p1(self):
        return self.__p1

    @property
    def p2(self):
        return self.__p2

    @property
    def field(self):
        return self.__field

    def play_game(self):
        game_done = False
        print("Let's get this started!")
        while not game_done:
            if not self.first:
                print("\nGo Next Round? (Y|n)")
                print(">>>", end=" ")
                next_round = input().lower().strip()
                if next_round not in ['y', 'n', '']:
                    print("Invalid input. Please try again.")
                    continue
            game_done = not self.__next_round()

    def __next_round(self):
        # Doing "transition" of the last round to current round "clearing" board for this new round
        if not self.first:
            if self.last_won == "P1":
                self.p1.field_to_disc(self.field)
            else:
                self.p2.field_to_disc(self.field)

            self.__field = []

        # actual new round stuff
        self.first = False
        who_won_round = None
        while who_won_round is None:
            p1_card_played = self.p1.hand.pop()
            p2_card_played = self.p2.hand.pop()

            self.__field.append(p1_card_played)
            self.__field.append(p2_card_played)

            print(self.p1)
            print(f"Field: {p1_card_played} vs {p2_card_played}")
            print(self.p2)

            if p1_card_played != p2_card_played:
                who_won_round = p1_card_played > p2_card_played
            else:
                print("Tie. Draw Again.")

        print(who_won_round)
        game_winner = self.__check_game_winner()
        if game_winner is not None:
            if game_winner:
                print("Player 1 wins")
            else:
                print("Player 2 wins")
            print("Would you like to play again? (Y|n)")
            while True:
                print(">>>", end=" ")
                keep = input().lower().strip()
                if keep not in ['y', 'n', '']:
                    print("Invalid input. Please try again.")
                    continue
                else:
                    if keep == 'n':
                        print("Thank you for playing")
                        return False
                    else:
                        self.reset()
                    break
        else:
            self.last_won = "P1" if who_won_round else "P2"
            print(f"Round Winner: {self.last_won}")

        sanity = len(self.p1.hand) + len(self.p1.disc) + len(self.p2.hand) + len(self.p2.disc) + len(self.field)
        assert sanity == 52, "Something went wrong, this should always be 52"
        return True

    def __check_game_winner(self):
        p1_total = len(self.p1.hand) + len(self.p1.disc)
        p2_total = len(self.p2.hand) + len(self.p2.disc)

        if p1_total > 35:
            return True
        if p2_total > 35:
            return False

        if (len(self.p1.hand) == 0 and len(self.p1.disc) == 0) or (len(self.p2.hand) == 0 and len(self.p2.disc) == 0):
            return p1_total > p2_total

        if len(self.p1.hand) == 0:
            self.p1.discard_to_hand()

        if len(self.p2.hand) == 0:
            self.p2.discard_to_hand()

        return None

    def __str__(self):
        # war_str = str(self.p1)
        # war_str += '\n' + 'Field: ' + str(self.field)
        # war_str += '\n' + str(self.p2)
        # return war_str
        return "Nothing to see here for now"

war = War()
war.play_game()
