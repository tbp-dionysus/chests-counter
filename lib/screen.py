from os import name
from typing import List, Optional

import screen_ocr
import pyautogui

from lib.db import add_chest_type, get_chest_type, get_player


class Chest:

    def __init__(self, player_name, source):
        self.player_name = player_name
        self.source = source

    def validate(self):
        if not self.player_name or not self.source:
            return False
        player = get_player(self.player_name)
        if not player:
            print(f"Player '{self.player_name}' not found in database.")
            return False

        chest_type = get_chest_type(self.source)
        if not chest_type:
            add_chest_type(self.source)
      
        return True 

class Player:
    def __init__(self, player_name):
        self.player_name = player_name


def read_chest_screen() -> Chest:
    ocr_reader = screen_ocr.Reader.create_quality_reader()
    
    results = ocr_reader.read_screen(bounding_box=(790, 411, 1149, 490))
    
    chest = parse_chest_text(results.as_string())
    
    if chest:
        if chest.validate():
            button_location = pyautogui.Point(x=1351, y=474)
            pyautogui.moveTo(button_location)
            pyautogui.click()
            return chest
        else:
            print("Invalid chest data: ", results.as_string())
            exit()
    else:
        print("No valid chest data found.")
        print("OCR Result: ", results.as_string())
        exit()
    return None

def read_player_screen() -> Chest:
    ocr_reader = screen_ocr.Reader.create_quality_reader()
    
    results = ocr_reader.read_screen(bounding_box=(790, 405, 1222, 437))
    
    player = parse_player_text(results.as_string())
    
    if player:
        return player
    return None


def parse_chest_text(text) -> Optional[Chest]:
    lines = text.splitlines()
    chest_found = False

    for line in lines:
        if "from" in line.lower():
            player_name = line.replace("From:", "").strip()
            chest_found = True
        if "source" in line.lower():
            source = line.replace("Source:", "").strip()

    if not chest_found:
        return None
    return Chest(player_name, source)


def parse_player_text(text) -> Optional[Player]:
    lines = text.splitlines()
    if len(lines) == 0:
        return None
    return Player(lines[0].strip())