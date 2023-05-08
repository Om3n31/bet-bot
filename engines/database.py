from pymongo import MongoClient
from pymongo.collection import Collection
from livebet import LiveBet
from discord import Member
from bettinguser import BettingUser
import time
from typing import Dict
import os

class Database:
    
    mongo_uri: str
    
    def __init__(self) -> None:
        self.mongo_uri = os.getenv('MONGO_URI')
        pass
    
    async def insert_user(self, user: BettingUser):
        mongo = self.get_conn()
        if not mongo['bet-bot']['users'].find_one({'id': user.id}):
           mongo['bet-bot']['users'].insert_one(self.user_to_document(user))
        mongo.close()
    
    async def insert_bet(self, bet: LiveBet):
        mongo = self.get_conn()
        if not mongo['bet-bot']['bets'].find_one({'id': bet.id}):
           mongo['bet-bot']['bets'].insert_one(self.bet_to_document(bet))
        mongo.close()
        pass
    
    def user_to_document(self, user: Member) -> Dict:
        return {
            'id': user.id,
            'name': user.nick,
            'balance': 5000,
            'punish_count': 0,
            'grace_count': 0,
            'wins': 0,
            'losses': 0
        }
    
    def get_collection(self, collection: str) -> Collection:
        return self.get_conn()['bet-bot'][collection]
        
    def update_user_balance(self, user: Member, amount: float):
        try:
            mongo = self.get_conn()
            usr = mongo['bet-bot']['users'].find_one({'id': user.id})
            balance = float(usr.balance)
            if user:
                mongo['bet-bot']['users'].update_one({'id':f'{user.id}'}, {'$set': {'balance':f'{balance + amount}'}})
        except Exception as e:
            print(e)
        pass
    
    def bet_to_document(self, bet: LiveBet) -> Dict:
        claims = []
        for claim in bet.claims:
            claims.append(
                {
                    'claim_text': claim.claim_text,
                    'main_bettor': {
                        'id': claim.owner.id,
                        'name': claim.owner.user.nick,
                        'amount': claim.owner.amount
                    },
                    'minor_bettors': len(claim.minor_bettors)
                }
            )
        return {
            'id': bet.id,
            'thread': bet.thread,
            'timestamp': int(time.time()),
            'winning_claim': bet.winning_claim,
            'claims': claims,
            'pot': bet.pot
            
        }
    def get_conn(self) -> MongoClient:
        return MongoClient(self.mongo_uri)