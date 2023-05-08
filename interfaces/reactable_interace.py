from abc import ABC, abstractmethod

class ReactableInterface(ABC):
    
    @abstractmethod
    def can_react(self) -> bool:
        pass

    @abstractmethod
    def add_reaction(self):
        pass
    
    @abstractmethod
    def remove_reaction(self):
        pass
    
    @abstractmethod
    def get_strategy(self):
        pass
    
    @abstractmethod
    async def exec(self):
        pass