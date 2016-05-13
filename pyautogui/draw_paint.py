import pyautogui
import time

time.sleep(5)

# pyautogui.typewrite('Hello world!')
pyautogui.click()

distance = 100
moves = [
	{'x':-1,'y':0},
	{'x':0,'y':2},
	{'x':-1,'y':0},
	{'x':1,'y':0},
	{'x':0,'y':-1},
	{'x':-1,'y':0},
	{'x':0,'y':-1},
	{'x':0,'y':1},
	{'x':2,'y':0},
	{'x':0,'y':1}]	
for move in moves:
	pyautogui.dragRel(move['x']*distance, move['y']*distance, duration=0.2)
