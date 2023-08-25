import os
import requests
import pandas as pd

def handler(event: None, context: None):
    notionDB = NotionDB()
    symbols = notionDB.get_symbols()
    etfs = FinanceDB.get_etfs()
    df = symbols.merge(etfs, how='inner', left_on='SYMBOL', right_on='itemcode').iloc[:, [0, 2]]
    print(df)
    return df.to_json()

class FinanceDB:
    def get_etfs():
        URL = 'https://finance.naver.com/api/sise/etfItemList.nhn'
        params = dict(
            etfType=0,
            targetColumn='market_sum',
            sortOrder='desc'
        )
        data = requests.get(URL, params=params).json()\
            .get('result').get('etfItemList')
        mapper = lambda x: {'itemcode': x.get('itemcode'), 'itemname': x.get('itemname')}
        df = pd.DataFrame(list(map(mapper, data))).rename(columns={'itemname': 'NAME'})
        return df

class NotionDB:
    def __init__(self) -> None:
        self.load_notion_api_key()
        self.load_db_id()

    def send_requests(self, method, URL):
        return requests.request(method, URL, headers={
            'Authorization' : f'Bearer {self.notion_api_key}',
            'Notion-Version' : '2022-06-28'
        })

    def get_symbols(self) -> pd.DataFrame:
        URL = f'https://api.notion.com/v1/databases/{self.db_id}/query'
        res = self.send_requests('POST', URL).json()
        mapper = lambda x: {'SYMBOL': x.get('properties').get('SYMBOL').get('title')[0]['plain_text']}
        symbols = pd.DataFrame(list(map(mapper, res.get('results'))))
        return symbols

    def load_notion_api_key(self):
        self.notion_api_key = os.getenv('notion_api_key')
        if not self.notion_api_key:
            raise Exception('NO NOTION API KEY')

    def load_db_id(self):
        self.db_id = os.getenv('mss_item_db_id')
        if not self.db_id:
            raise Exception('NO DB ID') 

if __name__ == '__main__':
    handler('', '')