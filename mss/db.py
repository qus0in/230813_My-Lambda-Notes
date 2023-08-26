import pandas as pd
import requests
import os

class FinanceDB:
    def get_etfs():
        URL = 'https://finance.naver.com/api/sise/etfItemList.nhn'
        data = requests.get(URL).json()\
            .get('result').get('etfItemList')
        mapper = lambda x: {'itemcode': x.get('itemcode'), 'itemname': x.get('itemname')}
        df = pd.DataFrame(list(map(mapper, data))).rename(columns={'itemname': 'NAME'})
        return df

class NotionDB:
    def __init__(self) -> None:
        self.load_notion_api_key()
        self.load_db_id()

    def send_requests(self, method, URL, json={}):
        headers = {
            'Authorization' : f'Bearer {self.notion_api_key}',
            'Notion-Version' : '2022-06-28'
        }
        return requests.request(method, URL,
                                json=json, headers=headers)
    
    def get_symbols(self) -> pd.DataFrame:
        URL = f'https://api.notion.com/v1/databases/{self.db_id}/query'
        res = self.send_requests('POST', URL).json()
        mapper = lambda x: {
            'ID': x.get('id'),
            'SYMBOL': x.get('properties').get('SYMBOL').get('title')[0]['plain_text'],
        }
        symbols = pd.DataFrame(list(map(mapper, res.get('results'))))
        return symbols
    
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

    def load_db_id(self):
        self.db_id = os.getenv('mss_item_db_id')
        if not self.db_id:
            raise Exception('NO DB ID') 
