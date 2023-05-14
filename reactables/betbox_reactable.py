import discord
from interfaces.vote_strategy_interface import VoteStrategyInterface
from discord import Reaction, Message, Member, RawReactionActionEvent
from typing import List
from interfaces.reactable_interace import ReactableInterface
from engines.bank import Bank
from livebet import LiveBet
from bettinguser import BettingUser, BettingUserFromMember
from tools.emojis import AMOUNT_EMOJI_VALUES, BET_AMOUNT_ENUM, INT_EMOJI_ENUM
from tools.tools import get_amount_from_message

class BetBoxReactable(ReactableInterface):
    
    bet: LiveBet
    
    def __init__(self, bet: LiveBet):
        self.bet = bet
        self.m_id = bet.bet_box.message.id
        pass
    
    def message_id(self) -> int:
        return self.m_id
    
    def can_react(self, event: RawReactionActionEvent):
        bank = Bank()
        bet = bank.get_bet_from_message_id(event.message_id)
        
        if bet.is_resolved or event.emoji not in self.emojis_used():
            return False
        user_claim = self.bet.user_claim(event.member.id)
        if event.emoji in INT_EMOJI_ENUM:
            if user_claim is not None:
                return False
            index = INT_EMOJI_ENUM.index(event.emoji)
            if index + 1 > bet.claim_count:
                return False
        if event.emoji in BET_AMOUNT_ENUM:
            #TODO: CHECK IF USER IS IN TMP BETTORS
            if user_claim is None:
                return False
            index = BET_AMOUNT_ENUM.index(event.emoji)
            if bank.balances[event.user_id] < AMOUNT_EMOJI_VALUES[index]:
                return False
        return True
    
    def can_reply(self, message: Message) -> bool:
        if self.bet.is_resolved:
            return False
        return True
    
    def emojis_used(self) -> set:
        return set(INT_EMOJI_ENUM).intersection(BET_AMOUNT_ENUM)
    
    def handle_reaction(self, reaction: Reaction, user: Member):
        pass
    
    def handle_reply(self, reaction: Reaction, user: Member):
        pass

    def on_add_reaction(self, event: RawReactionActionEvent):
        if event.emoji in BET_AMOUNT_ENUM:
            claim = self.bet.user_claim(event.user_id)
            bettor = [bettor for bettor in claim.tmp_bettors if bettor.get('id') == event.user_id][0].get('bettor')
            index = BET_AMOUNT_ENUM.index(event.emoji)
            bettor.amount += AMOUNT_EMOJI_VALUES[index]
            pass
        if event.emoji in INT_EMOJI_ENUM:
            index = BET_AMOUNT_ENUM.index(event.emoji)
            self.bet.claims[index].add_tmp_bettor(BettingUserFromMember(event.member))
            pass
        pass
    
    def on_remove_reaction(self):
        pass
    
    async def on_reply(self, member: Member, claim: str, amount: str, intent: str):
        bank = Bank()
        betting_user = BettingUserFromMember(member)
        try:
            amount = float(amount)
            if intent == 'add_claim':
                if not await self.new_claim(claim, amount, betting_user):
                    return False
            if intent == 'join_claim':
                pass
            return True
        except:
            return
        print(claim, amount)
        #HANDLE INTENT ?
        if member.id in self.bet.betting_users:
            #HANDLE REMOVE CLAIM
            return

        
        pass
    
    def get_strategy(self):
        strategy = Bank().get_strategy(self.message.id)
        self.strategy = strategy
        return self.strategy
    
    def register(self):
        pass
    
    async def exec(self):
        pass

    async def new_claim(self, claim_text: str, amount: float, betting_user: BettingUser):
        bank = Bank()
        print(bank.balances.get(betting_user.id))
        if bank.balances[betting_user.id] < amount:
            return False
        await self.bet.add_claim(claim_text, amount, betting_user)
        bank.balances[betting_user.id] -= amount
        await self.bet.bet_box.message.edit(embed=self.bet.bet_box)
        await self.bet.bet_box.message.add_reaction(INT_EMOJI_ENUM[self.bet.claim_count - 1])
        return True
    
    def join_claim(self):
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