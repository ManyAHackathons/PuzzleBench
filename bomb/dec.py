import base64
import random
from .module import Module

PHRASES = [
    "BOMB DEFUSAL",
    "KEEP TALKING",
    "NOBODY EXPLODES",
    "TOP SECRET",
    "DANGER ZONE",
    "RED WIRE",
]


class Dec(Module):
    def __init__(self):
        super().__init__()
        phrase = random.choice(PHRASES)
        self.encoded = base64.b64encode(phrase.encode()).decode()
        self.length = len(phrase)

    def description(self) -> str:
        return (
            f"A DECODING module. You see an encoded string on the display: {self.encoded}\n"
            f"Read this string exactly to your partner. Then wait for their instructions."
        )

    def manual(self) -> str:
        return (
            "DECODING MODULE MANUAL\n"
            "The defuser will read you a Base64-encoded string.\n"
            "1. Decode the Base64 string to find the original text.\n"
            "2. Count the number of characters in the decoded result (including spaces).\n"
            "3. Tell the defuser that exact character count.\n"
            "4. The defuser will submit the number. It succeeds if within 4 of the true length."
        )

    def action(self, string: str) -> str:
        try:
            guess = int(string.strip())
        except ValueError:
            return "Error: submit a number representing the character length of the decoded string."

        if abs(guess - self.length) <= 4:
            self.defuse()
            return f"Correct! The decoded string is {self.length} characters. Module defused!"
        return f"Wrong length. Strike! (Your guess: {guess}, acceptable range: {self.length - 4}–{self.length + 4})"
