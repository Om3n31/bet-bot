from discord import Embed, Message, Interaction, TextChannel
from tools.emojis import *
from typing import Dict, List
from interfaces.vote_strategy_interface import VoteStrategyInterface
from engines.googlelimiter import Counter

class VoteBoxVote(Embed):
    def __init__(self):
        super().__init__(title="", description=f"", color=0x36393F)
        self.set_footer(text=f"Vote under this box.")

    async def print(self, channel: TextChannel):
        message = await channel.send(embed=self)
        self.message = message
    
    async def set_content(self, vote: VoteStrategyInterface, channel: TextChannel):
        self.add_field(name=vote.vote_topic(), value=vote.vote_content())
        await self.print(channel)
        
    async def update(self):
        await self.message.edit(embed=self)
    
    async def add_vote_slot(self):
       await self.message.add_reaction(YES_REACTION)
       await self.message.add_reaction(X_REACTION)
       
    async def resolve_vote(self, vote: VoteStrategyInterface, yay_voters: List[str], nay_voters: List[str]):
        await self.clear_votes()
        await self.remove_footer().remove_field(0).add_field(name=vote.vote_topic(), vote=vote.resolved_content())
        await self.add_field(name='Yay', value=f'```{0}```'.format("\n".join(yay_voters)), inline=True).add_field(name='Nay', value=f'```{0}```'.format("\n".join(nay_voters)), inline=True)
        await self.update()
       
    async def clear_votes(self):
        await self.message.clear_reactions()