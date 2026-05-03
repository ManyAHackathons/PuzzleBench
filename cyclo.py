import random
import string
from typing import List, Optional
from .bomb import Module

class wordleCyclo(Module):
    def __init__(self):
        super().__init__()
        self.target_string = "".join(random.choices(string.ascii_uppercase, k =5))
        self.display_letters = list(self.target_string)
        random.shuffle(self.display_letters)

        self.current_index = 0
        self.attempts = 0
        self.max_attempts = 6
        self.solved = False

    def current_letter(self) -> str:
        """ What the Defuser model sees 'right now'. """
        return self.display_letters[self.current_index]

    def rotate(self):
        """Advance the cyclogram."""
        self.current_index = (self.current_index + 1) % len(self.display_letters)

    def submit_guess(self, guess: str) -> List[int]:
        """
        Logic for Wordle feedback.
        Returns a list of status codes: 2(Green), 1(Yellow), 0(Gray)
        """

        guess = guess.upper()
        if len(guess) != 5:
            return[]

        self.attempts += 1
        feedback = [0] * 5

        target_list : List[Optional[str]] = list(self.target_string) 
        guess_list : List[Optional[str]] = list(guess) 

        for i in range(5): 
            if guess_list[i] == target_list[i]:
                feedback[i] = 2
                target_list[i] = ""
                guess_list[i] = ""

        for i in range(5):
            if guess_list[i] != "" and guess_list[i] in target_list:
                feedback[i] = 1
                target_list[target_list.index(guess_list[i])] = ""

        if feedback == [2,2,2,2,2]:
            self.solved = True
        
        return feedback
