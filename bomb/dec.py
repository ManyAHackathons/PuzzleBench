from .bomb import Module
import base64
import random

class Dec(Module):
    #We can use a function called base64.decodebytes() to decode our base 64 string.
    def __init__(self):
        super().__init__()
        with open("base64encrypted.txt", "r") as e, open("base64decrypted.txt", "w") as d:
            self.all_enc = [line.strip() for line in e.line.strip()]
            self.all_dec = [line.strip() for line in d.line.strip()]

        index = random.randint(0, len(self.all_enc) - 1)
        self.target_encoded = self.all_enc[index]
        self.correct_word = self.all_dec[index]
        
        self.buttons = self._generate_buttons()

    def _generate_buttons(self):
        buttons  = [w for w in self.all_dec if w != self.correct_word and abs(len(w) - len(self.correct_word)) <= 4 and w != self.correct_word]
        selected = random.sample(buttons, min(len(buttons), 3)) + [self.correct_word]
        random.shuffle(selected)
        return selected
    
    def description(self) -> str:
        return f"Decoder Module: Display shows: {self.target_encoded}. Buttons available: {', '.join(self.buttons)}"
    
    def manual(self) -> str:
        mapping = [f"{e} -> {d}" for e, d in zip(self.all_enc, self.all_dec)]
        return "Decoder Manual:\n" + "\n".join(mapping)
    
    def action(self, choice: str) -> str:
        if choice.strip().lower() == self.correct_word.lower():
            self.defuse()
            return "Correct! Module defused."
        return "Incorrect. Strike Recorded."
        