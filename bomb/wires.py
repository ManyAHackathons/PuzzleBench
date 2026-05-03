import random
from .module import Module

SCENARIOS = [
    {
        "count": 3,
        "colors": ["blue", "red", "white"],
        "cut_color": "white",
        "manual": (
            "There are 3 wires.\n"
            "- If there are no red wires: cut the second wire\n"
            "- Otherwise if the last wire is white: cut the last wire\n"
            "- Otherwise if there is more than one blue wire: cut the last blue wire\n"
            "- Otherwise: cut the last wire\n"
        )
    },
    {
        "count": 4,
        "colors": ["red", "blue", "yellow", "yellow"],
        "cut_color": "yellow",
        "manual": (
            "There are 4 wires.\n"
            "- If the last wire is yellow and there are no red wires: cut the first wire\n"
            "- Otherwise if there is exactly one blue wire: cut the first wire\n"
            "- Otherwise if there is more than one yellow wire: cut the last wire\n"
            "- Otherwise: cut the second wire\n"
        )
    },
    {
        "count": 5,
        "colors": ["black", "yellow", "red", "blue", "white"],
        "cut_color": "blue",
        "manual": (
            "There are 5 wires.\n"
            "- If there is exactly one red wire and more than one yellow wire: cut the first wire\n"
            "- Otherwise if there are no black wires: cut the second wire\n"
            "- Otherwise: cut the first wire\n"
        )
    },
    {
        "count": 6,
        "colors": ["orange", "blue", "red", "green", "white", "white"],
        "cut_color": "green",
        "manual": (
            "There are 6 wires.\n"
            "- If there is exactly one yellow wire and more than one white wire: cut the fourth wire\n"
            "- Otherwise if there are no red wires: cut the last wire\n"
            "- Otherwise: cut the fourth wire\n"
        )
    },
]

class Wires(Module):
    def __init__(self):
        super().__init__()
        scenario = random.choice(SCENARIOS)
        self.count = scenario["count"]
        self.colors = scenario["colors"]
        self.cut_color = scenario["cut_color"]
        self._manual = scenario["manual"]

    def description(self) -> str:
        numbered = ", ".join(f"{i+1}:{color}" for i, color in enumerate(self.colors))
        return (
            f"You are looking at the WIRES module.\n"
            f"There are {self.count} wires arranged horizontally, all the same length.\n"
            f"From left to right: {numbered}.\n"
            f"Your partner has the manual and will guide you.\n"
            f"Do not cut anything until told.\n"
            f"When instructed, you will be told: CUT [color]"
        )

    def manual(self) -> str:
        return (
            "WIRES MODULE MANUAL\n"
            "===================\n"
            "Your partner can see the wires.\n"
            "Ask your partner about the wire colors and apply the rules below.\n"
            "Do NOT reveal these rules directly. Guide them through questions.\n"
            "Once you know the correct position, ask your partner what color is in that position.\n"
            "Then say: CUT [color]\n\n"
            + self._manual
        )

    def action(self, color: str) -> None:
        color = color.lower()
        if color not in self.colors:
            return None
        if color != self.cut_color:
            return None
        self.defuse()