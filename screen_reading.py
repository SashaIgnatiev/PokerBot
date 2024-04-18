import copy
import os
import time

import pyautogui
from PIL import ImageGrab, ImageOps
import numpy as np
import cv2 as cv
import pytesseract
import pygetwindow as gw
import math
from enum import Enum
from pokerBot.Poker_bot_desicions.poker_bot import PokerBot
from pokerBot import mouse_movements
import re

# Fields

# name of the window

# name = 'Screen_Shot_2023-12-20_at_14.23.03.webp'
# ensuring that pytesseract is in the path (idk why its not automatically, this just works)
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'


class State(Enum):
    PREFLOP = "Pre-Flop"
    FLOP = "Flop"
    TURN = "Turn"
    RIVER = "River"

class Card:
    '''class related to storing information about the card'''

    def __init__(self):
        self.im = []
        self.suit = ""
        self.rank = ""
        self.suit_im = []
        self.rank_im = []
        self.processed = False

class Sample:
    '''class related to storing the sample images used for comparison'''

    def __int__(self):
        self.name = ""
        self.img = []

def binerize(img, val):
    '''helper method for turning a grayscale image into a black and white image

    :param img - array of the image you want to turn black and white
    :param val - threshold at which you switch between black and white
    :return normed - array of the black and white image

    '''
    normed = copy.copy(img)
    normed[img < val] = 0
    normed[img > val] = 255
    return normed

def get_window_name():
    names = gw.getAllTitles()
    for name in names:
        if name[0:10] == "PokerStars":
            return name
    raise Exception("Couldn't find the Pokerstars window :(")

def grab_poker_window(window_name):
    ''' method that takes the given window, and return a 2-D array of the grayscales image of the window

     :param window_name - name of the window that you want to pass through, obtained from pygetwindow module
     :return img - the array representing the grayscaled image

     '''

    # setting the boundaries of the image to be grabbed, setting the parameters of the screenshot used by ImageGrab
    x, y, w, h = gw.getWindowGeometry(window_name)
    bbox = (int(x), int(y), int(x + w), int(y + h))

    # grabbing the image, greyscaling it, and returning it as a numpy array
    img = ImageGrab.grab(bbox)
    col = np.asarray(img)

    img2 = ImageOps.grayscale(img)
    img2 = np.array(img2)

    return img2, w, h, col, x, y

def get_box(im, box, pos, new_w, new_h, old_w = 952, old_h = 736):
    '''helper method for obtaining a certain part of an image as a new matrix
    '''

    box_w = math.ceil((box[0]/old_w) * new_w)
    box_h = math.ceil((box[1]/old_h) * new_h)


    pos_w = math.ceil((pos[0]/old_w) * new_w)
    pos_h = math.ceil((pos[1]/old_h) * new_h)

    output = im[pos_w: pos_w + box_w, pos_h: pos_h + box_h]
    return output

def get_box2(im, box, pos, new_w, new_h, old_w = 952, old_h = 736):
    '''helper method for obtaining a certain part of an image as a new matrix
    '''

    box_w = box[0]
    box_h = box[1]

    pos_w = math.ceil((pos[0]/old_w) * new_w)
    pos_h = math.ceil((pos[1]/old_h) * new_h)

    output = im[pos_w: pos_w + box_w, pos_h: pos_h + box_h]
    return output

def isolate_my_cards(img, w, h):
    '''method for retrieving the cards that are dealt to me'''
    # the coordinates for my two cards are hardcoded
    output = get_box(img, (43, 119), (440, 445), new_w = w, new_h = h)
    return output

def process_my_cards(input):
    # gets the values from my two cards

    new_x = np.shape(input)[0]
    new_y = np.shape(input)[1]


    first_card = Card()
    second_card = Card()

    # grabbing the first rank
    target = get_box2(input, (24, 21), (0, 0), old_w = 43, old_h=119, new_w=new_x, new_h=new_y)
    img = isolate_card(target)
    first_card.rank_im = img

    # grabbing the first suite
    target = get_box2(input, (11, 17), (24, 1), old_w=43, old_h=119, new_w=new_x, new_h=new_y)
    img = isolate_card(target, fsuite = True, bin_val= 100)
    first_card.suit_im = img

    # grabbing the second rank
    target = get_box2(input, (24, 21), (0, 60), old_w=43, old_h=119, new_w=new_x, new_h=new_y)
    img = isolate_card(target)
    second_card.rank_im = img

    # grabbing the second suite
    target = get_box2(input, (11, 21), (24, 60), old_w=43, old_h=119, new_w=new_x, new_h=new_y)
    img = isolate_card(target, fsuite = True, bin_val= 100)
    second_card.suit_im = img

    first_card.im = input

    return first_card, second_card

