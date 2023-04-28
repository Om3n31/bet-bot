import time
import json
from typing import List, Dict
import os

class Counter:
    _instance = None

    def __init__(self):
        self.data = []
        self.filename = os.path.join(os.getcwd(), "data","query_counter.json")
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def can_search_google(self) -> bool:
        now = int(time.time())
        cutoff = now - 24 * 3600
        try:
            data = self.get_data()
            timestamps = self.get_timestamps(data)
            last_24hours_count = len([timestamp for timestamp in timestamps if timestamp >= cutoff])
            if last_24hours_count < 100:
                data["queries"].append(now)
                self.set_timestamp(data)
                return True
            return False     
        except Exception as e:
            print(e)
                
    def get_data(self) -> Dict[str, List[int]]:
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except Exception as e:
            print(e)
    
    def get_timestamps(self, data) -> List[int]:
        return [int(value) for value in data["queries"]]
    
    def set_timestamp(self, data):
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file)
        except Exception as e:
            print(e)
    
    def searches_remaining(self) -> int:
        now = int(time.time())
        cutoff = now - 24 * 3600
        return 100 - len([t for t in self.get_timestamps(self.get_data()) if t >= cutoff])