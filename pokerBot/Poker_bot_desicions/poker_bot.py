#This is poker_bots control center, this is where he will execute his instructions
from .Equity import equity
from .Villain import Villain
from .handRankingspt2 import pre_flop_rating
import time
import pyautogui
import random
import numpy as np
class PokerBot:
    def __init__(self, chips, bigBlind):
        self.position = None
        self.cards = []
        self.table = []
        self.chips = chips
        self.positon = None
        self.bigBlind = False
        self.big_blind_amount = bigBlind
        self.raise_total = 0
        self.raise_amount = 0
        self.name = 'PokerBot_MK1'
    #This mehtod currently only works for a HUNL style game
    def action(self, pot_size, bet ,bet_total, game_state, table, position, Raise = False, All_In = False):
        print(f'Inside action -- Cards: {self.cards}')
        print(f'TABLE: {table}')
        print(f'SELF CHIPS: {self.chips}')
      #  print('INSIDE ACTION')
        start_time = time.time()
        #print(pyautogui.position())
        if position == 0:
            self.bigBlind = True
            #print('WE ARE BIG BLIND...')
            player_1 = Villain('Player1')
            player_1.position = 'LP'
        else:
            self.bigBlind = False
            #print('WE ARE BIG DEALER...')
            player_1 = Villain('Player1')
            player_1.position = 'EP'
        total_equity = 1

        #print(f'POKER BOT RECIEVED INFO: TABLE: {table} BET_SIZE: {bet_size}: CARDS: {self.cards}')
        pot_odds = bet_total / pot_size


        if game_state != 'Pre-Flop':

            try:
                equity_against_player = equity(self.cards, player_1.preflop_hand_distribution(), table)
            except:
                if bet_total > 0:
                    return 'Fold'
                else:
                    return 'Check'
            total_equity *= equity_against_player

            """ Expected Value for Flop, Turn and River"""
            if game_state == 'Flop':
                pass




            """Equity if we call or check"""
            opponent_equity = 1 - total_equity
            win = total_equity * (pot_size)
            lose = -((1 - total_equity) * (bet_total))

            expected_value = win + lose

            """Expected value if we raise"""
            win_fold = total_equity * (pot_size + bet_total)
            win_call = (total_equity) * (pot_size + self.chips)
            lose_call = -((1 - total_equity)) * (self.chips)
            expected_value_raise = win_fold + win_call + lose_call

            if All_In == True:
                if expected_value > 0 or expected_value_raise > 0:
                    return 'Call'
                else:
                    return 'Fold'

            """If raising is optimal, find an amount such that our opponent might call"""
            if expected_value_raise > expected_value and expected_value_raise > 0 and All_In == False:

                closest_raise_amount = {}
                for i in range(int(self.chips)):
                    closest_raise_amount[abs(opponent_equity - (i/pot_size))] = i

                try:
                    self.raise_amount = closest_raise_amount[min(closest_raise_amount.keys())]
                except:
                    if self.raise_amount == 0:
                        return 'Check'
                    else:
                        return 'Call'
                if self.raise_amount < bet_total + bet:
                    self.raise_amount = bet_total + bet

                elif bet_total == 0 and self.raise_amount < self.big_blind_amount:
                    #Raising the big blind
                    self.raise_amount = self.big_blind_amount

                if self.raise_amount >= self.chips:

                    return 'All_In'
                else:
                    self.raise_total += self.raise_amount
                    return 'Raise'

            elif (expected_value_raise < expected_value and expected_value > 0) or (expected_value_raise < expected_value and expected_value > 0):

                if bet_total > 0:
                    return 'Call'
                elif bet_total == 0:
                    return 'Check'

            elif expected_value_raise <= 0 and expected_value <= 0:
                if bet_total == 0:
                    return 'Check'
                else:
                    return 'Fold'

        else:
            return self.pre_flop_action(bet_total, pot_size, bet, Raise = Raise, All_In = All_In)
    #Method that is going to decide whether we play our pre flop cards based on their hand rankings + position + prior bets




    def pre_flop_action(self, bet_total, pot_size, bet, Raise = False, All_In = False):
        if bet_total == 0 or bet == 0:

            bet = 100
            bet_total = 100

        print(f'OUR CHIPS: {self.chips}')
        #print(f'RAISE TOTAL:{self.raise_total}')


        number_ranking = pre_flop_rating(self.cards)
        print(f'NUMBER RANKING: {number_ranking}')
        #High Range
        if number_ranking <= 42:
            #print(f'BET SIZE: {bet_size} BIG BLIND: {self.big_blind_amount}')
            #These are our all in cards, we can raise all the way to our max value of chips
            if number_ranking <= 8:
                #print('PRETTY GOOD CARDS')
                #If we are first to act or our opponent checks, raise a smaller amount as to not scare our opponent off
                if bet_total == self.big_blind_amount:
                    #print('BIG BLIND == BETSIZE')
                    range_percentage = np.random.uniform(.04, .08)


                    self.raise_amount = self.raise_total + round((bet_total + bet) + (self.chips * range_percentage))


                    if self.raise_amount >= self.chips:
                       # print(self.chips)
                        return 'All_In'
                    self.raise_total += self.raise_amount
                    #print(f'RAISE AMOUNT:{self.raise_amount}')
                    return 'Raise'

                #If our opponent raises, we are going to reraise based on a percentage of their raised amount
                elif bet_total > self.big_blind_amount:
                    #self.raise_amount = (2 * bet_size) - self.raise_total
                    self.raise_amount = (pot_size * .5) + (bet + bet_total)
                    if self.raise_amount >= self.chips:
                        #print(self.chips)
                        return 'All_In'
                    self.raise_total += self.raise_amount
                    #print(f'RAISE AMOUNT:{self.raise_amount}')
                    return 'Raise'

            else:
                if bet_total == self.big_blind_amount:
                    #print('BET SIZE IS BIG')
                    #print(f'INSIDE BET_SIZE == BIG BLIND')
                    range_percentage = np.random.uniform(.04, .065)
                    range_percentage = range_percentage / abs(8 - number_ranking)

                    self.raise_amount = self.raise_total + round((bet_total + bet) + (range_percentage * self.chips))
                    #self.raise_amount = self.raise_total + self.big_blind_amount


                    if self.raise_amount >= self.chips:
                        #print(self.chips)
                        return 'All_In'

                    else:
                        self.raise_total += self.raise_amount
                        #print(f'RAISE AMOUNT:{self.raise_amount}')
                        return 'Raise'

                elif bet_total > self.big_blind_amount:
                    #print('HIGH LOW')
                    #FIXME
                    higher_range  =  self.chips * (.85 - (abs(9 - number_ranking) * .001090909))
                    lower_range = self.chips * (.45 - (abs(9 - number_ranking) * .001090909))

                    if bet_total <= higher_range and bet_total >= lower_range:
                        if bet_total == self.big_blind_amount and self.bigBlind == True:
                            return 'Check'
                        return 'Call'
                    elif bet_total <= lower_range:

                        self.raise_amount = round((bet_total + bet) + lower_range)

                        if self.raise_amount >= self.chips:
                            #print(self.chips)
                            return 'All_In'
                        else:
                            self.raise_total += self.raise_amount
                            #print(f'RAISE AMOUNT:{self.raise_amount}')
                            return 'Raise'
                    elif bet_total > higher_range:
                        return 'Fold'

        #Middle Range
        elif number_ranking >= 43 and number_ranking <= 84:
            #print(f'BET SIZE: {bet_size} BIG BLIND: {self.big_blind_amount}')
            #If top of middle range, min-click + percentage
            range_percentage = np.random.uniform(.02, .04)
            range_percentage =  range_percentage / abs(42 - number_ranking)

            if  self.big_blind_amount < bet_total and (bet_total <= ((2 * self.big_blind_amount) + (range_percentage * self.chips))):
                return 'Call'
            elif (bet_total > ((2 * self.big_blind_amount) + (range_percentage * self.chips))):
                if bet_total == self.big_blind_amount and self.bigBlind == True:
                    return 'Check'
                return 'Fold'

            elif bet_total == self.big_blind_amount:
                #print(f'INSIDE BET_SIZE == BIG BLIND')

                self.raise_amount = round((bet + bet_total) + (range_percentage * self.chips))
                #self.raise_amount = self.raise_total + self.big_blind_amount
                if self.raise_amount >= self.chips:
                   # print(self.chips)
                    return 'All_In'

                self.raise_total += self.raise_amount
               # print(f'RAISE AMOUNT:{self.raise_amount}')
                return 'Raise'


        #Low Range
        #if bet_size == Big Blind
        elif number_ranking >= 85 and number_ranking <= 125:
           # print(f'BET SIZE: {bet_size} BIG BLIND: {self.big_blind_amount}')
            if bet_total == self.big_blind_amount and self.bigBlind == False:
                return 'Call'
            elif bet_total == 100 and self.bigBlind == True:
               # print(f'INSIDE BET_SIZE == BIG BLIND')
                return 'Check'
            else:
                return 'Fold'

        #Check/Fold Range
        elif number_ranking >= 126 and number_ranking <= 169:
           # print(f'BET SIZE: {bet_size} BIG BLIND: {self.big_blind_amount}')
            if bet_total == self.big_blind_amount and self.bigBlind == False:
             #   print(f'INSIDE BET_SIZE == BIG BLIND')
                return 'Fold'
            elif bet_total == self.big_blind_amount and self.bigBlind == True:
                return 'Check'
            else:
                return 'Fold'



















