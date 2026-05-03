import random
import string
from typing import List, Dict, Optional
from .bomb import Module

class Memory(Module):
    def __init__(self):
        super().__init__()
        self.stage = 1
        self.max_stage = 5

        self.history: List[Dict[str, int]] = []
        self._setup_stage()

    def _setup_stage(self):
        """Sets up a new display and randomizes button positions for the current stage."""
        self.display = random.randint(1, 4)
        self.buttons = [1,2,3,4]
        random.shuffle(self.buttons)

    def description(self) -> str:
        if self.defused:
            return "Memory module is defused."
        return (f"Memory Module - Stage {self.stage}/{self.max_stage}. "
                f"The Display shows: {self.display}. "
                f"The Buttons are labeled as: {self.buttons}")

    def manual(self) -> str:
        """The reference text for the Expert model."""
        return (
            "MEMORY MODULE MANUAL\n"
            "Positions are ordered 1, 2, 3, 4 from left to right.\n\n"
            "STAGE 1:\n"
            "- If display is 1: press button in 3rd position.\n"
            "- If display is 2: press button in 4th position.\n"
            "- If display is 3: press button in 1st position.\n"
            "- If display is 4: press button in 2nd position.\n\n"
            "STAGE 2:\n"
            "- If display is 1: press button labeled '3'.\n"
            "- If display is 2: press button in the same position as Stage 1.\n"
            "- If display is 3: press button in 4th position.\n"
            "- If display is 4: press button in the same position as Stage 1.\n\n"
            "STAGE 3:\n"
            "- If display is 1: press button with same label as Stage 1.\n"
            "- If display is 2: press button with same label as Stage 2.\n"
            "- If display is 3: press button labeled '1'.\n"
            "- If display is 4: press button in 2nd position.\n\n"
            "STAGE 4:\n"
            "- If display is 1: press button in the same position as Stage 2.\n"
            "- If display is 2: press button in 1st position.\n"
            "- If display is 3: press button in the same position as Stage 1.\n"
            "- If display is 4: press button in the same position as Stage 3.\n\n"
            "STAGE 5:\n"
            "- If display is 1: press button with same label as Stage 2.\n"
            "- If display is 2: press button with same label as Stage 3.\n"
            "- If display is 3: press button with same label as Stage 4.\n"
            "- If display is 4: press button with same label as Stage 1."
        )
    
    def action(self, label_str: int) -> str:
        """
        The Defuser performs an action by pressing a button label.
        Example usage in your bomb.py: bomb.module_action(module_id, label=3)
        """

        if self.defused:
            return "Module is already defused."
        
        try:
            label = int(label_str)
        except ValueError:
            return f"Error: Please provide the buttion label as a number"
        
        if label not in self.buttons:
            return f"Error. No button labeled '{label}' is present."
        
        target_index = self._get_target_index()
        pressed_index = self.buttons.index(label)

        if pressed_index == target_index:
            self.history.append({'label': label, 'position': pressed_index})

            if self.stage == self.max_stage:
                self.defuse()
                return f"Correct! Button '{label}' pressed. MODULE DEFUSED!"
            
            self.stage += 1
            self._setup_stage()
            return f"Correct! Button '{label}' pressed. Moving to Stage {self.stage}."
        else:
            self.stage = 1
            self.history = []
            self._setup_stage()
            return f"Incorrect! Button '{label}' pressed. STRIKE: Module RESET to Stage 1."
    
    def _get_target_index(self) -> int:
        """Logic to find the target position (0-3) based on the manual rules."""
        d = self.display
        h = self.history

        if self.stage == 1:
            if d == 1: return 2
            if d == 2: return 3
            if d == 3: return 0
            return 1
        elif self.stage == 2:
            if d == 1: return self.buttons.index(3)
            if d == 2: return h[0]['position']
            if d == 3: return 3
            return h[0]['position']
        elif self.stage == 3:
            if d == 1: return self.buttons.index(h[0]['label'])
            if d == 2: return self.buttons.index(h[1]['label'])
            if d == 3: return self.buttons.index(1)
            return 1
        elif self.stage == 4:
            if d == 1: return h[1]['position']
            if d == 2: return 0
            if d == 3: return h[0]['position']
            return h[2]['position']
        elif self.stage == 5:
            if d == 1: return self.buttons.index(h[1]['label'])
            if d == 2: return self.buttons.index(h[2]['label'])
            if d == 3: return self.buttons.index(h[3]['label'])
            return self.buttons.index(h[0]['label'])
        return - 1
    
