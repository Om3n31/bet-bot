from typing import List
from claim import Claim
from engines.bank import Bank

class BetResolver:
    main_bettor_modifier: int
    minor_bettor_modifier: int
    bank: Bank
    claims: List[Claim]
    winner_claim_id: int
    
    def __init__(self, claims: List[Claim]):
        self.main_bettor_modifier = 120
        self.minor_bettor_modifier = 20
        self.bank = Bank()
        self.claims = claims
        self.winner_claim_id = 0
    
    def vote_count(self) -> int:
        return max(self.claims, key=lambda claim: claim.vote_weight).id
        
    def resolve(self, winner_claim_id: int) -> bool:
        claim = self.claims[winner_claim_id]
        if claim:
            if len(claim.minor_bettors) > 0:
                for minor_bettor in claim.minor_bettors:
                    self.bank.balances[minor_bettor] += (claim.minor_amount) + self.get_resolution_minor_gains(claim)
                self.bank.balances[claim.owner.id] += (claim.original_pot) + self.get_resolution_major_gains(claim)
                return True
            self.bank.balances[claim.owner.id] += self.get_pot()
            return True
        return False
    
    def get_pot(self) -> float:
        total = 0.
        for claim in self.claims:
            total += claim.pot
        return total
    
    def get_gains(self, winning_claim_id: int) -> float:
        return sum([cl.pot for cl in self.claims if cl.id is not winning_claim_id])
    
    def get_resolution_minor_gains(self, winning_claim: Claim) -> float:
        return round(((self.get_gains(winning_claim.id)/100)*self.main_bettor_modifier)/len(winning_claim.minor_bettors),2)
    
    def get_resolution_major_gains(self, winning_claim: Claim) -> float:
        return round((self.get_gains(winning_claim.id)/100)*(100-self.main_bettor_modifier),2)
    