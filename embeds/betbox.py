from discord import Embed, Message, Interaction, TextChannel
from discord.ext.commands import Context
from claim import Claim
from typing import Union

class BetBox(Embed):
    bet_id: str
    message: Message
    def __init__(self, author_nick: str, bet_id: str, thread: str):
        super().__init__(title=f"", description=f"", color=0xd4af37)
        self.bet_id = bet_id
        self.add_field(name=f"@{author_nick} started a new bet:", value=f"```{thread}\n```", inline=False)
        
    async def add_claim(self, claim_id: int, user_name: str, amount: float, claim_text: str):
        self.add_field(name="", value=f"```{claim_id+1} - {user_name} for {amount}\n{claim_text}```", inline=False)
        await self.update()

    async def print(self, channel: TextChannel):
        message = await channel.send(embed=self)
        self.message = message
    
    async def post_claim_footer(self):
        self.set_footer(text=f"Add a minor bet:")
        await self.update()
    
    async def update(self):
        await self.message.edit(embed=self)
        
    async def add_resolve_field(self, resolver: str, claim: Claim):
        self.add_field(name=f"{resolver} resolved the bet:", value=f"```{claim.owner.user.nick}: {claim.claim_text}```", inline=False)
        await self.update()