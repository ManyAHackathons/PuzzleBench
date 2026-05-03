import random
from typing import List, Dict, Optional
from .bomb import Module

class Memory(Module):
    def __init__(self):
        super().__init__()
        self.stage = 1
        self.max_stage = 5

        self.display = random.randint(1, 4)
        self.buttons = [1,2,3,4]
        random.shuffle(self.buttons)

        self.history: List[Dict[str, int]] = []

def description(self) -> str:
        return f"Stage {self.stage}: Display shows {self.display}, buttons are {self.buttons}"

def manual(self) -> str:
        return f"""Memory Module Manual:
        Stage 1: If the display is 1, press the button in third position. 
        If the display is 2, press the button in fourth position.
        If the display is 3, press the button in first position.
        If the display is 4, press the button in second position.

        Stage 2: If the display is 1, press the button labeled '3'.
        If the display is 2, press the button in the same position as you pressed in stage 1.
        If the display is 3, press the button in the fourth position.
        If the display is 4, press the button in the same position as you pressed in stage 1.

        Stage 3: If the display is 1, press the button with the same label you pressed in stage 1.
        If the display is 2, press the button with the same label you pressed in stage 2.
        If the display is 3, press the button labeled '1'.
        If the display is 4, press the second button. 

        Stage 4: If the display is 1, press the button in the same position as you pressed in stage 2.
        If the display is 2, press the button in the first position.
        If the display is 3, press the button in the same position as you pressed in stage 1.
        If the display is 4, press the button in the same position as you pressed in stage 3.

        Stage 5: If the display is 1, press the button with the same label you pressed in stage 2.
        If the display is 2, press the button with the same label you pressed in stage 3.
        If the display is 3, press the button with the same label you pressed in stage 4.
        If the display is 4, press the button with the same label you pressed in stage 1.
        """

