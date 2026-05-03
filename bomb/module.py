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
    def action(self, *args, **kwargs) -> None:
        """Performs an action on the module. Returns a result message."""
        pass

    def is_defused(self) -> bool:
        return self.defused

    def defuse(self):
        self.defused = True
