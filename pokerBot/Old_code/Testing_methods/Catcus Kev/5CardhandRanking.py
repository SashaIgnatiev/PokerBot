import random
import arrays
# Poker hand evaluator
#
# Kevin L. Suffecool
# kevin@suffe.cool
#

# This routine initializes the deck. A deck of cards is
# simply an integer array of length 52 (no jokers). This
# array is populated with each card, using the following
# scheme:
#
# An integer is made up of four bytes. The high-order
# bytes are used to hold the rank bit pattern, whereas
# the low-order bytes hold the suit/rank/prime value
# of the card.
#
# +--------+--------+--------+--------+
# |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
# +--------+--------+--------+--------+
#
# p = prime number of rank (deuce=2,trey=3,four=5,five=7,...,ace=41)
# r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
# cdhs = suit of card
# b = bit turned on depending on rank of card
#
# As an example, the Five of Hearts would be represented as
#
# +--------+--------+--------+--------+
# |00000000|00001000|00100111|00000111| = 0x00082707
# +--------+--------+--------+--------+
#
# and the Queen of Clubs would be represented as
#
# +--------+--------+--------+--------+
# |00000100|00000000|10001010|00011111| = 0x04008A1F
# +--------+--------+--------+--------+

def init_deck(deck):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    suit = 0x8000
    n = 0
    for i in range(4):
        for j in range(13):
            deck[n] = primes[j] | (j << 8) | suit | (1 << (16+j))
            n += 1
        suit >>= 1

# This routine will search a deck for a specific card
# (specified by rank/suit), and return the INDEX giving
# the position of the found card. If it is not found,
# then it returns -1

def find_card(rank, suit, deck):
    for i in range(52):
        c = deck[i]
        if (c & suit) and ((arrays.RANK(c) >> 8) & 0xF) == rank:
            return i
    return -1

# This routine takes a deck and randomly mixes up
# the order of the cards.

def shuffle_deck(deck):
    temp = deck.copy()
    for i in range(52):
        n = random.randint(0, 51)
        while temp[n] == 0:
            n = random.randint(0, 51)
        deck[i] = temp[n]
        temp[n] = 0

# This routine prints the given hand as a string; e.g.
# Ac 4d 7c Jh 2s

def print_hand(hand, n):
    rank = "23456789TJQKA"
    for i in range(n):
        r = (hand[i] >> 8) & 0xF
        if hand[i] & 0x8000:
            suit = 'c'
        elif hand[i] & 0x4000:
            suit = 'd'
        elif hand[i] & 0x2000:
            suit = 'h'
        else:
            suit = 's'
        print(rank[r] + suit, end=' ')
    print()

# Returns the hand rank of the given equivalence class value.
# Note: the parameter "val" should be in the range of 1-7462.

def hand_rank(val):
    if val > 6185:
        return "HIGH_CARD"        # 1277 high card
    if val > 3325:
        return "ONE_PAIR"         # 2860 one pair
    if val > 2467:
        return "TWO_PAIR"         #  858 two pair
    if val > 1609:
        return "THREE_OF_A_KIND"  #  858 three-kind
    if val > 1599:
        return "STRAIGHT"         #   10 straights
    if val > 322:
        return "FLUSH"            # 1277 flushes
    if val > 166:
        return "FULL_HOUSE"       #  156 full house
    if val > 10:
        return "FOUR_OF_A_KIND"   #  156 four-kind
    return "STRAIGHT_FLUSH"       #   10 straight-flushes

# Perform a perfect hash lookup (courtesy of Paul Senzee).

def find_fast(u):
    u += 0xe91aaa35
    u ^= u >> 16
    u += u << 8
    u ^= u >> 4
    b  = (u >> 8) & 0x1ff
    a  = (u + (u << 2)) >> 19
    r  = a ^ hash_adjust[b]
    return r

def eval_5cards(c1, c2, c3, c4, c5):
    q = (c1 | c2 | c3 | c4 | c5) >> 16
    # This checks for Flushes and Straight Flushes
    if c1 & c2 & c3 & c4 & c5 & 0xf000:
        return flushes[q]
    # This checks for Straights and High Card hands
    if (s := unique5[q]):
        return s
    # This performs a perfect-hash lookup for remaining hands
    q = (c1 & 0xff) * (c2 & 0xff) * (c3 & 0xff) * (c4 & 0xff) * (c5 & 0xff)
    return hash_values[find_fast(q)]

def eval_5hand(hand):
    c1, c2, c3, c4, c5 = hand[:5]
    return eval_5cards(c1, c2, c3, c4, c5)

# This is a non-optimized method of determining the
# best five-card hand possible out of seven cards.
# I am working on a faster algorithm.

def eval_7hand(hand):
    subhand = [0] * 5
    best = 9999
    for i in range(21):
        for j in range(5):
            subhand[j] = hand[perm7[i][j]]
        q = eval_5hand(subhand)
        if q < best:
            best = q
    return best

deck = [0] * 52
init_deck(deck)
shuffle_deck(deck)
print_hand(deck, 5)


