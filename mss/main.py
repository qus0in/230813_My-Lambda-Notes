import os
import requests
import pandas as pd

def handler(event: None, context: None):
    notionDB = NotionDB()
    symbols = notionDB.get_symbols()
    return symbols.to_json()

class NotionDB:
    def __init__(self) -> None:
        self.load_notion_api_key()
        self.load_db_id()

    def send_requests(self, URL):
        return requests.post(URL, headers={
            'Authorization' : f'Bearer {self.notion_api_key}',
            'Notion-Version' : '2022-06-28'
        })

    def get_symbols(self) -> pd.DataFrame:
        URL = f'https://api.notion.com/v1/databases/{self.db_id}/query'
        res = self.send_requests(URL).json()
        mapper = lambda x: x.get('properties').get('SYMBOL').get('title')[0]['plain_text']
        symbols = pd.DataFrame({'SYMBOL': list(map(mapper, res.get('results')))})
        return symbols

    def load_notion_api_key(self):
        self.notion_api_key = os.getenv('notion_api_key')
        if not self.notion_api_key:
            raise Exception('NO NOTION API KEY')

    def load_db_id(self):
        self.db_id = os.getenv('mss_item_db_id')
        if not self.db_id:
            raise Exception('NO DB ID') 
