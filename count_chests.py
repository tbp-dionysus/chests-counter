
from pynput import keyboard
import pyautogui

from lib.screen import read_chest_screen, read_player_screen
from lib.db import add_chest, add_player, export, export_html

all_chests = []

def on_key_release(key):
    if 'char' in dir(key):
        if key.char == 'c':
            chest = read_chest_screen()
            if chest:
                add_chest(chest.player_name, chest.source)
        if key.char == 'p':
            player = read_player_screen()
            if player:
                add_player(player.player_name)  
        elif key.char == 'h':
            print(pyautogui.position())
        elif key.char == 'e':
            export()
            export_html()
            exit()
    elif key == keyboard.Key.esc:
        exit()

with keyboard.Listener(on_release=on_key_release) as l2:
    l2.join()

