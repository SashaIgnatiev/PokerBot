#This method checks to see if there is a possible flush AND if that possible flush beats our cards
from .handRankingspt2 import rating
from .deck import Deck


def suit_win_lose(table, villain_hand, suited, our_cards):
    win_lose_tie ={ 'win': 0,
                    'lose': 0,
                    'tie' : 0


    }
    suits = ['h', 's', 'c', 'd']
    deck = Deck()
    deck.remove_cards(our_cards + table)
    our_value = rating(our_cards + table)



    #Now we deal with different suits, if suited == yes then there are 4 combos of cards to check if theu beat ours
    if suited == True:
        for i in suits:

            left_card = str(villain_hand[0]) + i
            right_card = str(villain_hand[1]) + i
            #Check if right and left cards exist
            if deck.is_in_deck(left_card) == True and deck.is_in_deck(right_card) == True:
                new_villain_hand = [left_card, right_card]
                villain_rating = rating(new_villain_hand + table)
                #If theu exist then we check to see if we win or lose

                if villain_rating < our_value:
                    win_lose_tie['win'] += 1
                elif villain_rating > our_value:
                    win_lose_tie['lose'] += 1
                else:
                    win_lose_tie['tie'] += 1
    #If suited == no then there are 16 combinations of cards to check, -4 from repeated suited cards  makes 12 combination of cards max to check
    if suited == False:

        for i in suits:
            for ii in suits:
                left_card = str(villain_hand[0][0]) + i
                right_card =  str(villain_hand[1][0]) + ii
                #Check to see if right and left card exist and we check to make sure they arent the same suit
                if (deck.is_in_deck(left_card) == True and deck.is_in_deck(right_card) == True) and (i != ii):
                    new_villain_hand = [left_card, right_card]
                    villain_rating = rating(new_villain_hand + table)
                    #If all conditions are met we check to see if opponent win lose or tie
                    if villain_rating < our_value:
                        win_lose_tie['win'] += 1
                    elif villain_rating > our_value:
                        win_lose_tie['lose'] += 1
                    else:
                        win_lose_tie['tie'] += 1
    return win_lose_tie

#Tester case
if __name__ == '__main__':
    table = ['6s', 'Qh', 'Ah', 'Th', '8c']
    villain_hand = 'KJ'
    our_hand = ['As', 'Ac']


    our_value = rating(our_hand + table)
    print(our_value)
    suited = True
    x = suit_win_lose(table, villain_hand, suited, our_hand)
    print(x)

