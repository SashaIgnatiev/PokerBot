class Card:
    def __init__(self, suits, value):
        self.suits = suits #string 'red' or 'black'
        self.value = value #int 2-14, Jack = 11, Queen = 12, King = 13, Ace = 14

    def is_in_deck(self):
        return False


    def to_String(self):
        return self.suits + ": " + str(self.value)



