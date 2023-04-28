from discord.ext import commands
from discord import Member, User


class BettingUser():
    id: int
    tier: int
    claim_id: int
    amount: float
    user: Member | User
    def __init__(bettingUser, id: int, user: Member,tier = 1, amount = 0):
        bettingUser.id = id
        bettingUser.user = user
        bettingUser.tier = tier
        bettingUser.amount = amount
        
    def set_id(bettingUser, id: int):
        bettingUser.id = id
    def set_user(bettingUser, user: Member | User):
        bettingUser.user = user
#TO GET THE CLAIM, USE THE CLAIM_ID AND FETCH IT FROM LIVEBET
@staticmethod
def BettingUserFromMember(user: Member | User) -> BettingUser:
    return BettingUser(user.id, user)