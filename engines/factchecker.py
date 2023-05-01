import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict


API_ERROR = "There was an issue with fetching claims for your query."

class FactChecker():
    _instance = None
    
    def __init__(self):
        pass
        
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def check(self, thread: str) -> str:
        try:
            return
            print("in factchecker")
            service = build("customsearch", "v1", developerKey=API_KEY)
            response = service.cse().list(q=thread, cx=CSE_ID, num=N_SEARCH_RESULTS, safe='active').execute()
            results: List[Dict[str, str]] = []
            for i, item in enumerate(response['items']):
                results.append({'snippet': item['snippet'], 'url': item['formattedUrl']})
            return results
        except HttpError as err:
            print (err)
            raise err
    
    