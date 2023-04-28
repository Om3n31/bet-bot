from bettinguser import BettingUser
from typing import List

class Claim:
    id: int
    owner: BettingUser
    minor_bettors: List[int]
    claim_text: str
    pot: float
    original_pot: float
    minor_amount: float
    vote_weight: float
    
    def __init__(self, owner: BettingUser, id: int, claim_text: str, amount: float, minorBettorModifier: int):
        self.owner = owner
        self.id = id
        self.claim_text = claim_text
        self.vote_weight = 0.
        self.pot = amount
        self.minor_bettors = []
        self.original_pot = amount
        self.minor_amount = (amount/100)*minorBettorModifier
    
    def update_pot(self, amount: float):
        self.pot += amount
    
    def add_minor_bettor(self, minorBettor: BettingUser):
        amount = (self.original_pot/100)*20
        self.update_pot(amount)
        self.minor_bettors.append(minorBettor.id)
        
    def remove_minor_bettor(self, minorBettor: BettingUser):
        amount = (self.original_pot/100)*20
        self.update_pot(amount*-1)
        self.minor_bettors.remove(minorBettor.id)
        