import pyautogui
import time

pyautogui.PAUSE = 1

pyautogui.press("win")
pyautogui.write('brave')
pyautogui.press('enter')
time.sleep(2)
pyautogui.write('www.youtube.com')
time.sleep(1)
pyautogui.press('enter')
time.sleep(2)
pyautogui.click(x=464, y=323) # pego a posiçao com o print(pyautogui.position()) e time.sleep(5)  
# pyautogui.hotkey('alt', 'tab')   // este é para atalho
