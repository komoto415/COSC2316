from deck import *
from player import *

class WarPlayer(Player):

    def __init__(self):
        super().__init__()
        self.disc = []

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
        self.__round = 0

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

    @property
    def round(self):
        return self.__round

    def play_game(self):
        game_done = False
        print("Go Next Round? (Y|n)")
        while not game_done:
            print(">>>", end=" ")
            next_round = input().lower().strip()
            if next_round not in ['y', 'n', '']:
                print("Invalid input. Please try again.")
                continue
            game_done = not self.next_round()

    def next_round(self):
        # Doing "transition" of the last round to current round "clearing" board for this new round
        if not self.first:
            if self.last_won == "P1":
                self.p1.disc.extend(self.field)
            else:
                self.p2.disc.extend(self.field)

            self.__field = []

        # actual new round stuff
        self.__round += 1
        self.first = False
        who_won_round = None
        while who_won_round is None:
            p1_card_played = self.p1.hand.pop()
            p2_card_played = self.p2.hand.pop()

            self.__field.append(p1_card_played)
            self.__field.append(p2_card_played)
            print(f"Field: {p1_card_played} vs {p2_card_played}")

            if p1_card_played != p2_card_played:
                who_won_round = p1_card_played > p2_card_played
            else:
                print("Tie. Draw Again.")

        print(who_won_round)
        game_winner = self.check_game_winner()
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
        print(self.p1)
        [print(card, end=" ") for card in self.field]
        print()
        print(self.p2)
        return True

    def check_game_winner(self):
        p1_total = len(self.p1.hand) + len(self.p1.disc)
        p2_total = len(self.p2.hand) + len(self.p2.disc)

        if p1_total > 35:
            return True
        if p2_total > 35:
            return False

        if (len(self.p1.hand) == 0 and len(self.p1.disc) == 0) or (len(self.p2.hand) == 0 and len(self.p2.disc) == 0):
            return p1_total > p2_total

        if len(self.p1.hand) == 0:
            self.p1.hand.extend(self.p1.disc)
            self.p1.disc = []
            shuffle(self.p1.hand)

        if len(self.p2.hand) == 0:
            self.p2.hand.extend(self.p2.disc)
            self.p2.disc = []
            shuffle(self.p2.hand)

        return None

    def __str__(self):
        # war_str = str(self.p1)
        # war_str += '\n' + 'Field: ' + str(self.field)
        # war_str += '\n' + str(self.p2)
        # return war_str
        return "Nothing to see here for now"

war = War()
# war.play_game()

