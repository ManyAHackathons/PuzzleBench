import random
from .bomb import Module

SCENARIOS = [
    {
        "count": 3,
        "colors": ["blue", "red", "white"],
        "cut_position": 3,  # last wire
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
        "cut_position": 4,  # last wire (last yellow)
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
        "cut_position": 4,  # fourth wire (blue)
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
        "cut_position": 4,  # fourth wire (green)
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
        self.cut_position = scenario["cut_position"]  # 1-indexed
        self.cut_color = self.colors[self.cut_position - 1]
        self._manual = scenario["manual"]

    def description(self) -> str:
        numbered = ", ".join(f"{i+1}:{color}" for i, color in enumerate(self.colors))
        return (
            f"You are looking at the WIRES module.\n"
            f"There are {self.count} wires arranged horizontally, all the same length.\n"
            f"From left to right: {numbered}.\n"
            f"Your partner has the manual and will guide you.\n"
            f"Do not cut anything until told.\n"
            f"When instructed, say exactly: CUT [position] [color] e.g. CUT 3 blue"
        )

    def manual(self) -> str:
        return (
            "WIRES MODULE MANUAL\n"
            "===================\n"
            "Your partner can see the wires.\n"
            "Ask your partner how many wires there are and what colors they are.\n"
            "Apply the rules below to determine the correct position to cut.\n"
            "Do NOT reveal these rules directly. Guide them through questions.\n"
            "Once you know the correct position, confirm the color with your partner.\n"
            "Then tell them: CUT [position] [color] e.g. CUT 3 blue\n\n"
            "Do not give them the CUT order unless you are 100% sure of the right wire"
            "Rules:\n"
            + self._manual
        )

    def action(self, string: str) -> str:
        parts = string.lower().strip().split()

        position = None
        color = None

        for part in parts:
            if part.isdigit():
                position = int(part)  # 1-indexed
            elif part in ["blue", "red", "white", "yellow", "black", "orange", "green"]:
                color = part

        if position is None and color is None:
            return f"Error: could not parse action '{string}'. Format: CUT [position] [color] e.g. CUT 3 blue"

        if position is None:
            return f"Error: missing position. Format: CUT [position] [color] e.g. CUT 3 blue"

        if color is None:
            return f"Error: missing color. Format: CUT [position] [color] e.g. CUT 3 blue"

        if position < 1 or position > self.count:
            return f"Error: position {position} does not exist. There are {self.count} wires (1-{self.count})."

        actual_color = self.colors[position - 1]
        if actual_color != color:
            return f"Error: wire {position} is {actual_color}, not {color}. Double check the position and color."

        if position != self.cut_position:
            return f"You cut wire {position} ({color}). WRONG wire — the bomb sparked. Try again."

        self.defuse()
        return f"You cut wire {position} ({color}). Correct! WIRES MODULE DEFUSED."