def isolate_card(img, bin_val=150, thresh_val=127, cont=1, fsuite=False):
    first_rank = binerize(img, bin_val)

    if fsuite == True:
        length = np.shape(first_rank)[1]
        new_row = np.tile(255, (1, length))
        first_rank = np.vstack((first_rank, new_row))
        first_rank = np.vstack((new_row, first_rank))
        first_rank = np.uint8(first_rank)
        first_rank[first_rank == -1] = 151


    ret, thresh = cv.threshold(first_rank, thresh_val, 255, 0)
    contours, heirarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    index_sort = sorted(range(len(contours)), key=lambda i: cv.contourArea(contours[i]), reverse=True)
    try:
        contour = contours[index_sort[cont]]
    except:
        contour = contours[index_sort[0]]
    x, y, w, h = cv.boundingRect(contour)
    new_card = first_rank[y:y + h, x:x + w]

    res_card = cv.resize(new_card, (20, 30), 0, 0)
    res_bin = binerize(res_card, bin_val)

    return res_bin

def process_table(img, w, h):
    card_size = 1400

    table1 = Card()
    table2 = Card()
    table3 = Card()
    table4 = Card()
    table5 = Card()

    table = [table1, table2, table3, table4, table5]

    # isolating the table (yeah its hardcoded, thats a problem for future me
    output = get_box(img, (50, 312), (246, 343), new_w = w, new_h = h)
    first_rank = binerize(output, 150)
    ret, thresh = cv.threshold(first_rank, 127, 255, 0)
    contours, heirarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    index_sort = sorted(range(len(contours)), key=lambda i: cv.contourArea(contours[i]), reverse=True)

    if index_sort == []:
        return ()

    for i in range(0, 5):
        contour = contours[index_sort[i]]
        x, y, w, h = cv.boundingRect(contour)
        new_card = first_rank[y:y + h, x:x + w]
        dims = np.shape(new_card)
        area = dims[0] * dims[1]
        if area > card_size:
            table[i].im = new_card
            rank, suite = isolate_info(table[i].im)
            rank = isolate_card(rank)
            suite = isolate_card(suite)
            table[i].rank_im = rank
            table[i].suit_im = suite
            table[i].processed = True
        else:
            continue

    export = []
    for x in table:
        if x.processed == True:
            export.append(x)

    return export

def isolate_info(card):
    w = np.shape(card)[0]
    h = np.shape(card)[1]
    #try 22
    rank = get_box(card, (24, 21), (0, 0), old_w = 49, old_h = 58, new_w = w, new_h = h)
    suite = get_box(card, (26, 23), (22, 0), old_w = 49, old_h = 58, new_w = w, new_h = h)

    return rank, suite

def load_samples():
    '''method that boots up at the start of the program to load the sample images'''

    os.chdir("sample_images3")
    suite_names = ["spade", "heart", "club", "diamond", "diamond_first", "club_first", "heart_first", "spade_first"]
    rank_names = ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack",
                  "queen", "king", "ace", "spade_first2"]

    ranks = []
    suits = []

    # loading the list of suits
    for name in suite_names:
        try:
            img = cv.imread(name + ".png", 0)
            output = Sample()
            output.img = img
            output.name = name
            if output.img is not None:
                suits.append(output)
        except Exception as e:
            raise e

    # loading the list of ranks
    for name in rank_names:
        try:
            img = cv.imread(name + ".png", 0)
            output = Sample()
            output.img = img
            output.name = name
            if output.img is not None:
                ranks.append(output)
        except Exception as e:
            raise e

    os.chdir('../')
    return ranks, suits

