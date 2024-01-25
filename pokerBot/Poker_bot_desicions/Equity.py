#This method calculates the equity of our hand based on
# if we are winning currently and draws in the future
from .Villain import Villain
from .suit_win_lose import suit_win_lose
from .handRankingspt2 import rating
from .deck import Deck
def equity(our_cards, player_distribution, table):

    win_loss_tie = {
        'win': 0,
        'loss': 0,
        'tie': 0
    }
    deck1 = Deck()
    deck2 = Deck()

    deck1.remove_cards(our_cards + table)
    deck2.remove_cards(our_cards + table)
    #If this is the flop
    if len(table) == 3:

        our_rating = rating(our_cards + table)
        for i in player_distribution:

            suited = False
            if i[2] == 's':
                suited = True

            #We are going to go through all possiblilities to calculate chances of winning
            for ii in deck1.deck:

                #print(deck1.deck)
                deck2.remove_cards([ii])

                for iii in deck2.deck:
                    table2 = table + [ii] + [iii]

                    #print(i)
                    #Check for flush // see flush_checker
                    game_winner = suit_win_lose(table2, i, suited, our_cards)
                    #print(game_winner)
                    win_loss_tie['loss'] += game_winner['win']
                    win_loss_tie['win'] += game_winner['lose']
                    win_loss_tie['tie'] += game_winner['tie']
                deck2.add_cards([ii])
    #Checking equity if table is on the turn
    if len(table) == 4:
        for i in player_distribution:
            suited = False
            if i[2] == 's':
                suited = True
            for ii in deck1.deck:
                table3 = table + [ii]
                game_winner = suit_win_lose(table3, i[:2], suited, our_cards)
                win_loss_tie['loss'] += game_winner['win']
                win_loss_tie['win'] += game_winner['lose']
                win_loss_tie['tie'] += game_winner['tie']


    #Checking equity after the river card
    if len(table) == 5:
        for i in player_distribution:
            suited = False

            if i[2] == 's':
                suited = True
            game_winner = suit_win_lose(table, i[:2], suited, our_cards)

            win_loss_tie['loss'] += game_winner['win']
            win_loss_tie['win'] += game_winner['lose']
            win_loss_tie['tie'] += game_winner['tie']

    return win_loss_tie['win']/(win_loss_tie['win'] + win_loss_tie['loss'] + win_loss_tie['tie'])

if __name__ == '__main__':
    vllain = Villain('player1')

    our_cards = ['Tc', 'Td']
    x = vllain.preflop_hand_distribution()
    print(x)
    table = ['6s', '3h', '8d', 'Qh', 'Ks']

    print(equity(our_cards, x, table))

