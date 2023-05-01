from bettinguser import BettingUser
from typing import List
from claim import Claim
from discord.ext.commands import Context
from embeds.betbox import BetBox
from embeds.votebox import VoteBox
from tools.tools import *
from engines.factchecker import FactChecker

class LiveBet:
    bet_box: BetBox
    vote_box: VoteBox
    id: str
    message_id: int
    creator_id: int
    claims: List[Claim]
    claim_count: int
    betting_users: List[int]
    main_bettor: List[int]
    main_bettor_modifier: int
    minor_bettor_modifier: int
    thread: str
    is_resolved: bool
    is_searched: bool
    winning_claim: int
    pot: float
    
    def __init__(self, ctx: Context, thread: str):
        hash_id = generate_hash(8)
        self.creator_id = ctx.author.id
        self.claims = []
        self.betting_users = []
        self.thread = thread
        self.id = hash_id
        self.claim_count = 0
        self.is_resolved = False
        self.is_searched = False
        self.main_bettor = []
        self.main_bettor_modifier = 120
        self.minor_bettor_modifier = 20
        self.bet_box = {}
        self.vote_box = {}
        self.winning_claim = None
        self.pot = 0.
    
    async def add_claim(self, claim_text: str, amount: float, betting_user: BettingUser) -> bool:
        if self.claim_count < 9:
            betting_user.amount = self.claim_amount_resolve(betting_user.id, amount)
            claim = Claim(betting_user, self.claim_count, claim_text, betting_user.amount, self.minor_bettor_modifier)
            self.claims.append(claim)
            self.betting_users.append(betting_user.id)
            await self.vote_box.add_vote_slot(self.claim_count)
            await self.vote_box.add_search_emoji()
            if self.claim_count == 0:
                await self.set_box_footers()
            await self.bet_box.add_claim(self.claim_count, betting_user.user.nick, amount, claim_text)
            print(f"Added claim number {self.claim_count} to bet {self.id}.")
            self.claim_count += 1
            return True
        return False
    
    async def init_boxes(self, ctx: Context):
        self.bet_box = BetBox(ctx, self.id, self.thread)
        await self.bet_box.print(ctx)
        self.vote_box = VoteBox(self.id)
        await self.vote_box.print(ctx)
        self.message_id = self.bet_box.message.id
        
    async def set_box_footers(self):
        await self.bet_box.post_claim_footer()
        await self.vote_box.post_claim_footer()
    
    def add_main_bettor(self, main_bettor: BettingUser):
        self.main_bettor.append(main_bettor.id)
        print(f"Added main bettor {main_bettor.user.nick} ({main_bettor.id}) to bet {self.id}")
    
    def add_minor_bettor(self, minor_bettor: BettingUser, claim_id: int):
        self.betting_users.append(minor_bettor.id)
        claim = self.get_claim(claim_id)
        claim.add_minor_bettor(minor_bettor)
        print(f"Added minor bettor {minor_bettor.user.nick} ({minor_bettor.id}) to claim {claim_id + 1}.")
    
    async def display_result(self):
        results = FactChecker().check(self.thread)
        for result in results:
            await self.vote_box.insert_result(result)
            
    
    def remove_minor_bettor(self, minor_bettor: BettingUser, claim_id: int):
        self.betting_users.remove(minor_bettor.id)
        claim = self.get_claim(claim_id)
        claim.remove_minor_bettor(minor_bettor)
    
    def claim_amount_resolve(self, user_id: int, amount: float) -> float:
        if user_id in self.main_bettor:
            amount = (amount/100)*self.main_bettor_modifier
        return amount
            
    def get_claim(self, claim_id: int) -> Claim:
        return self.claims[claim_id]
    
    def set_pot(self, amount: float):
        self.pot = amount