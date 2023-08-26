import pandas as pd
import requests
import os
from io import BytesIO

class FinanceDB:
    prices = {}
    fibonacci = (8, 13, 21, 34, 55)
    names = None

    @classmethod
    def get_etfs(cls):
        URL = 'https://finance.naver.com/api/sise/etfItemList.nhn'
        data = requests.get(URL).json()\
            .get('result').get('etfItemList')
        mapper = lambda x: {
            'itemcode': x.get('itemcode'),
            'itemname': x.get('itemname')}
        df = pd.DataFrame(list(map(mapper, data)))\
            .rename(columns=dict(
                itemcode='SYMBOL',
                itemname='NAME'))
        cls.names = df.copy()
        return df
    
    @classmethod
    def get_price(cls, symbol):
        if symbol in cls.prices:
            return cls.prices[symbol]
        URL = 'https://api.finance.naver.com/siseJson.naver'
        params = dict(
            symbol=symbol, requestType=1,
            startTime='20230101', endTime='20991231', timeframe='day'
        )
        content = requests.get(URL, params).content
        with BytesIO(content) as byte_io:
            df = pd.read_csv(byte_io).iloc[:-1, 0:5]
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close']
        df.Date = df.Date.str.extract(r'(\d{8})')
        df.Date = pd.to_datetime(df.Date).dt.date
        df.set_index('Date', inplace=True)
        cls.prices[symbol] = df
        return df
    
    @classmethod
    def get_momentum(cls, symbol):
        price = cls.get_price(symbol)
        # 8, 13, 21, 34, 55
        return (
            sum([price.Close.rolling(f)\
            .apply(lambda x: (x[-1] / x[0]))\
            .sub(1).div(f).add(1).pow(252).sub(1)
            for f in cls.fibonacci])\
            .div(len(cls.fibonacci))\
            .round(3).iloc[-1])

    @classmethod
    def get_risk(cls, symbol):
        price = cls.get_price(symbol)
        concat = lambda x, y: pd.concat([x, y], axis=1)
        th = concat(price.High, price.Close.shift(1)).max(axis=1)
        tl = concat(price.Low, price.Close.shift(1)).min(axis=1)
        tr = th - tl
        atr = tr.ewm(max(cls.fibonacci)).mean()
        aatr = atr / price.Close
        return aatr.round(3).iloc[-1]
    
    @classmethod
    def get_score(cls, symbols):
        cls.get_etfs()
        return pd.DataFrame([dict(
            ID=ID, SYMBOL=symbol,
            NAME=cls.names.loc[cls.names.SYMBOL == symbol, 'NAME'].iloc[-1],
            MOMENTUM=cls.get_momentum(symbol),
            RISK=cls.get_risk(symbol),
        ) for ID, symbol in symbols])\
        .sort_values('MOMENTUM', ascending=False)\
        .reset_index(drop=True)

class NotionDB:
    def __init__(self) -> None:
        self.load_notion_api_key()
        self.load_item_db_id()
        self.load_option_db_id()

    def send_requests(self, method, URL, json={}):
        headers = {
            'Authorization' : f'Bearer {self.notion_api_key}',
            'Notion-Version' : '2022-06-28'
        }
        return requests.request(method, URL,
                                json=json, headers=headers)
    
    def get_options(self) -> pd.DataFrame:
        URL = f'https://api.notion.com/v1/databases/{self.option_db_id}/query'
        res = self.send_requests('POST', URL).json()
        mapper = lambda x: {
            'OPTION': x.get('id'),
            'VALUE': x.get('properties').get('SYMBOL').get('title')[0]['plain_text'],
        }
        symbols = pd.DataFrame(list(map(mapper, res.get('results'))))
        return symbols        
    
    def get_symbols(self) -> pd.DataFrame:
        URL = f'https://api.notion.com/v1/databases/{self.item_db_id}/query'
        res = self.send_requests('POST', URL).json()
        mapper = lambda x: {
            'ID': x.get('id'),
            'SYMBOL': x.get('properties').get('SYMBOL').get('title')[0]['plain_text'],
        }
        symbols = pd.DataFrame(list(map(mapper, res.get('results'))))
        return symbols
    
    def get_options(self) -> pd.DataFrame:
        URL = f'https://api.notion.com/v1/databases/{self.option_db_id}/query'
        res = self.send_requests('POST', URL).json()
        mapper = lambda x: {
            'ID': x.get('id'),
            'OPTION': x.get('properties').get('OPTION').get('title')[0]['plain_text'],
            'VALUE': x.get('properties').get('VALUE').get('number')
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

    def load_item_db_id(self):
        self.item_db_id = os.getenv('mss_item_db_id')
        if not self.item_db_id:
            raise Exception('NO ITEM DB ID') 
        
    def load_option_db_id(self):
        self.option_db_id = os.getenv('mss_option_db_id')
        if not self.option_db_id:
            raise Exception('NO OPTION DB ID') 
        
    @classmethod
    def text_mapper(cls, content):
        return {'rich_text': [{'text':{'content': content}}]}

    @classmethod
    def number_mapper(cls, value):
        return {'number': value}