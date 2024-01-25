from .Pre_flop_hand_rankings import hand_rankings
import phevaluator


#Method is responsible for checking the amount of cards and giving it
# to the correct ranking system for each turn
def rating(cards):

    #Pre-Flop Cards
    if len(cards) == 2:
        return pre_flop_rating(cards)

    #Flop Cards
    if len(cards) == 5:
        return flop_rating(cards)
    #Turn Cards
    if len(cards) == 6:
        return turn_rating(cards)

    #River Cards
    if len(cards) == 7:
        return river_rating(cards)

#All pre-flop hands have been ranked from 1-169, this gets our hand and finds its ranking
def pre_flop_rating(cards):
    string = ''
    val = 'AKQJT98765432'
    if cards[0][0] == cards[1][0]:
        string += cards[0][0] + cards[0][0] +'o'
        return hand_rankings[string]
    else:
        for i in val:
            if i == cards[0][0] or i == cards[1][0]:
                string += i
    x = cards[0][1]
    y = cards[1][1]
    if x == y:
        string += 's'
    else:
        string += 'o'

    return hand_rankings[string]
#Evaluator method that takes x amount of cards and returns its general
# ranking against the other combination of cards, being used for all 3 stages of the game

def flop_rating(cards):
    return phevaluator.evaluate_cards(cards[0], cards[1], cards[2], cards[3], cards[4])
def turn_rating(cards):
    return phevaluator.evaluate_cards(cards[0], cards[1], cards[2], cards[3], cards[4], cards[5])
def river_rating(cards):
    return phevaluator.evaluate_cards(cards[0], cards[1], cards[2], cards[3], cards[4], cards[5], cards[6])


if __name__ =='__main__':
    print(phevaluator.evaluate_cards('Ac', 'Kc', 'Qc', 'Jc', 'Tc'))


