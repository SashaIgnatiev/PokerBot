from Old_code.cards import Card
import random
class Deck:
    def __init__(self):
        self.deck = []
        suites = ["spades", "hearts", "diamonds", "clubs"]
        for suite in suites:
            for i in range(2, 15):
                self.deck.append(Card(suite, i))
   #Method to test use of deck
    def deck_to_string(self):
        for i in self.deck:
            print(i.to_String())

    def deal_cards(self, num):
        table = set()
        lis = list(self.deck)
        #Adds cards to the table, removes cards from the deck
        for i in range(num):
            x = random.choice(lis)
            table.add(x)
            self.deck.remove(x)
            lis.remove(x)
        #Print method to test if the deal cards works
        #print(Table.set_to_string(table))

        return table
    def deal_cards_in_order(self, num):
        lis = []
        for i in range(num):
            lis.append(self.deck[-1])
            self.deck.pop(-1)
        return lis
if __name__ == '__main__':
    deck = Deck()
    print(deck.deck_to_string())
    print(len(deck.deck))