def compare(target, sample_r, sample_s):
    sample_ranks = sample_r
    sample_suites = sample_s
    both = sample_suites + sample_ranks
    # both_shape = []

    # first sort by proper shape
    # for tar in both:
    #     if np.shape(tar.img) == np.shape(target):
    #         both_shape.append(tar)

    # fail_counter = 0

    lead_val = np.mean(np.abs(target - both[0].img))
    lead_name = ""
    # except:
    #     lead_val = float(1000000)
    #     lead_name = ""

    for tar in both:
        name = tar.name
        val = np.mean(np.abs(target - tar.img))
        if val <= lead_val:
            lead_val = val
            lead_name = name
        else:
            continue

    return lead_name

def invert(image):
    output = copy.deepcopy(image)
    output[image < 100] = 255
    output[image > 100] = 0
    return output

def grab_pot(imgray):
    input = get_box(imgray, (25, 200), (190, 320), 952, 736)
    input2 = binerize(input, val = 150)
    input3 = invert(input2)
    output = ""
    text = pytesseract.image_to_string(input3)
    for a in range(len(text)):
        b = text[a:a + 5]
        if b == "Pot: ":
            for i in range(10):
                u = text[a + 5 + i]
                if u == "\n":
                    output = text[a + 5:a + 5 + i]
                    break
    #first step to debugging is to uncomment this line, if grab pot ever stop working properly
    #print(f"Output: {output}")
    try:
        return string_to_int(output)
    except:
        return 1

def get_dealer_pos(imcolor, w, h):
    area = get_box(imcolor, (330, 510), (100, 150), w, h)
    hsv = cv.cvtColor(area, cv.COLOR_BGR2HSV)
    lower_red = np.array([110, 50, 50])
    upper_red = np.array([130, 255, 255])
    mask = cv.inRange(hsv, lower_red, upper_red)
    ret, thresh = cv.threshold(mask, 150, 255, 0)
    contours, heirarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    index_sort = sorted(range(len(contours)), key=lambda i: cv.contourArea(contours[i]), reverse=True)

    contour = contours[index_sort[0]]
    x, y, w, h = cv.boundingRect(contour)
    #150, is the tested and hardcoded 'middle' of the screen. Thats why that value is there
    if y > 150:
        return 1
    else:
        return 0

def get_my_chips(imgray, w, h):
    my_chips_box = get_box(imgray, (25, 100), (510, 500), new_w=w, new_h=h)
    # cv.imshow("yes", my_chips_box)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    text = pytesseract.image_to_string(my_chips_box)
    print(f"my chips raw = {text}")
    try:
        return string_to_int(text)
    except:
        return 0

def get_opponent_chips(imgray, w, h):

    opponent_chips_box = get_box(imgray, (25, 100), (120, 440), new_w=w, new_h=h)
    opp_box_inverted = invert(opponent_chips_box)
    #collect_img("image", opp_box_inverted)
    text = pytesseract.image_to_string(opponent_chips_box)
    try:
        return string_to_int(text)
    except:
        return 0

def update_list_of_cards(cards, list_of_cards, old_state):
    update = False

    if len(cards) == 0:
        state = State.PREFLOP
    if len(cards) == 1 or len(cards) == 2:
        raise AssertionError("There cannot be one or two cards on the table :(")
    if len(cards) == 3:
        deck_card1 = cards[0]
        list_of_cards.append(deck_card1)
        deck_card2 = cards[1]
        list_of_cards.append(deck_card2)
        deck_card3 = cards[2]
        list_of_cards.append(deck_card3)
        state = State.FLOP
    if len(cards) == 4:
        deck_card1 = cards[0]
        list_of_cards.append(deck_card1)
        deck_card2 = cards[1]
        list_of_cards.append(deck_card2)
        deck_card3 = cards[2]
        list_of_cards.append(deck_card3)
        deck_card4 = cards[3]
        list_of_cards.append(deck_card4)
        state = State.TURN
    if len(cards) == 5:
        deck_card1 = cards[0]
        list_of_cards.append(deck_card1)
        deck_card2 = cards[1]
        list_of_cards.append(deck_card2)
        deck_card3 = cards[2]
        list_of_cards.append(deck_card3)
        deck_card4 = cards[3]
        list_of_cards.append(deck_card4)
        deck_card5 = cards[4]
        list_of_cards.append(deck_card5)
        state = State.RIVER


    if state != old_state:
        update = True

    return list_of_cards, state, update

def get_opponent_bet(imgray, old_imgray, w, h):

    old_chips = get_opponent_chips(old_imgray, w, h)
    new_chips = get_opponent_chips(imgray, w, h)
    bet = old_chips - new_chips

    return bet

