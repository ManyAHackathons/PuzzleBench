import random
import string
from typing import List, Optional
from .bomb import Module

class WordleCyclo(Module):
    def __init__(self):
        super().__init__()
      
        self.target_string = "".join(random.choices(string.ascii_uppercase, k=5))
        self.display_letters = list(self.target_string)
        random.shuffle(self.display_letters)

        self.current_index = 0
        self.attempts = 0
        self.max_attempts = 6

    def description(self) -> str:
        """What the Defuser sees to describe the module."""
        return (f"A WordleCyclo module with 5 rotating positions. "
                f"The letter currently visible is: '{self.current_letter()}'")

    def manual(self) -> str:
        """The instructions the Expert model must follow."""
        return (
            "WORDLE CYCLOGRAM MANUAL\n"
            "1. The module cycles through 5 random letters.\n"
            "2. Identify all 5 letters by instructing the defuser to 'rotate'.\n"
            "3. Submit a 5-letter guess to receive feedback.\n"
            "4. Feedback codes: 2 = Correct letter & position, 1 = Correct letter but wrong position, 0 = Absent.\n"
            "5. The module is defused when you receive all 2s (Green)."
        )

    def current_letter(self) -> str:
        return self.display_letters[self.current_index]

    def action(self, cmd: str) -> str:
        """
        Modified to handle 'rotate [n]' or 'submit[guess]' in a single string
        to stay consistent with the base case.
        """
        if self.defused:
            return "Module is already defused."
        
        parts = cmd().lower().split()
        if not parts:
            return "No command provided."
        
        cmd = parts[0]

        if cmd == "rotate":
            try:
                steps = int(parts[1]) if len(parts) > 1 else 1
                self.current_index = (self.current_index + steps) % len(self.display_letters)
                return f"Rotated {steps} step(s). Current letter: {self.current_letter()}"
            except ValueError:
                return "Error: Rotation steps must be a number."

        elif cmd == "submit":

            if len(parts) < 2 or len(parts[1]) != 5:
                return "Error: Guess must be a 5-letter word."
            
            guess = parts[1].upper()
            feedback = self._submit_guess(guess)
            
            if self.defused:
                return f"Feedback: {feedback}. MODULE DEFUSED!"
            
            if self.attempts >= self.max_attempts:
                return f"Feedback: {feedback}. STRIKE: Maximum attempts reached."

        return "Unknown command. Use 'rotate[n]' or 'submit[n]'."

    def _submit_guess(self, guess: str) -> List[int]:
        """Internal logic for Wordle feedback."""
        guess = guess.upper()
        self.attempts += 1
        feedback = [0] * 5
        
        target_list: List[Optional[str]] = list(self.target_string)
        guess_list: List[Optional[str]] = list(guess)

        for i in range(5):
            if guess_list[i] == target_list[i]:
                feedback[i] = 2
                target_list[i] = None
                guess_list[i] = None

        for i in range(5):
            if guess_list[i] is not None and guess_list[i] in target_list:
                feedback[i] = 1
                target_list[target_list.index(guess_list[i])] = None

        if feedback == [2, 2, 2, 2, 2]:
            self.defuse()
        
        return feedback