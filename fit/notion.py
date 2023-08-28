import pandas as pd
import requests
import os

class Notion:
    def __init__(self) -> None:
        self.load_notion_api_key()

    def send_requests(self, method, URL, json={}):
        headers = {
            'Authorization' : f'Bearer {self.notion_api_key}',
            'Content-Type': 'application/json',
            'Notion-Version' : '2022-06-28'
        }
        return requests.request(method, URL,
                                json=json, headers=headers)
    
    def get_data(self, db_id, mapper) -> pd.DataFrame:
        URL = f'https://api.notion.com/v1/databases/{db_id}/query'
        res = self.send_requests('POST', URL).json()
        return pd.DataFrame(list(map(mapper, res.get('results'))))
    
    def update_properties(self, page_id, properties):
        URL = f"https://api.notion.com/v1/pages/{page_id}"
        print(page_id, properties)
        res = self.send_requests('PATCH', URL,
                                 {'properties': properties})
        if res.status_code != 200:
            raise Exception(res.json().get('message'))
    
    def load_notion_api_key(self):
        self.notion_api_key = os.getenv('notion_api_key')
        if not self.notion_api_key:
            raise Exception('NO NOTION API KEY')

    @classmethod
    def text_mapper(cls, content):
        return {'rich_text': [{'text':{'content': content}}]}

    @classmethod
    def number_mapper(cls, value):
        return {'number': value}
    
    @classmethod
    def checkbox_mapper(cls, value):
        return {'checkbox': bool(value)}