def action_control(action):
    pass

def get_opp_name(imgray, w, h):
    name_box = get_box(imgray, (30, 130), (100, 420), new_w=w, new_h=h)
    text = pytesseract.image_to_string(name_box)
    return text

def compare_card(card, sample_ranks, sample_suits):
    # comparing rank
    rank_im = card.rank_im
    rank_name = compare(rank_im, sample_ranks, sample_suits)
    card.rank = rank_name

    # comparing suit
    suit_im = card.suit_im
    suit_name = compare(suit_im, sample_ranks, sample_suits)
    card.suit = suit_name

def is_our_turn (imcolor, w, h):
    check_button = get_box(imcolor, (50, 150), (625, 680), new_w=w, new_h=h)
    hsv = cv.cvtColor(check_button, cv.COLOR_BGR2HSV)
    lower_red = np.array([110, 50, 50])
    upper_red = np.array([130, 255, 255])
    mask = cv.inRange(hsv, lower_red, upper_red)

    if np.mean(mask) < 100:
        return False
    else:
        return True

def card_converter(card):
    suite_names = ["spade", "heart", "club", "diamond", "diamond_first", "club_first", "heart_first", "spade_first"]
    rank_names = ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack",
                  "queen", "king", "ace", "spade_first2"]

    help_dict = {
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'ten': 'T',
        'jack': 'J',
        'queen': 'Q',
        'king' : 'K',
        'ace'  : 'A'
    }

    for key in help_dict:
        if card.rank == key:
            rank = help_dict[key]
    suit = card.suit[0]

    return (rank + suit)

def string_to_int(text):
    string_final = ""
    for letter in text:
        try:
            val = int(letter)
            string_final = string_final + letter
        except:
            continue
    return int(string_final)

def adjust_win(x, y, w, h):
    corner_x = x+w-2
    corner_y = y+h-2

    x_pos = pyautogui.position()[0]
    y_pos = pyautogui.position()[1]
    pyautogui.moveTo(corner_x, corner_y, .25)
    pyautogui.dragTo(x + 841, y + 608, .25, button='left')# move the mouse to 100, 200, then release the right button up.

def reset(pokerBot):
    bet = 0
    pokerBot.raise_total = 0
    pokerBot.raise_amount = 0
    return bet

def collect_img(im_name, image):
    cv.imwrite(f"images_we_want/{im_name}.png", image)

