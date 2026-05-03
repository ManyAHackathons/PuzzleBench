from typing import List
from .module import Module
from .wires import Wires
from .cyclo import WordleCyclo
from .button import Button

class Bomb():
    def __init__(self):
        self.modules: List[Module] = []
        self.modules.append(Button())

    def view_bomb(self):
        module_list = "\n".join(
            f" Module {i}: {module.getName()} ({'defused' if module.is_defused() else 'active'})" for i, module in enumerate(self.modules)
        )
        return (
            f"You are looking at the bomb.\n"
            f"Active modules:\n{module_list}"
        )

    def action_module(self, module_id: int, string: str) -> str:
        """Perform an action on a module (cut a wire, press a button, etc...). Actions are represented as strings that are passed to the module's action function. Returns a result message. If the string that is entered is part of the module's solution flag, the module is defused."""
        return self.modules[module_id].action(string)

    def view_module(self, module_id: int) -> str:
        """Look at a module and get its description"""
        return self.modules[module_id].description()
    
    def get_modules(self) -> List[Module]:
        """Returns the list of modules on the bomb."""
        return self.modules

    def get_manual(self, module_name: str) -> str:
        """Return the manual for the first module whose name matches module_name (case-insensitive)."""
        for module in self.modules:
            if module.getName().lower() == module_name.lower():
                return module.manual()
        available = ", ".join(m.getName() for m in self.modules)
        return f"No module named '{module_name}' found. Active modules: {available}"
    
    def defused(self) -> bool:
        """Returns true if all modules are defused, false otherwise."""
        return all(module.is_defused() for module in self.modules)