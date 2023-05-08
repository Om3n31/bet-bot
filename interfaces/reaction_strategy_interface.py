from abc import ABC, abstractmethod
from discord import Member
from typing import List

class ReactionStrategyInterface(ABC):
    
    @abstractmethod
    async def add_reaction(self):
        pass

    @abstractmethod
    async def remove_reaction(self):
        pass