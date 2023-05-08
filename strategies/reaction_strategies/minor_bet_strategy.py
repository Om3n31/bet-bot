import discord
from interfaces.reaction_strategy_interface import ReactionStrategyInterface
from discord import Reaction, Member
from typing import List
from vote import Vote
from embeds.votebox_vote import VoteBoxVote
from tools.emojis import *

class MinorBetReactionStrategy(ReactionStrategyInterface):
    
    vote: Vote
    reaction: Reaction
    user: Member
    
    def __init__(self, vote: Vote, reaction: Reaction, user: Member):
        self.vote = vote
        self.reaction = reaction
        self.user = user
    
    async def add_reaction(self):
        if self.reaction.emoji == YES_REACTION:
            await self.vote.add_vote(self.user.id, True)
        elif self.reaction.emoji == X_REACTION:
            await self.vote.add_vote(self.user.id, False)
    
    async def remove_reaction(self):
        if self.reaction.emoji == YES_REACTION:
            await self.vote.remove_vote(self.user.id, True)
        elif self.reaction.emoji == X_REACTION:
            await self.vote.remove_vote(self.user.id, False)