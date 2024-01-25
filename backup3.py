import copy
import os
from PIL import ImageGrab, ImageOps
import numpy as np
import cv2 as cv
import pytesseract
import pygetwindow as gw
import math
from enum import Enum

# Fields

# name of the window

# name = 'Screen_Shot_2023-12-20_at_14.23.03.webp'
# ensuring that pytesseract is in the path (idk why its not automatically, this just works)
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'


class State(Enum):
    PREFLOP = 0
    FLOP = 3
    TURN = 4
    RIVER = 5

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

    return img2, w, h, col

def get_box(im, box, pos, new_w, new_h, old_w = 952, old_h = 736):
    '''helper method for obtaining a certain part of an image as a new matrix
    '''

    box_w = math.ceil((box[0]/old_w) * new_w)
    box_h = math.ceil((box[1]/old_h) * new_h)

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
    target = get_box(input, (24, 21), (0, 0), old_w = 43, old_h=119, new_w=new_x, new_h=new_y)
    img = isolate_card(target)
    first_card.rank_im = img

    # grabbing the first suite
    target = get_box(input, (12, 15), (24, 1), old_w=43, old_h=119, new_w=new_x, new_h=new_y)
    img = isolate_card(target, fsuite = True)
    first_card.suit_im = img

    # grabbing the second rank
    target = get_box(input, (24, 21), (0, 60), old_w=43, old_h=119, new_w=new_x, new_h=new_y)
    img = isolate_card(target)
    second_card.rank_im = img

    # grabbing the second suite
    target = get_box(input, (12, 21), (24, 60), old_w=43, old_h=119, new_w=new_x, new_h=new_y)
    img = isolate_card(target, fsuite = True)
    second_card.suit_im = img

    first_card.im = input

    return first_card, second_card

def isolate_card(img, bin_val=150, thresh_val=127, cont=1, fsuite=False):
    first_rank = binerize(img, bin_val)

    if fsuite == True:
        length = np.shape(first_rank)[1]
        new_row = np.tile(255, (1, length))
        first_rank = np.concatenate((first_rank, new_row))
        first_rank = np.uint8(first_rank)
        first_rank[first_rank == -1] = 151

        width = np.shape(first_rank)[0]
        new_column = np.tile(255, (1, width))
        first_rank = np.append(new_column.reshape(width, 1), first_rank, axis=1)
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

def grab_pot(imgray):
    output = ""
    text = pytesseract.image_to_string(imgray)
    for a in range(len(text) - 10):
        b = text[a:a + 5]
        if b == "Pot: ":
            for i in range(10):
                u = text[a + 5 + i]
                if u == "\n":
                    output = text[a + 5:a + 5 + i]
                    break
    return output

def get_dealer_pos(imcolor, height):
    hsv = cv.cvtColor(imcolor, cv.COLOR_BGR2HSV)
    lower_red = np.array([110, 50, 50])
    upper_red = np.array([130, 255, 255])
    mask = cv.inRange(hsv, lower_red, upper_red)

    ret, thresh = cv.threshold(mask, 150, 255, 0)
    contours, heirarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    index_sort = sorted(range(len(contours)), key=lambda i: cv.contourArea(contours[i]), reverse=True)

    contour = contours[index_sort[0]]
    x, y, w, h = cv.boundingRect(contour)

    if y > height/2:
        return "You are dealer"
    else:
        return "You are not the dealer"

def get_my_pot(imgray, w, h):
    my_chips_box = get_box(imgray, (30, 100), (510, 500), new_w=w, new_h=h)
    text = pytesseract.image_to_string(my_chips_box)
    return int(text)

def get_opponent_pot(imgray, w, h):
    opponent_chips_box = get_box(imgray, (30, 100), (120, 440), new_w=w, new_h=h)
    text = pytesseract.image_to_string(opponent_chips_box)
    return int(text)

def update_list_of_cards(cards, list_of_cards):
    pass

def get_opponent_bet():
    pass

def action_control(action):
    pass

def get_opp_name(imgray, w, h):
    name_box = get_box(imgray, (30, 130), (100, 420), new_w=w, new_h=h)
    text = pytesseract.image_to_string(name_box)
    return int(text)
def main():
    # loading sample images
    sample_ranks, sample_suits = load_samples()

    # grabbing a grayscale image of the poker window
    name = get_window_name()
    imgray, w, h, imcolor = grab_poker_window(name)

    # grabbing pot, opponent name
    pot = grab_pot(imgray)
    opp_name = get_opp_name(imgray, w, h)

    # creaing a list of cards
    list_of_cards = []

    # excracting my cards from the image
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
    if len(cards) == 0:
        dealer = get_dealer_pos(imcolor, h)
    if len(cards) == 1 or len(cards) == 2:
        raise AssertionError("There cannot be one or two cards on the table :(")
    if len(cards) == 3:
        deck_card1 = cards[0]
        list_of_cards.append(deck_card1)
        deck_card2 = cards[1]
        list_of_cards.append(deck_card2)
        deck_card3 = cards[2]
        list_of_cards.append(deck_card3)
    if len(cards) == 4:
        deck_card1 = cards[0]
        list_of_cards.append(deck_card1)
        deck_card2 = cards[1]
        list_of_cards.append(deck_card2)
        deck_card3 = cards[2]
        list_of_cards.append(deck_card3)
        deck_card4 = cards[3]
        list_of_cards.append(deck_card4)
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

    for card in list_of_cards:
        # comparing rank
        rank_im = card.rank_im
        rank_name = compare(rank_im, sample_ranks, sample_suits)
        card.rank = rank_name

        # comparing suit
        suit_im = card.suit_im
        suit_name = compare(suit_im, sample_ranks, sample_suits)
        card.suit = suit_name


    # rewrite = list_of_cards[1].suit_im
    # cv.imshow("yes", rewrite)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    #cv.imwrite("sample_images3/spade_first2.png", rewrite)

    for card in list_of_cards:
        print(card.rank, card.suit)

    check_button = get_box(imgray, (50, 150), (625, 680), new_w=w, new_h=h)
    raise_button = get_box(imgray, (50, 145), (625, 855), new_w=w, new_h=h)
    fold_button =  get_box(imgray, (50, 145), (625, 510), new_w=w, new_h=h)
    raise_amount = get_box(imgray, (20, 20), (590, 730), new_w=w, new_h=h)



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

