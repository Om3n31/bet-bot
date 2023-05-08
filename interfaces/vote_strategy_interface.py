from abc import ABC, abstractmethod
from discord import Member
from typing import List

class VoteStrategyInterface(ABC):
    
    @abstractmethod
    def vote_owner(self) -> Member:
        pass
    
    @abstractmethod
    def vote_mentions(self) -> List[Member] | None:
        pass
    
    @abstractmethod
    def vote_topic(self) -> str:
        pass
    
    @abstractmethod
    async def exec(self) -> bool:
        pass
    
    @abstractmethod
    def vote_content(self) -> str:
        pass
    
    @abstractmethod
    def resolved_content(self) -> str:
        pass
    
    @abstractmethod
    async def print(self):
        pass