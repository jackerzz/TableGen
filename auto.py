import sys
import time
import pyautogui
time.sleep(3)
x=650
y=270
pyautogui.click(x,y)      #鼠标点击(x,y)
# pyautogui.typewrite("import os sys")
def run():
    while True:
        pyautogui.typewrite("import os sys")
        time.sleep(3)
        pyautogui.hotkey('ctrl','a')
        time.sleep(3)
        pyautogui.typewrite(["backspace"])
        time.sleep(2)
# pyautogui.rightClick(x,y)     #鼠标右击(x,y),同理还有middleClick(中击)，doubleClick(双击)，tripleClickimport os sys# pyautogui.scroll(x,y)      #鼠标在(x,y)滚动
#
#
# pyautogui.mouseDown(x,y,button='left')     #鼠标左边按下，同理mouseUp为鼠标松开
run()