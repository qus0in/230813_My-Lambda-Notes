from notion import Notion

def handler(event=None, context=None):
    notion = Notion()
    채권현황 = 채권현황_불러오기(notion)
    print(채권현황)

def 채권현황_불러오기(notion):
    채권현황_DB_ID = '7634ac1547be404293e48393dc72a146'
    mapper = lambda x: {
        'ID': x.get('id'),
        'NAME': x.get('properties')\
            .get('NAME').get('title')[0]['plain_text'],
    }
    notion.get_data(채권현황_DB_ID, mapper)

if __name__ == '__main__':
    handler()