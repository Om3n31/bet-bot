from discord import Embed, Message, Interaction, TextChannel
from tools.emojis import *
from typing import Dict, Union
from engines.googlelimiter import Counter

class VoteBox(Embed):
    bet_id: str
    message: Message
    def __init__(self, bet_id: str):
        super().__init__(title="", description=f"", color=0x36393F)
        self.bet_id = bet_id
        self.set_footer(text=f"You can vote for a claim under this box.")

    async def print(self, channel: TextChannel):
        message = await channel.send(embed=self)
        self.message = message
    
    async def post_claim_footer(self):
        searches_left = Counter().searches_remaining()
        self.set_footer(text=f"Vote for a claim    -    Searches left: {searches_left}")
        await self.update()
    
    async def update(self):
        await self.message.edit(embed=self)
        
    async def add_search_emoji(self):
        await self.message.remove_reaction(SEARCH_REACTION, self.message.author)
        await self.message.add_reaction(SEARCH_REACTION)
    
    async def add_vote_slot(self, claim_id: int):
       await self.message.add_reaction(INT_EMOJI_ENUM[claim_id])
       
    async def insert_result(self, result: Dict[str, str]):
        self.add_field(name="", value=f"```{result['snippet']}```\n{result['url']}", inline=False)
        await self.update()
    
    async def clear_votes(self):
        await self.message.clear_reactions()