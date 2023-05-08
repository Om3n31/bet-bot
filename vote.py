import os
import asyncio
from typing import List
from interfaces.vote_strategy_interface import VoteStrategyInterface
from embeds.votebox_vote import VoteBoxVote
from tools.tools import *

class Vote:
    vote_strategy: VoteStrategyInterface
    votebox: VoteBoxVote
    voters: List[int]
    yay: int
    nay: int
    is_resolved: bool
    
    def __init__(self, vote_strategy: VoteStrategyInterface, votebox: VoteBoxVote):
        self.yay = 1
        self.nay = 0
        self.voters = []
        self.voters.append(vote_strategy.vote_owner().id)
        self.vote_strategy = vote_strategy
        self.vote_box = votebox
        self.is_resolved = False
    
    async def start_timer(self, duration: int):
        await asyncio.sleep(duration)
        await self.resolve()
    
    async def add_vote(self, voter_id: int, vote: bool):
        self.voters.append(voter_id)
        if vote:
            self.yay += 1
            await self.start_timer(1)
        else:
            self.nay += 1
    
    def remove_vote(self, voter_id: int, vote: bool):
        self.voters.remove(voter_id)
        if vote:
            self.yay -= 1
        else:
            self.nay -= 1
    
    async def resolve(self):
        if self.yay > self.nay:
            await self.vote_strategy.exec()
        else:
            print("in vote resolve nay")
            pass
        self.is_resolved = True
        pass