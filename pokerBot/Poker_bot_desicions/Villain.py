#This is going to be a class for information on each player on the game,
# this will hold their betting pattenrns, thier card distribution
from .Pre_flop_hand_rankings import  hand_rankings

class Villain:
    def __init__(self, name):
        self.name = name
        self.bet = 0
        self.card_distribution= []
        self.position = ''

    def preflop_hand_distribution(self):
        ordered_rankings = list(hand_rankings)

        #our_position = position.position[self.name]
        our_position = 'EP'
        if our_position == 'EP':
            expected = 42
        elif our_position == 'MP':
            expected = 85
        elif our_position == 'LP':
            expected = 127
        #Adds the cards from pre_flop_hand_rankings to the player distribution,
        # if we are holding one the cards it skips and moves on
        for i in range(expected):
            self.card_distribution.append(ordered_rankings[i])
        return self.card_distribution

if __name__ == '__main__':
    ordered_rankings = list(hand_rankings)
    print((ordered_rankings))
