from discord.ext import commands
from discord import Member, User


class BettingUser():
    id: int
    tier: int
    claim_id: int
    amount: float
    user: Member | User
    def __init__(self, user: Member, tier = 1, amount = 0):
        self.id = user.id
        self.user = user
        self.tier = tier
        self.amount = amount
        
    def set_id(self, id: int):
        self.id = id
    def set_user(self, user: Member | User):
        self.user = user
#TO GET THE CLAIM, USE THE CLAIM_ID AND FETCH IT FROM LIVEBET
@staticmethod
def BettingUserFromMember(user: Member | User) -> BettingUser:
    return BettingUser(user)