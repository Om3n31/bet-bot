import discord
from interfaces.vote_strategy_interface import VoteStrategyInterface
from discord import Member, Interaction
from typing import List
from engines.database import Database
from embeds.votebox_vote import VoteBoxVote

class PunishStrategy(VoteStrategyInterface):
    
    interaction: Interaction
    votebox: VoteBoxVote
    
    def __init__(self, interaction: Interaction):
        self.interaction = interaction
        self.options = [option for option in self.interaction.data.get('options')]
        print([option for option in self.options if option.get('name') == 'amount'])
        self.amount = [option for option in self.options if option.get('name') == 'amount'][0]['value']
    
    def vote_owner(self) -> Member:
        return self.interaction.user
    
    def vote_mentions(self) -> List[Member] | None:
        mentions = next((option for option in self.options if option.get('name') == 'users'), None)['value'].split(' ')
        return [discord.utils.get(self.interaction.guild.members, mention=mention) for mention in mentions]
    
    def vote_topic(self) -> str:
        return self.interaction.command.name

    def vote_content(self) -> str:
        return f'{self.vote_owner().nick} wants to punish {self.mentions_to_nicks()} for {self.amount} points.'
    
    def resolved_content(self) -> str:
        return f'{self.mentions_to_nicks()} {"were" if len(self.mentions_to_nicks()) > 1 else "was"} punished for {self.amount} points.'
    
    def mentions_to_nicks(self) -> List[str]:
        return ', '.join([user.nick for user in self.vote_mentions()])
    
    async def exec(self):
        db = Database().get_collection('users')
        for member in self.vote_mentions():
            balance = db.find_one({'id': member.id})['balance']
            new_balance = balance - float([option for option in self.options if option.get('name') == 'amount'][0]['value'])
            db.update_one({'id':member.id}, {'$set': {'balance': new_balance}})
    
    
    async def print(self):
        pass