def main():
    # loading sample images
    sample_ranks, sample_suits = load_samples()

    # grabbing a grayscale image of the poker window
    name = get_window_name()
    old_imgray, w, h, imcolor, x, y = grab_poker_window(name)

    adjust_win(x, y, w, h)

    # grabbing pot, opponent name
    opp_name = get_opp_name(old_imgray, w, h)

    chips = get_my_chips(old_imgray, w, h)

    # creaing a list of cards, initializing game state
    list_of_cards = []
    state = State.PREFLOP

    pokerBot = PokerBot(chips, 100)

    #impossible value for dealer pos, so that when the game starts, new game state is always achieved
    pos = 2
    old_dealer_pos = 3
    turn = False
    list_of_cards = []
    new_game = True
    bet_total = 0
    opp_chips = get_opponent_chips(old_imgray, w, h)

    while (1):

        #if it's not our turn
        if turn == False:

            #and grab a new picture
            imgray, w, h, imcolor, x, y = grab_poker_window(name)

            #get the dealer position, and update 2 variable that will be used to determine if the game state has been updated
            try:
                cards = process_table(imgray, w, h)
                list_of_cards, state2, update2 = update_list_of_cards(cards, list_of_cards, state)
                pos = get_dealer_pos(imcolor, w, h)
            except:
                pass
            # try:
            #     cards = process_my_cards(yes)
            # except:
            #     old_imgray = grab_poker_window(name)[0]

            #if the game state is being updated
            if update2 == True:
                #print("update")
                bet_total = reset(pokerBot)

                test = get_opponent_chips(imgray, w, h)

                turn = is_our_turn(imcolor, w, h)
                list_of_cards = []

            #if a new round is being started
            if old_dealer_pos != pos:
                print("newround")
                bet_total = reset(pokerBot)

                old_imgray = imgray

                if pos == 1:
                    bet_total = 100
                else:
                    bet_total = 0

                old_dealer_pos = pos
                turn = is_our_turn(imcolor, w, h)
                list_of_cards = []

            # if the opponent simply raises
            else:
                turn = is_our_turn(imcolor, w, h)
                list_of_cards = []

        else:

            # excracting my cards from the image
            imgray, w, h, imcolor, x, y = grab_poker_window(name)
            yes = isolate_my_cards(imgray, w, h)


            try:
                cards = process_my_cards(yes)
                my_card1 = cards[0]
                list_of_cards.append(my_card1)
                my_card2 = cards[1]
                list_of_cards.append(my_card2)
            except Exception as e:
                print("Coudn't locate my cards. Probably not on the table")

            # excracting the deck cards from the image
            cards = process_table(imgray, w, h)
            list_of_cards, state, update = update_list_of_cards(cards, list_of_cards, state)
            for card in list_of_cards:
                compare_card(card, sample_ranks, sample_suits)

            #processing the cards into pokerbot freindly formatt
            our_cards = list_of_cards[0:2]
            table_cards = list_of_cards[2:]
            our_cards_good = []
            table_cards_good = []
            for card in our_cards:
                our_cards_good.append(card_converter(card))
            for card in table_cards:
                table_cards_good.append(card_converter(card))

            #adjusting the parameters
            pokerBot.cards = our_cards_good
            pokerBot.chips = get_my_chips(imgray, w, h)
            pos = get_dealer_pos(imcolor, w, h)
            pot = grab_pot(imgray)

            if update == False: # and old_dealer_pos == pos:
                bet_total = bet_total + get_opponent_bet(imgray, old_imgray, w, h)

            bet = bet_total - pokerBot.raise_amount

            print(f"bet total: {bet_total}")

            #running the poker bot
            if get_dealer_pos(imcolor, w, h) == 0:
                action = pokerBot.action(pot, bet, bet_total, state.value, table_cards_good, pos , Raise = True)
            else:
                action = pokerBot.action(pot, bet, bet_total, state.value, table_cards_good, pos)

            #processing poker bot output
            if action == "Check":
                print("check")
                mouse_movements.click_button(563, 688, 544, 599, x, y)
            if action == "Call":
                print("call")
                mouse_movements.click_button(563, 688, 544, 599, x, y)
            if action == "Fold":
                print("fold")
                mouse_movements.click_button(422, 542, 544, 599, x, y)
            if action == "Raise":
                print("raise")
                print(f'BOT RAISE TOTAL: {pokerBot.raise_total}')
                print(f'CURRENT RAISE: {pokerBot.raise_amount}')
                raise_amount = pokerBot.raise_amount
               # print(f'RAISE AMOUNT2: {raise_amount}')
                mouse_movements.click_button(609, 612, 523, 531, x, y)
                mouse_movements.write_amount(raise_amount)
                mouse_movements.click_button(708, 828, 554, 599, x, y)
            if action == 'All_In':
                raise_amount = pokerBot.chips
                print('All_In')
                mouse_movements.click_button(609, 612, 523, 531, x, y)
                mouse_movements.write_amount(raise_amount)
                mouse_movements.click_button(708, 828, 554, 599, x, y)



            #reseting list of card, and grabbing old imgray
            list_of_cards = []
            turn_checker = grab_poker_window(name)[3]
            turn = is_our_turn(turn_checker, w, h)
            old_imgray = imgray


            #if the dealer position wasn't the same, the turn has ended, meaning that we continue with the same position
            if get_dealer_pos(imcolor, w, h) != old_dealer_pos:
                old_dealer_pos = pos

    # check_button = get_box(imgray, (50, 150), (625, 680), new_w=w, new_h=h)
    # raise_button = get_box(imgray, (50, 145), (625, 855), new_w=w, new_h=h)
    # fold_button =  get_box(imgray, (50, 145), (625, 510), new_w=w, new_h=h)
    # raise_amount = get_box(imgray, (20, 20), (590, 730), new_w=w, new_h=h)

if __name__ == "__main__":
    main()

'''
To do:
   * use the image with and length to grab the actual box, for any size of the image, instead of hardcoding the pixels
   * isolate the numbers and suites on my two cards
   * create a contour for the suites and rank to store in my card object
   * crop my images around them, and use the guys method to compare them, should be a method that works for any card,
     try to keep universal

'''

