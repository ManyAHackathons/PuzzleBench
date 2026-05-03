import random
from .module import Module


class Wires(Module):
    def __init__(self):
        super().__init__()
        self.count = random.randint(3, 6)
        self.colors = ["blue", "black", "orange", "green"]
        self.cut_wire = False
        self.cut_order = random.randint(0, self.count - 1)

    def description(self) -> str:
        return f"There are {self.count} wires. The colors are: {', '.join(self.colors[:self.count])}."

    def action(self, wire_index: int) -> str:
        if wire_index < 0 or wire_index >= self.count:
            return "Invalid wire index. Try again."

        if self.cut_wire:
            return "You have already cut a wire. This module is now defused."

        self.cut_wire = True

        if wire_index == self.cut_order:
            self.defused = True
            return "You cut the correct wire! This module is now defused."
        else:
            self.defused = True
            return "You cut the wrong wire! The bomb explodes!"
