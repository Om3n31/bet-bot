from abc import ABC, abstractmethod
from discord import Embed

class ReactableInterface(ABC):
    
    @abstractmethod
    def message_id(self) -> int:
        pass
    
    @abstractmethod
    def can_react(self) -> bool:
        pass
    
    @abstractmethod
    def can_reply(self) -> bool:
        pass
    
    @abstractmethod
    def emojis_used(self) -> set:
        pass
    
    @abstractmethod
    def on_add_reaction(self):
        pass
    
    @abstractmethod
    def on_remove_reaction(self):
        pass
    
    @abstractmethod
    def on_reply(self):
        pass
    
    @abstractmethod
    def get_strategy(self):
        pass
    
    @abstractmethod
    async def exec(self):
        pass