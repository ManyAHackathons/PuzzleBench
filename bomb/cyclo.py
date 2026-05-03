import random
import string
from typing import List, Optional
from .module import Module


class Cyclogram(Module):
    def __init__(self):
        super().__init__()

        self.target_string = "".join(random.choices(string.ascii_uppercase, k=5))
        # 6 letters shown to defuser: the 5 target letters plus one random extra
        extra = random.choice(string.ascii_uppercase)
        self.display_letters = list(self.target_string) + [extra]
        random.shuffle(self.display_letters)

        self.current_index = 0
        self.attempts = 0
        self.max_attempts = 6

    def description(self) -> str:
        all_letters = ", ".join(self.display_letters)
        current = self.display_letters[self.current_index]
        return (
            f"A Cyclogram module. There are 6 letters available: {all_letters}. "
            f"The currently highlighted letter is: '{current}'. "
            f"You can 'rotate' to cycle the highlight, or submit a 5-letter guess."
        )

    def manual(self) -> str:
        return (
            "WORDLE CYCLOGRAM MANUAL\n"
            "The defuser sees 6 letters and must find the hidden 5-letter word.\n"
            "1. Ask the defuser to read all 6 letters to you.\n"
            "2. Determine a valid 5-letter word using only those letters.\n"
            "3. Tell the defuser to submit your word guess.\n"
            "4. Feedback codes per letter: 2 = correct letter & position, "
            "1 = correct letter but wrong position, 0 = not in word.\n"
            "5. Use feedback to refine guesses. Module defuses on all 2s.\n"
            f"Maximum {self.max_attempts} attempts."
        )

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
