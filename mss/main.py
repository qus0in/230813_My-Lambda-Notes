import db
from math import floor

# 3, 5, 8, 13, 21, 34, 55, 89
def handler(event=None, context=None):
    notionDB = db.NotionDB() 
    options = notionDB.get_options()
    budget = options.query('OPTION == "BUDGET"').iloc[-1].VALUE
    risk = options.query('OPTION == "RISK"').iloc[-1].VALUE
    symbols = notionDB.get_symbols()
    df_score = db.FinanceDB.get_score(
        [(row.ID, row.SYMBOL) for _, row in symbols.iterrows()])
    print(df_score)
    df_score['SCORE'] = df_score.apply(lambda row: floor(min(risk / row.RISK, 1) * row.MOMENTUM * 1000), axis=1).div(1000)
    df_score['UNIT'] = df_score.apply(lambda row: floor(min(risk / row.RISK, 1) * budget / 5 / 100000), axis=1).mul(100000)
    df_score.sort_values('SCORE', ascending=False, inplace=True)
    free_risk = df_score.query('SYMBOL == "357870"').iloc[-1].SCORE
    relative_momentum = df_score.head(6).iloc[-1].SCORE
    # 노션 DB 업데이트
    for _, row in df_score.iterrows():
        notionDB.update_properties(row.ID, dict(
            NAME = notionDB.text_mapper(row.NAME),
            MOMENTUM = notionDB.number_mapper(row.MOMENTUM),
            RISK = notionDB.number_mapper(row.RISK),
            SCORE = notionDB.number_mapper(row.SCORE),
            UNIT = notionDB.number_mapper(row.UNIT),
            SCREEN = notionDB.checkbox_mapper(row.SCORE > max(free_risk, relative_momentum))
        ))

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': '{"message": "OK"}'
    }

if __name__ == '__main__':
    handler()