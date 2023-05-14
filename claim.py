from bettinguser import BettingUser
from typing import List, Dict

class Claim:
    id: int
    owner: BettingUser
    minor_bettors: List[int]
    tmp_bettors: List[Dict[int,BettingUser]]
    extra_bettors: List[Dict[int,BettingUser]]
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
        self.tmp_bettors = []
        self.extra_bettors = []
    
    def update_pot(self, amount: float):
        self.pot += amount
    
    def add_minor_bettor(self, minorBettor: BettingUser):
        amount = (self.original_pot/100)*20
        self.update_pot(amount)
        self.minor_bettors.append(minorBettor.id)
        
    def add_tmp_bettor(self, extra_bettor: BettingUser):
        print("in tmp bettor")
        self.tmp_bettors.append({'id': extra_bettor.id, 'bettor': extra_bettor})
        print(self.tmp_bettors)
        
    def update_tmp_bettor_amount(self, bettor_id: int, amount: float):
        self.tmp_bettors[bettor_id]['bettor']
        
    def lock_extra_bettor(self, bettor_id: int):
        bettor = [bettor for bettor in self.tmp_bettors if bettor.get('id') == bettor_id][0].get('bettor')
        self.extra_bettors.append({'id': bettor.id, 'bettor': bettor})
        self.tmp_bettors.remove(bettor)
        print(self.extra_bettors)
        print(self.tmp_bettors)
        self.update_pot(bettor.amount)
        
    def has_user_claimed(self, bettor_id: int) -> bool:
        owner = bettor_id == self.owner.id
        extra_bettor = len([xbettor for xbettor in self.extra_bettors if xbettor.get('id') == bettor_id]) == 1
        tmp_bettor = len([tbettor for tbettor in self.tmp_bettors if tbettor.get('id') == bettor_id]) == 1
        return owner or extra_bettor or tmp_bettor
        
    def remove_minor_bettor(self, minorBettor: BettingUser):
        amount = (self.original_pot/100)*20
        self.update_pot(amount*-1)
        self.minor_bettors.remove(minorBettor.id)
        