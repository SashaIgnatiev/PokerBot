from Poker_bot_desicions.deck import Deck
import random
from Poker_bot_desicions.poker_bot import PokerBot
from Poker_bot_desicions.handRankingspt2 import rating
from Poker_game.player import Player
from database import database

class Table:

    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.bot = PokerBot(3000)
        self.action = 0
        self.position = [self.bot, self.player]
        self.pot_size = 0
        self.board = []
        self.game_state = 'Pre-Flop'

    def deal_cards(self):


        #Random card 1 for player
        rand_card = random.choice(self.deck.deck)
        self.player.recieve_cards(rand_card)
        self.deck.remove_cards(rand_card)

        #Random card 2 for player
        rand_card = random.choice(self.deck.deck)
        self.player.recieve_cards(rand_card)
        self.deck.remove_cards(rand_card)

        #Random card 1 for Bot
        rand_card = random.choice(self.deck.deck)
        self.bot.cards.append(rand_card)
        self.deck.remove_cards(rand_card)

        #Random card 2 for bot
        rand_card = random.choice(self.deck.deck)
        self.bot.cards.append(rand_card)
        self.deck.remove_cards(rand_card)
        print(f'Player Cards: {self.player.cards}')
        #print(f'Bot Cards {self.bot.cards}')


    #Responsible for switching positions after the round ends
    def new_position(self):
        placeHolder = self.position[0]
        self.position[0] = self.position[-1]
        self.position[-1] = placeHolder

        #position[0] is going to be dealer
        self.position[0].chips -= 100
        self.pot_size += 100

        #Position[-1] is going to be BB
        self.position[-1].chips -= 50
        self.pot_size += 50
        if self.position[0] == self.player:
            self.player.raise_amount = 100
            self.player.raise_total += 100
            self.bot.raise_amount = 50
            self.bot.raise_total += 50
            self.player.bigBlind = True
            self.bot.bigBlind = False
            self.bot_betting(preflop = True)
        else:
            self.bot.raise_amount = 100
            self.bot.raise_total += 100
            self.player.raise_amount = 50
            self.player.raise_total += 50
            self.bot.bigBlind = True
            self.player.bigBlind = False
            self.player_betting(preflop = True)



    def player_betting(self, Raise = False , preflop = False):
        if self.game_state == 'Pre-Flop':
            preflop = True

        action = self.player.action(preflop, Raise)

        if action == 'All_In':
            self.all_in_winner(self.bot, self.player, self.game_state)
        #If player raises, next turn will alwyas be passed to the bot
        elif action == 'Raise':
            if self.player.raise_amount >= self.bot.chips:
                self.all_in_winner(self.bot, self.player, self.game_state)
            self.player.chips -= self.player.raise_amount
            self.pot_size += self.player.raise_amount
            self.print_action(action, self.player)
            self.bot_betting(Raise = True)
        #If player calls or checks and they are in last position we move on to the next turn
        elif (action == 'Check' and self.position[-1] == self.player) or (action == 'Check' and self.player.bigBlind == True and self.game_state == 'Pre-Flop'):
            self.next_action(self.position[0], self.position[-1])
            self.print_action(action, self.player)
        elif action == 'Check' and self.position[-1] != self.player:
            self.print_action(action, self.player)
            self.bot_betting()
        #If player calls then we will alwyas move on to the next turn on the table
        elif action == 'Call':
            self.player.chips -= self.bot.raise_total - self.player.raise_total
            self.pot_size += self.bot.raise_total - self.player.raise_total
            self.player.raise_total += self.bot.raise_total - self.player.raise_total

            self.print_action(action, self.player)
            if self.game_state == 'Pre-Flop' and self.player.bigBlind == False and self.bot.raise_amount == 0:
                self.bot_betting(preflop = True)
            else:

                self.next_action(self.position[0], self.position[-1])

        elif action == 'Fold':
            self.bot.chips += self.pot_size
            self.pot_size = 0
            self.reset_round()








    def bot_betting(self, Raise = False, preflop = False):
        if preflop == True and self.bot.bigBlind == False:
            action = self.bot.action(self.pot_size, self.player.raise_amount, self.game_state, self.board, self.position, Raise = True)
        else:
            action = self.bot.action(self.pot_size, self.player.raise_amount, self.game_state, self.board, self.position, Raise)
        if action == 'All_In':
            self.all_in_winner(self.player, self.bot, self.game_state)

        elif action == 'Raise':
            if self.bot.raise_amount >= self.player.chips:
                self.all_in_winner(self.player, self.bot, self.game_state)

            self.bot.chips -= self.bot.raise_amount
            self.pot_size += self.bot.raise_amount
            self.print_action(action, self.bot)
            self.player_betting(Raise = True)
        elif (action == 'Check' and self.position[-1] == self.bot) or (action == 'Check' and self.game_state == 'Pre-Flop'):
            self.print_action(action, self.bot)
            self.next_action(self.position[0], self.position[-1])

        elif action == 'Check' and self.position[-1] != self.bot and self.game_state != 'Pre-Flop':
            self.print_action(action, self.bot)
            self.player_betting()

        elif action == 'Call':

            self.bot.chips -= self.player.raise_total - self.bot.raise_total
            self.pot_size += self.player.raise_total - self.bot.raise_total
            self.bot.raise_total += self.player.raise_total - self.bot.raise_total

            self.print_action(action, self.bot)
            if self.player.bigBlind == True and self.game_state == 'Pre-Flop' and self.pot_size == 200:
                self.player_betting(preflop = True)
            else:
                self.next_action(self.position[0], self.position[-1])

        elif action == 'Fold':
            self.player.chips += self.pot_size
            self.pot_size = 0
            self.reset_round()

    #Function that takes the chips in the pot and gives it to the winner
    def winner(self, currentplayer, end = False):
        currentplayer.chips += self.pot_size
        if self.bot.chips <= 0 and end == True:
            print(f'YOU WON, nice job beating poker bot\nYour chips: {self.player.chips}\nPoker bot chips {self.bot.chips}')
            database.performance_stat_tracker('LOSE')

        elif self.player.chips <= 0 and end == True:
            print(f'HAHAHAHAH HOW DID YOU LOSE TO POKER BOT, man you sure suck at poker, i would recommend laying down the cards')
            database.performance_stat_tracker('WIN')

        else:

            print(f'Pot Size: {self.pot_size}')
            print(f'Your Chips: {self.player.chips}')
            print(f'Bots Chips: {self.bot.chips}')
            self.reset_round()






    #Method that deals with all ins or when both player make it to the river and dont fold
    def all_in_winner(self, caller, all_in_player, game_state, call = False):
        self.pot_size += all_in_player.chips
        all_in_player.raise_total += all_in_player.chips
        all_in_player.chips = 0

        caller_amount = caller.raise_total + caller.chips
        all_in_amount = all_in_player.raise_total

        if caller_amount < all_in_amount:
            print('CALLER HAS LESS CHIPS')
            call_amount = caller_amount - caller.raise_total
            all_in_player.chips += all_in_amount - caller_amount
            self.pot_size -= all_in_amount - caller_amount
        elif caller_amount > all_in_amount:
            print('CALLER HAS MORE CHIPS')
            call_amount = all_in_amount - caller.raise_total
            caller.chips += caller_amount - all_in_amount
        else:
            call_amount = caller_amount - caller.raise_total
            print('CHIPS ARE EQUAL')


        if caller == self.player:
            action = caller.action_all_in()
        else:
            action = caller.action(self.pot_size, self.player.raise_amount, self.game_state, self.board, self.position, All_In = True, Raise = True)
            if action == 'Raise':
                action = 'Call'
        if action == 'Fold':

            self.winner(all_in_player)

        if action == 'Call':
            caller.chips -= call_amount
            self.pot_size += call_amount
            if game_state == 'Pre-Flop':
                self.board.append(self.deck.deal_random_card())
                self.board.append(self.deck.deal_random_card())
                self.board.append(self.deck.deal_random_card())
                self.board.append(self.deck.deal_random_card())
                self.board.append(self.deck.deal_random_card())
                print(f'BOARD: {self.board}')
                if rating(self.board + self.bot.cards) > rating(self.board + self.player.cards):
                    self.winner(self.player, end = True)
                elif rating(self.board + self.bot.cards) < rating(self.board + self.player.cards):
                    self.winner(self.bot, end = True)
                else:
                    self.tie()
            if game_state == 'Flop':
                self.board.append(self.deck.deal_random_card())
                self.board.append(self.deck.deal_random_card())
                print(f'BOARD: {self.board}')
                if rating(self.board + self.bot.cards) > rating(self.board + self.player.cards):
                    self.winner(self.player, end = True)
                elif rating(self.board + self.bot.cards) < rating(self.board + self.player.cards):
                    self.winner(self.bot, end = True)
                else:
                    self.tie()
            if game_state == 'Turn':
                self.board.append(self.deck.deal_random_card())
                print(f'BOARD: {self.board}')
                if rating(self.board + self.bot.cards) > rating(self.board + self.player.cards):
                    self.winner(self.player, end = True)
                elif rating(self.board + self.bot.cards) < rating(self.board + self.player.cards):
                    self.winner(self.bot, end = True)
                else:
                    self.tie()

            if game_state == 'River':
                print(f'BOARD: {self.board}')
                if rating(self.board + self.bot.cards) > rating(self.board + self.player.cards):
                    self.winner(self.player, end = True)
                elif rating(self.board + self.bot.cards) < rating(self.board + self.player.cards):
                    self.winner(self.bot, end = True)
                else:
                    self.tie()


    def tie(self):
        tie_chips = self.pot_size/2
        self.bot.chips += tie_chips
        self.player.chips += tie_chips
        print('TIE OCCURED')
        print(f'Your chips: {self.player.chips}')
        print(f'Bot Chips: {self.bot.chips}')
        self.reset_round()

    #When this method is called, the table deals the next cards based on the current position of the game
    def next_action(self, first_act, second_act):
        if len(self.board) == 0:
            self.game_state = 'Flop'
            self.board.append(self.deck.deal_random_card())
            self.board.append(self.deck.deal_random_card())
            self.board.append(self.deck.deal_random_card())
            print(f'BOARD: {self.board}')
            print(f'POT: {self.pot_size}')
            self.reset_raise()
            if first_act == self.player:
                self.player_betting()
            else:
                self.bot_betting()
        if len(self.board) == 3:
            self.game_state = 'Turn'
            self.board.append(self.deck.deal_random_card())
            print(f'BOARD: {self.board}')
            print(f'POT: {self.pot_size}')
            self.reset_raise()
            if first_act == self.player:
                self.player_betting()
            else:
                self.bot_betting()

        if len(self.board) == 4:
            self.game_state = 'River'
            self.board.append(self.deck.deal_random_card())
            print(f'BOARD: {self.board}')
            print(f'POT: {self.pot_size}')
            self.reset_raise()
            if first_act == self.player:
                self.player_betting()
            else:
                self.bot_betting()

            if len(self.board) == 5:
                print(f'BOARD: {self.board}')
                print(f'POT: {self.pot_size}')
                self.reset_raise()
                if rating(self.board + self.bot.cards) > rating(self.board + self.player.cards):
                    self.winner(self.player)
                elif rating(self.board + self.bot.cards) < rating(self.board + self.player.cards):
                    self.winner(self.bot)
                else:
                    self.tie()
                #When round end occurs we start the entire process from scratch

    #This method adds the cards back into the deck, then shuffles, then calls deal_cards to start a new round
    def reset_round(self):
        print('STARTING NEW ROUND...')
        bot_cards = input(f'DO YOU WANT TO SEE THE BOT CARDS, Y OR N')
        if bot_cards == 'Y':
            print(f'BOT CARDS: {self.bot.cards}')

        self.deck.add_cards(self.board)
        self.deck.add_cards(self.bot.cards)
        self.deck.add_cards(self.player.cards)
        self.board.clear()
        self.player.cards.clear()
        self.bot.cards.clear()
        self.deck.shuffle_deck()
        self.game_state = 'Pre-Flop'
        self.pot_size = 0
        self.reset_raise()

        self.deal_cards()
        self.new_position()
    #THIS WILL NOT STAY, using just for test cases
    def print_action(self, action, player):
        current = ''
        if player == self.bot:
            current2 = self.player
            current = 'Bot'
        else:
            current2 = self.bot
            current = 'Player'
        println = f' current chips: {self.player.chips}, bot chips: {self.bot.chips}, pot size:{self.pot_size}, player cards {self.player.cards}'
        if action == 'Raise':
            print(f'{current} raised -- {player.raise_amount}\n{player.raise_amount - current2.raise_total} to call\n' + println)
        if action == 'Call':
            print(f'{current} called\n' + println)
        if action == 'Check':
            print(f'{current} checked\n' + println)
        if action == 'Fold':
            print(f'{current} folded\n' + println)



    def reset_raise(self):
        self.bot.raise_amount = 0
        self.bot.raise_total = 0
        self.player.raise_amount = 0
        self.player.raise_total = 0


