import os

class Tracker:
    def __init__(self, player_name):
        self.player_name = player_name
        file = f'./poker_hand_history/{player_name}.txt'
        if os.path.isfile(file) == True:
            self.f = open(file, 'a')
            self.f.write('----------------NEW GAME WITH SAME OPPONENT----------------')
        else:
            self.f.write('----------------NEW GAME----------------')
            self.f = open(file, 'a')

        self.f.write('')
        self.hand_counter = 0


    def log_game_state(self, game_state):
        self.f.write(game_state)


    def log_action(self, action, current ,Raise = 0):
        if Raise > 0:
            write = f'{current} {action} {Raise} chips'
            self.f.write(write)
        else:
            write = f'{current} {action}'
            self.f.write(write)


    def log_current_hand(self, our_cards):
        self.hand_counter += 1
        write = f'------ HAND {self.hand_counter} ------'
        self.f.write(write)
        write = f'Our cards: {our_cards}'
        self.f.write(write)


    def log_current_board(self, board, our_stack, opp_stack):
        write = f'cards on board: {board}'
        self.f.write(write)
        write = f'Our current chips: {our_stack}; Opponent current chips: {opp_stack}'
        self.f.write(write)

    def round_winner(self, result):
        if result == 'TIE':
            self.f.write('Round is a tie, players split the pot')

        else:
            write = f'{result} wins the hand'
            self.f.write(write)



    def game_winner(self, winner, cards = None):
        write = f'{winner} Wins the game!'
        self.f.write(write)

        if cards != None:
            write = f'Player cards: {cards}'
            self.f.write(write)

        self.f.close()

if __name__ == '__main__':
    file = open('./poker_hand_history/test3.txt', 'x')








