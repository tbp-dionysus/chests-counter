from os import name
from typing import List, Optional

import screen_ocr
import pyautogui

class Chest:
    def __init__(self, player_name, source):
        self.player_name = player_name
        self.source = source

def read_screen() -> Chest:
    ocr_reader = screen_ocr.Reader.create_quality_reader()
    
    results = ocr_reader.read_screen(bounding_box=(785, 406, 1411, 495))
    
    chest = parse_text(results.as_string())
    
    if chest:
        button_location = pyautogui.Point(x=1351, y=474)
        pyautogui.moveTo(button_location)
        pyautogui.click()
        return chest
    return None

def parse_text(text) -> Optional[Chest]:
    lines = text.splitlines()
    chest_found = False
    print(lines)

    for line in lines:
        if "from" in line.lower():
            player_name = line.replace("From:", "").strip()
            chest_found = True
        if "source" in line.lower():
            source = line.replace("Source:", "").strip()

    if not chest_found:
        return None
    return Chest(player_name, source)