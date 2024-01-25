import pyautogui
import random
import time
def click_button(x1, x2, y1, y2, x, y):
    # rand_x = random.randint(x1, x2)
    # rand_y = random.randint(y1, y2)
    rand_x = (x1 + x2)/2
    rand_y = (y1 + y2)/2
    x_pos = rand_x + x
    y_pos =  rand_y + y

    movement = pyautogui.easeInQuad

    rand_num = random.randint(0, 3)
    if rand_num == 1:
        movement = pyautogui.easeInQuad
    elif rand_num == 2:
        movement = pyautogui.easeOutQuad
    elif rand_num == 3:
        movement = pyautogui.easeInElastic
    else:
        movement = pyautogui.easeInQuad

    pyautogui.moveTo(x_pos,  y_pos , 1, movement)
    #pyautogui.moveTo(x1, y1, 1)
    pyautogui.click()




def write_amount(num):
    for i in range(10):
        pyautogui.press('backspace')
    pyautogui.write(str(num), interval = .5)

if __name__ == '__main__':
    x, y = pyautogui.size()
    x1, y1 = pyautogui.position()
    pyautogui.moveTo(x - 50 , y - 50, 1, pyautogui.easeInElastic)





