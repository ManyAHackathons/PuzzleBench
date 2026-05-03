from typing import List

from .module import Module
from .wires import Wires


class Bomb():
    def __init__(self):
        self.modules: List[Module] = []
        self.modules.append(Wires())

    def look_at_bomb(self):
        """Return information about the bomb (serial number, indicators, ports, etc...)"""
        return "The bomb has a serial number of ABC123"

    def module_action(self, module_id: int, *args, **kwargs) -> str:
        """Perform an action on a module (cut a wire, press a button, etc...)"""
        return self.modules[module_id].action(*args, **kwargs)

    def module_look(self, module_id: int) -> str:
        """Look at a module and get its description"""
        return self.modules[module_id].description()

    def add_module(self, module: Module):
        """Add a module to the bomb"""
        self.modules.append(module)
    