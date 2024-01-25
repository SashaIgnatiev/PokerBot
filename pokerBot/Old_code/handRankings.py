from Old_code.deck import Deck


#Program that takes 7 cards and outputs a number ranking
def rating(hand):

    straight = []
    newHand = sorted(hand, key = lambda x : x.value)
    # Checking for straight and straight flush
    straight_checker = False
    if newHand[0].value == 2 and newHand[-1].value == 14:
        straight.append(newHand[-1])
        straight.append(newHand[0])

    else:
        straight.append(newHand[0])
    for i in range(1, len(newHand)):
        if newHand[i].value == newHand[i - 1].value + 1:
            straight.append(newHand[i])
        elif newHand[i].value == newHand[i - 1]:
            continue

        elif len(straight) < 5:
            straight = []
            straight.append(newHand[i])
    if len(straight) >= 5:
        if straight_flush_checker(straight) != None:

            return straight_flush(straight_flush_checker(straight))
        else:
            straight_checker = True
    #Checking for quads, Keeping track of : trips, 2-pair and pair
    fourOfKind = {}

    for i in newHand:
        if i.value in fourOfKind:
            fourOfKind[i.value] += 1
            if fourOfKind[i.value] == 4 and i.value == newHand[-1].value:
                return (10000 * i.value) + (.0001 * newHand[-5].value)
            elif fourOfKind[i.value] == 4 and i != newHand[-1].value:
                return (10000 * i.value) + (.0001 * newHand[-1].value)

        else:
            fourOfKind[i.value] = 1
    for i,x in fourOfKind.items():
        print(f'{i} : {x}')

    #If we have gotten this far, we can check for full house

    #Check once for highest trips
    high_card = 0
    check1 = False
    check2 = False
    second_card = 0
    for i, x in fourOfKind.items():
        if x == 3 and i > high_card:
            check1 = True
            high_card = i
    # Check Again for lower trips or pair
    for i, x in fourOfKind.items():
        if (x == 3 or x == 2) and (i > second_card )and (i != high_card):
            check2 = True
            second_card = i
    if check1 == True and check2 == True:
        return 1500 + (high_card * 1) + (second_card * .005)


    flush = dict()

    #checking for flush
    high_card = 0
    flush2 = []
    flushCheck = False
    suit = None
    for i in newHand:
        if i.suits in flush:
            flush[i.suits] += 1
            if flush[i.suits] >= 5:
                suit = i.suits
                flushCheck = True

        else:
            flush[i.suits] = 1
    for i in newHand:
        if i.suits == suit:
            flush2.append(i)

    if flushCheck == True:
        high_card = flush2[-1].value
        return 100 * high_card
    #Checking for Straight
    if straight_checker == True:
        return 10 * straight[-1].value
    #Checking for trips
    trips_eval = 0
    max_val = 0
    max_val2 = 0

    for i, x in fourOfKind.items():
        if x == 3:
            trips_eval = 1 * i

        if i > max_val and x != 3:
            max_val2 = max_val
            max_val = i
    if trips_eval > 0:
        return trips_eval + (.0001 * max_val) + (.0001 * max_val2)
    #Checking for 2 pair
    max_val = 0
    max_val2 = 0
    max_val3 = 0
    for i, x in fourOfKind.items():
        if x == 2:
            if i > max_val:
                max_val2 = max_val
                max_val = i
        #FIXME
        if x == 1 or (x == 2 and (0 < i < max_val and 0 < i < max_val2)):
            if i > max_val3:
                max_val3 = i
        #FIXME
    if max_val > 0 and max_val2 > 0:
        return .15 + (.005 * max_val) + (.005 * max_val2) + (.0001 * max_val3)

    #FML checking for pair ALMSOT DNE NI-
    max_val = 0
    max_val2 = 0
    max_val3 = 0
    pair_check = False
    pair_value = 0
    for i,x  in fourOfKind.items():

        if x == 2:
            pair_value = i * .005
            pair_check = True
        elif i > max_val:
            max_val3 = max_val2
            max_val2 = max_val
            max_val = i
    if pair_check == True:
        return pair_value + (max_val * .0001) + (max_val2 * .0001) + (max_val3 * .0001)




    return (newHand[-1].value + newHand[-2].value + newHand[-3].value + newHand[-4].value + newHand[-5].value) * .0001
def straight_flush_checker(straight):
    newStraight = []

    if (straight[-1].value == 14) and (straight[-1].suits == straight[0].suits):
        count = 2
        newStraight.append(straight[-1])
        newStraight.append(straight[0])
    else:
        newStraight.append(straight[0])
        count = 1
    checker = False
    suit = straight[0].suits
    for i in range(1, len(straight)):
        if straight[i].suits == suit and straight[i].value == straight[i - 1].value + 1:
            count += 1
            newStraight.append(straight[i])
        elif checker == True:
            continue
        else:
            suit = straight[i].suits
            newStraight = []
            count = 1
        if count >= 5:
            suit = straight[i].suits
            checker = True
    if checker == False:
        return None
    if checker == True:
        return newStraight
def straight_flush(straight_flush):
    return 100000 * straight_flush[-1].value

if __name__ =="__main__":
    deck = Deck()
    x = list(deck.deal_cards(7))
    for i in x:
        print(i.to_String())
    print(rating(x))