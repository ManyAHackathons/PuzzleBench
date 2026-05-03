from .module import Module


class Button(Module):
    def __init__(self):
        super().__init__()
        self.color = "green"
        self.text = "Hold"
        
    def description(self) -> str:
        return f"There is a {self.color} button that says '{self.text}' on it."
    
    def action(self, string: str) -> str:
        if string.lower() == "tap":
            self.defuse()
            return "You tapped the button. It defused!"
        else:
            return "You did the wrong action. Try again."
    
    def manual(self) -> str:
        return f"""No matter what, "tap" the button. Don't hold it, don't do anything else, just tap it. If you do anything else, you will fail."""
    