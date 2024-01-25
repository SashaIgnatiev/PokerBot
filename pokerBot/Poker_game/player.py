class Player:
    def __init__(self):
        self.chips = 3000
        self.cards = []
        self.position = None
        self.raise_amount = 0
        self.bigBlind = False
        self.raise_total = 0
    def recieve_cards(self, card):
        self.cards.append(card)

    def action(self, preflop = False, Raise = False):
        if preflop == True and self.bigBlind == False:

            print(f'Pre-Flop you are small blind/dealer \n Do you \n Call(50): Ca \n Raise: R \n Fold  F')
        elif preflop == True and self.bigBlind == True:
            print(f'Bot called, do you check \n raise: R\ncheck: Ch\nfold: F')

        else:
            print('Check: Ch or Call: Ca')
            print('Raise press: R')
            print('Fold press: F')
            print(f'Current Chips: {self.chips}')

        action = input()
        if action == 'Ca' or action == 'ca':
            return 'Call'

        elif action == 'Ch' or action == 'ch':
            return 'Check'

        elif action == 'R' or action == 'r':
            print('Enter amount to raise')
            raise_amount = int(input())

            self.raise_amount = raise_amount

            if raise_amount >= self.chips:
                return 'All_In'

            print(f'Current_chips: {self.chips}')
            print(f'Raise Amount: {raise_amount}')
            self.raise_total += raise_amount
            return 'Raise'


        elif action == 'F' or action == 'f':
            return 'Fold'

    def action_all_in(self):
        print(f'PokerBot went all in')
        print(f'Call his all in or Fold: C or F respectively')
        action = input()
        if action == 'c' or action == 'C':
            return 'Call'
        if action == 'f' or action == 'F':
            return 'Fold'
