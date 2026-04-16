
from pynput import keyboard
import pyautogui

from lib.screen import read_screen
from lib.db import create_connection, add_chest, export

all_chests = []

def on_key_release(key):
    if 'char' in dir(key):
        if key.char == 'c':
            chest = read_screen()
            if chest:
                add_chest(chest.player_name, chest.source)  
        elif key.char == 'h':
            print(pyautogui.position())
        elif key.char == 'e':
            export()
    elif key == keyboard.Key.esc:
        exit()
    
with keyboard.Listener(on_release=on_key_release) as l2:
    l2.join()

