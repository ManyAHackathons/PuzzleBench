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

    def action(self, cmd: str, guess: Optional[str] = None) -> str:
        """
        Implementation of the abstract action method.
        Commands: 'rotate' or 'submit'
        """
        if self.defused:
            return "Module is already defused."

        if cmd.lower() == "rotate":
            self.current_index = (self.current_index + 1) % len(self.display_letters)
            return f"Rotated. Current letter: {self.current_letter()}"

        elif cmd.lower() == "submit":
            if not guess or len(guess) != 5:
                return "Error: Guess must be exactly 5 letters."
            
            feedback = self._submit_guess(guess)
            if self.defused:
                return f"Feedback: {feedback}. MODULE DEFUSED!"
            
            if self.attempts >= self.max_attempts:
                return f"Feedback: {feedback}. STRIKE: Maximum attempts reached."
            
            return f"Feedback: {feedback}. Attempts left: {self.max_attempts - self.attempts}"

        return "Unknown command. Use 'rotate' or 'submit'."

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