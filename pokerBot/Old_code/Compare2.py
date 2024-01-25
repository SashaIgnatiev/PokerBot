#This will be a program that takes the handDistribution of our opponents and compares it with our hand score
from handRankingspt2 import rating

#FIXME This method does not work for draws
def equity_postflop(our_cards, opponent_distribution, table):
    #Our win loss or tie counter against the opponetns distribution
    win_loss_tie = {
        'win' : 0,
        'loss': 0,
        'tie': 0
    }

    our_rating =  rating(our_cards + table)
    #going through each card, tallying a win loss or tie
    for i in opponent_distribution:
        if our_rating > rating(i + table):
            win_loss_tie['win'] += 1
        elif our_rating < rating(i + table):
            win_loss_tie['loss'] += 1
        else:
            win_loss_tie['tie'] += 1
    #Percentage of winning, i.e how much of the pot we should own
    equity = win_loss_tie['win'] / len(opponent_distribution)
    return equity




