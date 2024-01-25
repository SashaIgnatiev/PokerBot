from handRankings import rating
from deck import Deck

x = 184528125
deck = Deck()
#Payer 1: Ace of spades, king of spades
player1 = deck.deal_cards_in_order(2)
#Player 2: Queen of spades, jack of spades
player2 = deck.deal_cards_in_order(2)
table = deck.deal_cards_in_order(5)
win_or_lose = {'As/Ks' : 0, 'Qs/Js': 0, 'tie' : 0}

def compare(player1, player2, table):
    player1_rating = rating(table + player1)
    player2_rating = rating(table + player2)
    if player1_rating > player2_rating:
        win_or_lose['player1'] += 1
    elif player1_rating < player2_rating:
        win_or_lose['player2'] += 1
    else:
        win_or_lose['tie'] += 1
for i in deck.deck:
    print(i.to_String())

for i in range(len(deck.deck)):
    for i in range(len(deck.deck)):
        for i in range(len(deck.deck)):
            for i in range(len(deck.deck)):
                for i in range(len(deck.deck)):
                    compare(player1, player2, table)
                    placeholder = table[-1]
                    table[-1] = deck.deck[-1]
                    deck.deck.insert(0, placeholder)
                    deck.deck.pop()
                    x -= 1
                compare(player1, player2, table)
                placeholder = table[-2]
                table[-2] = deck.deck[-1]
                deck.deck.insert(0, placeholder)
                deck.deck.pop()
                x-= 1
            compare(player1, player2, table)
            placeholder = table[-3]
            table[-3] = deck.deck[-1]
            deck.deck.insert(0, placeholder)
            deck.deck.pop()
            x-= 1
        compare(player1, player2, table)
        placeholder = table[-4]
        table[-4] = deck.deck[-1]
        deck.deck.insert(0, placeholder)
        deck.deck.pop()
        x -= 1
    compare(player1, player2, table)
    placeholder = table[-5]
    table[-5] = deck.deck[-1]
    deck.deck.insert(0, placeholder)
    deck.deck.pop()
    x -= 1
    print(x)

c = conn.cursor()
c.execute(''' CREATE TABLE test1
            As/Ks real, Qs/Js real, tie real''')
c.execute(''' INSERT INTO test1 VALUES (:As/Ks, :Qs/Js :tie)''', win_or_lose)



print(win_or_lose)
