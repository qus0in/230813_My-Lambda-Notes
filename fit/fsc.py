import pandas as pd
import requests
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

class FSC:
    BASE_URL = 'http://apis.data.go.kr/1160100/service'
    PRICE_INFO = 'GetBondSecuritiesInfoService/getBondPriceInfo'
    BASE_INFO= 'GetBondIssuInfoService/getBondBasiInfo'

    @classmethod
    def get_data(cls, entrypoint, base_date, num_of_rows):
        fsc_api_key = os.getenv('fsc_api_key')
        if not fsc_api_key:
            raise Exception('NO FSC API KEY')
        params = dict(
            serviceKey=fsc_api_key,
            resultType='json',
            basDt=base_date,
            numOfRows=num_of_rows,
        )
        res = requests.get(f'{cls.BASE_URL}/{entrypoint}', params=params)
        json : dict = res.json()
        data : {} = json.get('response', {}).get('body', {})\
                          .get('items', {}).get('item', {})
        if not len(data):
            raise Exception('NO DATA')
        df = pd.DataFrame(data)
        return df

    @classmethod
    def get_price_info(cls):
        최근일자 = datetime.utcnow()
        for _ in range(14):
            print(최근일자.date())
            try:
                return cls.get_data(FSC.PRICE_INFO,
                                    최근일자.strftime('%Y%m%d'), 1000)
            except Exception as e:
                print(e)
                최근일자 -= relativedelta(days=1)    


    @classmethod
    def get_price_info(cls):
        # 금융위원회_채권시세정보
        # https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15094784
        최근일자 = datetime.utcnow()
        for _ in range(14):
            print(최근일자.date())
            try:
                return cls.get_data(FSC.PRICE_INFO,
                                    최근일자.strftime('%Y%m%d'), 1000)
            except Exception as e:
                print(e)
                최근일자 -= relativedelta(days=1)

    @classmethod
    def get_base_info(cls):
        # 금융위원회_채권기본정보
        # https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15059592
        최근일자 = datetime.utcnow()
        for _ in range(14):
            print(최근일자.date())
            try:
                return cls.get_data(FSC.BASE_INFO,
                                    최근일자.strftime('%Y%m%d'), 30000)
            except Exception as e:
                print(e)
                최근일자 -= relativedelta(days=1)   

    @classmethod
    def get_bond_info(cls):
        price_info = cls.get_price_info()
        base_info = cls.get_base_info()
        bond_info = pd.merge(price_info, base_info, on='isinCd', suffixes=['x', 'y'])
        bond_info = bond_info.loc[:, [
            # 채권명, 거래량, 가격, 수익률, 표면이율, 
            'itmsNm', 'trqu', 'clprPrc', 'clprBnfRt', 'bondSrfcInrt', # 'scrsItmsKcdNm' : 분류
            # 만기일
            'bondExprDt', # 'bondIsurNm' : 발행자명, 'intPayCyclCtt' : 이자주기
            # 신뢰도
            'kisScrsItmsKcdNm', 'kbpScrsItmsKcdNm', 'niceScrsItmsKcdNm']]
        bond_info.rename(columns=dict(
            itmsNm = 'NAME', trqu = 'VOLUME', clprPrc = 'PRICE',
            clprBnfRt = 'BENEFIT', bondSrfcInrt = 'INTEREST', bondExprDt = 'EXPIRE',
            kisScrsItmsKcdNm = 'KIS', kbpScrsItmsKcdNm = 'KBP', niceScrsItmsKcdNm = 'NICE',
        ), inplace=True)
        bond_info.KIS = bond_info.KIS.map({
            '': True, 'AAA': True,
            'AA+': True, 'AA0': True, 'AA-': True,
            'A+': True, 'A0': True, 'A-': True,
            'BBB+': True, 'BBB0': True, 'BBB-': True}).fillna(False)
        bond_info.KBP = bond_info.KBP.map({
            '': True, 'AAA': True,
            'AA+': True, 'AA': True, 'AA-': True,
            'A+': True, 'A': True, 'A-': True,
            'BBB+': True, 'BBB': True, 'BBB-': True}).fillna(False)
        bond_info.NICE = bond_info.NICE.map({
            '': True, 'AAA': True,
            'AA+': True, 'AA0': True, 'AA-': True,
            'A+': True, 'A0': True, 'A-': True,
            'BBB+': True, 'BBB0': True, 'BBB-': True}).fillna(False)        
        return bond_info