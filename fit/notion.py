import pandas as pd
import requests
import os

class Notion:
    채권현황_DB_ID = '7634ac1547be404293e48393dc72a146'
    채권기록_DB_ID = '7214b17f1c4a4511996d4193d1df63cc'
    옵션_DB_ID = '2cafa7dc713d4738957fc6edb1e29b83'

    @classmethod
    def send_requests(cls, method, URL, json={}):
        notion_api_key = os.getenv('notion_api_key')
        if not notion_api_key:
            raise Exception('NO NOTION API KEY')

        headers = {
            'Authorization' : f'Bearer {notion_api_key}',
            'Content-Type': 'application/json',
            'Notion-Version' : '2022-06-28'
        }
        return requests.request(method, URL,
                                json=json, headers=headers)
    
    @classmethod
    def get_data(cls, db_id: str, mapper) -> pd.DataFrame:
        URL = f'https://api.notion.com/v1/databases/{db_id}/query'
        res = cls.send_requests('POST', URL).json()
        return pd.DataFrame(list(map(mapper, res.get('results'))))
    
    @classmethod
    def add_data(cls, db_id: str, properties):
        URL = f'https://api.notion.com/v1/pages'
        res = cls.send_requests('POST', URL,
                {'parent': { 'database_id' : db_id } ,'properties': properties})
        if res.status_code != 200:
            raise Exception(res.json().get('message'))

    @classmethod
    def update_properties(cls, page_id, properties):
        URL = f"https://api.notion.com/v1/pages/{page_id}"
        print(page_id, properties)
        res = cls.send_requests('PATCH', URL,
                                 {'properties': properties})
        if res.status_code != 200:
            raise Exception(res.json().get('message'))
    
    @classmethod
    def text_mapper(cls, content):
        return {'rich_text': [{'text':{'content': content}}]}

    @classmethod
    def number_mapper(cls, value):
        return {'number': value}
    
    @classmethod
    def checkbox_mapper(cls, value):
        return {'checkbox': bool(value)}
    
    @classmethod
    def date_mapper(cls, value):
        return {'date': {'start': value}}
    
    @classmethod
    def title_mapper(cls, content):
        return {'title': [{'text':{'content': content}}]}