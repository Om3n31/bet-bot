from typing import List, Dict
from livebet import LiveBet
from vote import Vote
from interfaces.reaction_strategy_interface import ReactionStrategyInterface
from interfaces.reactable_interace import ReactableInterface
# from reactables.betbox_reactable import BetBoxReactable
# from reactables.bet_votebox_reactable import BetVoteboxReactable

class Bank:
    _instance = None
    balances: Dict[int, float]
    bets: List[Dict[str, LiveBet]]
    message_id_bet_id: List[Dict[int, str]]
    votes: List[Dict[int, Vote]]
    votebox_message_id: List[int]
    reaction_strategies: Dict[int, ReactionStrategyInterface]
    reactables: List[Dict[int, ReactableInterface]]
    
    def __init__(self):
        pass

    
    def __new__(self):
        if self._instance is None:
            self._instance = super().__new__(self)
            self.balances = {}
            self.bets = {}
            self.message_id_bet_id = {}
            self.votebox_message_id = []
            self.votes = {}
            self.reaction_strategies = {}
            self.reactables = []
        return self._instance
    
    def get_bet_from_message_id(self, message_id: int) -> LiveBet:
        print(self.message_id_bet_id)
        bet_id = self.message_id_bet_id[message_id]
        return self.bets[bet_id]
    
    def get_bet_id_from_message_id(self, message_id: int) -> str:
        return self.message_id_bet_id[message_id]
    
    def init_balance(self, id: int, amount: float):
        self.balances[id] = amount
        
    def add_to_balance(self, id: int, amount: float):
        self.balances[id] += amount
    
    def register_bet(self, bet: LiveBet) -> str:
        # bet_box_mid = bet.vote_box.message.id
        # vote_box_mid = bet.bet_box.message.id
        self.bets[bet.id] = bet
        # self.reactables.append({'key': bet_box_mid, 'reactable': BetBoxReactable(bet)})
        # self.reactables.append({'key': vote_box_mid, 'reactable': BetVoteboxReactable(bet)})
        self.message_id_bet_id[bet.message_id] = bet.id
        self.message_id_bet_id[bet.vote_box.message.id] = bet.id
        self.votebox_message_id.append(bet.vote_box.message.id)
        return bet.id
    
    def register_reactable(self, reactable: ReactableInterface):
        self.reactables.append({'key': reactable.message_id(), 'reactable': reactable})
    
    def get_reactable(self, message_id: int) -> ReactableInterface | None:
        reactables = [reactable for reactable in self.reactables if reactable.get('key') == message_id]
        if len(reactables) == 0:
            return None
        return reactables[0].get('reactable')
    
    def message_id_to_strategy(self, message_id: int) -> str:
        
        pass
    
    def register_vote(self, vote: Vote, message_id: int):
        self.votes[message_id] = vote
        
    def register_strategy(self, message_id: int, strategy: ReactionStrategyInterface):
        self.reaction_strategies[message_id] = strategy
        
    def get_strategy(self, message_id: int) -> ReactionStrategyInterface:
        return self.reaction_strategies[message_id]
        
    def add_votebox_message_id(self, id: int):
        self.votebox_message_id.append(id)