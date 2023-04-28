from typing import List, Dict
from livebet import LiveBet
from tools.tools import generate_hash

class Bank:
    _instance = None
    balances: List[Dict[int, float]]
    bets: List[Dict[str, LiveBet]]
    message_id_bet_id: List[Dict[int, str]]
    votebox_message_id: List[int]
    
    def __init__(self):
        self.balances = {}
        self.bets = {}
        self.message_id_bet_id = {}
        self.votebox_message_id = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_bet_from_message_id(self, message_id: int) -> LiveBet:
        bet_id = self.message_id_bet_id[message_id]
        return self.bets[bet_id]
    
    def get_bet_id_from_message_id(self, message_id: int) -> str:
        return self.message_id_bet_id[message_id]
    
    def register_bet(self, bet: LiveBet) -> str:
        self.bets[bet.id] = bet
        self.message_id_bet_id[bet.message_id] = bet.id
        self.message_id_bet_id[bet.vote_box.message.id] = bet.id
        self.votebox_message_id.append(bet.vote_box.message.id)
        return bet.id
        
    def add_votebox_message_id(self, id: int):
        self.votebox_message_id.append(id)