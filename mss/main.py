import db

# 3, 5, 8, 13, 21, 34, 55, 89
def handler(event=None, context=None):
    notionDB = db.NotionDB() 
    options = notionDB.get_options()
    notionDB.update_properties(
        options.query('OPTION == "UPDATE"').iloc[-1].ID,
        dict(VALUE=notionDB.number_mapper(1))
    )
    symbols = notionDB.get_symbols()
    df_score = db.FinanceDB.get_score(
        [(row.ID, row.SYMBOL) for _, row in symbols.iterrows()])
    print(df_score)
    # 노션 DB 업데이트
    for _, row in df_score.iterrows():
        notionDB.update_properties(row.ID, dict(
            NAME = notionDB.text_mapper(row.NAME),
            MOMENTUM = notionDB.number_mapper(row.MOMENTUM),
            RISK = notionDB.number_mapper(row.RISK),))
    notionDB.update_properties(
        options.query('OPTION == "UPDATE"').iloc[-1].ID,
        dict(VALUE=notionDB.number_mapper(0))
    )

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': '{"message": "OK"}'
    }

if __name__ == '__main__':
    handler()