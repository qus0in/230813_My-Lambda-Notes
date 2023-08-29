from notion import Notion
from fsc import FSC
import pandas as pd

def handler(event=None, context=None):
    채권기록_최신날짜 = 채권기록_날짜확인()
    # print(채권기록_최신날짜)
    try:
        채권정보 = FSC.get_bond_info()
        # 채권정보.info()
        # print(채권정보.head())
        채권정보_최신날짜 = 채권정보.DATE.unique().max().strftime('%Y-%m-%d')
        print(채권기록_최신날짜, 채권정보_최신날짜)
        if 채권기록_최신날짜 < 채권정보_최신날짜:
            print('* 채권기록 저장 진행')
            채권기록_저장하기(채권정보)
            채권기록_날짜갱신(채권정보_최신날짜)
        else:
            print('* 채권기록 저장 생략')
        채권현황 = 채권현황_불러오기()
        # print(채권현황.head())
        채권현황_시세 = pd.merge(채권현황, 채권정보, how='inner', on='NAME')
        # print(채권현황_시세.head())
        채권현황_수정하기(채권현황_시세)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': '{"message": "OK"}'
        }
    except Exception as e:
        print(e)
        return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': f'{"message": {e}}'
        }

def 채권현황_불러오기():
    mapper = lambda x: {
        'ID': x.get('id'),
        'NAME': x.get('properties')\
            .get('NAME').get('title')[0]['plain_text'],
    }
    return Notion.get_data(Notion.채권현황_DB_ID, mapper)

def 채권기록_날짜확인():
    mapper = lambda x: {
        'ID': x.get('id'),
        'DATE': x.get('properties')\
            .get('VALUE').get('date').get('start'),
    }
    data = Notion.get_data(Notion.옵션_DB_ID, mapper)
    # print(data.ID)
    return data.DATE.unique().max()

def 채권기록_날짜갱신(채권정보_최신날짜):
    Notion.update_properties('cfa4c645-4f3e-4002-a831-022f3e1e334e',
        dict(
            VALUE=Notion.date_mapper(채권정보_최신날짜)
        ))
    pass

def 채권기록_저장하기(채권정보):
    for _, row in 채권정보.iterrows():
        print(row.NAME)
        Notion.add_data(Notion.채권기록_DB_ID, dict(
            NAME=Notion.title_mapper(row.NAME),
            DATE=Notion.date_mapper(row.DATE.strftime('%Y-%m-%d')),
            VOLUME=Notion.number_mapper(row.VOLUME),
            PRICE=Notion.number_mapper(row.PRICE),
            BENEFIT=Notion.number_mapper(row.BENEFIT),
            INTEREST=Notion.number_mapper(row.INTEREST),
            EXPIRE=Notion.date_mapper(row.EXPIRE.strftime('%Y-%m-%d') if not pd.isna(row.EXPIRE) else '2099-12-31'),
            KIS=Notion.checkbox_mapper(row.KIS),
            KBP=Notion.checkbox_mapper(row.KBP),
            NICE=Notion.checkbox_mapper(row.NICE),
        ))

def 채권현황_수정하기(채권현황_시세):
    for _, row in 채권현황_시세.iterrows():
        print(row.NAME)
        Notion.update_properties(row.ID, dict(
            PRICE=Notion.number_mapper(row.PRICE)
        ))

if __name__ == '__main__':
    handler()