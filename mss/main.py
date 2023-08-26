import db

def handler(event=None, context=None):
    notionDB = db.NotionDB()
    symbols = notionDB.get_symbols()
    etfs = db.FinanceDB.get_etfs().rename(columns={'itemcode':'SYMBOL'})
    df = symbols.merge(etfs, how='inner')
    print(df)
    for _, row in df.iterrows():
        notionDB.update_properties(
            row.ID,
            {'NAME': {'rich_text': [{'text':{'content': row.NAME}}]}}
        )
    # return df.to_json()

if __name__ == '__main__':
    handler()