import discord
from interfaces.vote_strategy_interface import VoteStrategyInterface
from discord import Reaction, Embed, Member, Message
from typing import List
from engines.database import Database
from embeds.votebox_vote import VoteBoxVote
from interfaces.reactable_interace import ReactableInterface
from engines.bank import Bank
from livebet import LiveBet
from bettinguser import BettingUser
from tools.emojis import INT_EMOJI_ENUM

class BetVoteboxReactable(ReactableInterface, Embed):
    
    bet: LiveBet
    
    def __init__(self, bet: LiveBet):
        self.bet = bet
        self.m_id = bet.vote_box.message.id
        pass
    
    def message_id(self) -> int:
        return self.m_id
    
    def can_react(self, reaction: Reaction, user: Member):
        bet = Bank().get_bet_from_message_id(reaction.message.id)
        if bet.is_resolved or user.id in bet.betting_users:
            return False
        return True
    
    def can_reply(self, message: Message) -> bool:
        return False

    def emojis_used(self) -> set:
        return set(INT_EMOJI_ENUM)
    
    def on_add_reaction(self):
        
        pass
    
    def on_remove_reaction(self):
        pass
    
    def on_reply(self):
        pass
    
    def get_strategy(self):
        strategy = Bank().get_strategy(self.message.id)
        self.strategy = strategy
        return self.strategy
    
    async def exec(self):
        pass
    
    def get_amount_from_message(self, message: Message) -> float:
        content = self.get_content_from_message(message, False)
        return float(content.split(' ')[-1])
    
    def get_content_from_message(self, message: Message, has_amount: bool) -> str:
        mentions = self.get_mentions_from_message(message)
        if has_amount:
            dirty_message = message.content.split(' ')[:-1]
        else:
            dirty_message = message.content.split(' ')[1:]
        return ' '.join([x for x in dirty_message if x not in mentions])
    
    def get_mentions_from_message(self, message: Message) -> List[str]:
        return [m.mention for m in message.mentions]