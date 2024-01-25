#This method keeps track of the cards inside of the deck, needed for equity
import random
class Deck:
    def __init__(self):
        self.deck = []
        suites = ["s", "h", "d", "c"]
        for suite in suites:
            for i in range(2, 15):
                if i == 14:
                    i = 'A'
                if i == 13:
                    i = 'K'
                if i == 12:
                    i = 'Q'
                if i == 11:
                    i = 'J'
                if i == 10:
                    i = 'T'
                self.deck.append(str(i) + suite)
    #Takes a list of cards and either adds or removes to the deck
    def remove_cards(self,  cards):
        if type(cards) != list:
            cards = cards.split(' ')
        for i in cards:
            self.deck.remove(i)
        return self.deck

    def add_cards(self, cards):
        if type(cards) != list:
            cards = cards.split(' ')
        for i in cards:
            self.deck.append(i)

        return self.deck

    def  deal_random_card(self):

        x = random.choice(self.deck)
        self.deck.remove(x)
        return x
    def shuffle_deck(self):
        random.shuffle(self.deck)


    def is_in_deck(self, card):
        new_deck = set(self.deck)
        if card in new_deck:
            return True
        else:
            return False
    #Method for dealing with flush cards, gets a card of equal value that is in the deck
    def get_equal_value_card(self, card):
        for i in self.deck:
            if i[0] == card[0] and i[1] != card[1]:
                return i
        return card








if __name__ == '__main__':
    deck = Deck()


    deck.remove_cards('Ah')
    print('divide')
    for i in deck.deck:
        print(i)
    print(len(deck.deck))
    print(deck.is_in_deck('Kh'))
    print(deck.get_equal_value_card('Kh'))