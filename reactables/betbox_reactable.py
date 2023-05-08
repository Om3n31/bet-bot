import discord
from interfaces.vote_strategy_interface import VoteStrategyInterface
from discord import Reaction, Message, Member
from typing import List
from engines.database import Database
from embeds.votebox_vote import VoteBoxVote
from interfaces.reactable_interace import ReactableInterface
from engines.bank import Bank
from livebet import LiveBet
from bettinguser import BettingUser

class BetBoxReactable(ReactableInterface):
    
    bet: LiveBet
    
    def __init__(self, bet: LiveBet):
        self.bet = bet
        pass
    
    def can_react(self, reaction: Reaction, user: Member):
        bet = Bank().get_bet_from_message_id(reaction.message.id)
        if bet.is_resolved or user.id in bet.betting_users:
            return False
        return True

    def add_reaction(self):
        pass
    
    def remove_reaction(self):
        pass
    
    def get_strategy(self):
        strategy = Bank().get_strategy(self.message.id)
        self.strategy = strategy
        return self.strategy
    
    async def exec(self):
        pass
    