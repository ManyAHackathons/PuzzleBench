from abc import ABC, abstractmethod


class Module(ABC):
    def __init__(self):
        self.defused = False

    @abstractmethod
    def description(self) -> str:
        """Returns a description of the module."""
        pass
    
    @abstractmethod
    def manual(self) -> str:
        """Returns the manual for the module."""
        pass

    @abstractmethod
    def action(self, string: str) -> str:
        """Performs an action on the module. Returns a result message. The string that is entered is part of the module's solution flag. If the correct string is entered, the module is defused."""
        pass

    def getName(self) -> str:
        return self.__class__.__name__

    def is_defused(self) -> bool:
        return self.defused

    def defuse(self):
        self.defused = True
