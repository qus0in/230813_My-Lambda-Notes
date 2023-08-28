from notion import Notion
from fsc import FSC
import pandas as pd

def handler(event=None, context=None):
    채권현황 = 채권현황_불러오기()
    print(채권현황.head())
    채권정보 = FSC.get_bond_info()
    채권정보.info()
    print(채권정보.head())

def 채권현황_불러오기():
    mapper = lambda x: {
        'ID': x.get('id'),
        'NAME': x.get('properties')\
            .get('NAME').get('title')[0]['plain_text'],
    }
    return Notion.get_data(Notion.채권현황_DB_ID, mapper)
    
if __name__ == '__main__':
    handler()