
import pandas as pd

mg_client = MongoClient()


import sys
sys.path.append('/Users/sambong/p/lib/')
import __pymongo as mg


from datamap import *
db = mg_client[DB]



def 텍스트확장자파일로부터_파이썬_패키지명을_수집후_저장(파일명):
    # 수집
    df = pd.read_table(DATA_PATH + 파일명, header=None).rename(columns={0:'text'})

    # 파싱
    df = df[ df['text'].str.contains(pat='pip install', case=False, na=False) ]
    df = df[ ~(df['text'].str.contains(pat='upgrade',case=False,na=False)) ]
    df = df[ ~(df['text'].str.contains(pat='. More',case=False,na=False)) ]
    df = df[ ~(df['text'].str.contains(pat='package',case=False,na=False)) ]

    df['text'] = df['text'].apply(lambda x: str(x).replace('==3.3.0', ''))
    df = df['text'].str.partition(pat='pip install').rename(columns={2:'pkg'}).loc[:,['pkg']]
    df = df.drop_duplicates(subset=['pkg']).sort_values('pkg')
    df['pkg'] = df['pkg'].apply(lambda x: str(x).replace(' ',''))

    tbl = '대상의_태그정의'
    원본_파일명 = 파일명.replace('.txt', '.pdf')
    dic = {'대상명':원본_파일명, 'lib_li': list(df['pkg'].values)}

    # 저장, 중복제거, 백업
    rslt = list( db[tbl].find({'대상명':dic['대상명']}) )
    if len(rslt) == 0:
        db[tbl].insert_one(dic)
    elif len(rslt) == 1:
        rslt = rslt[0]
        db[tbl].update_many(
            {'_id':ObjectId(rslt['_id'])},
            {'$set':{'lib_li':dic['lib_li']}}
        )
    mg.테이블의_중복제거(DB, tbl, where=None, subset=['대상명'])
    mg.테이블의_백업csv_생성(DB, tbl, DATA_PATH=DATA_PATH)

def 분류성_컬럼들에_대해_값을_추출해서_두개의_테이블_생성(df):
    def __스트링_cols의_분류값을_추출해서_분류명_분류값li_맵_생성(df, 분류명_li):
        tbl = '분류명_분류값li_맵'

        for 분류명 in 분류명_li:
            print('\n 분류명 : ', 분류명)
            분류값_li = list(df[분류명].dropna().unique())
            dic = {'분류명':분류명, '분류값_li':분류값_li}
            db[tbl].insert_one(dic)

        mg.테이블의_중복제거(DB, tbl, where=None, subset=['분류명'])

    def __리스트_cols의_분류값을_추출해서_저장(df, 분류명_li):
        tbl = '분류명_분류값li_맵'

        for 분류명 in 분류명_li:
            print('\n 분류명 : ', 분류명)
            df1 = df[분류명].dropna()
            df1_values_li = list(df1.values)
            임시_li = []
            for li in df1_values_li:
                임시_li = 임시_li + li

            분류값_li = lh.리스트의_중복제거(임시_li)
            dic = {'분류명':분류명, '분류값_li':분류값_li}
            db[tbl].insert_one(dic)

        mg.테이블의_중복제거(DB, tbl, where=None, subset=['분류명'])

    def __대상명에_대한_신규_테이블_생성(df, 키_cols):
        tbl = '대상의_분류값_정의'

        for name, g in df.groupby('_id'):
            g = g.dropna(axis=1)
            col_li = list(g.columns)
            col_li.remove('_id')
            col_li = lh.리스트1로부터_리스트2를_제거(col_li, 키_cols)

            분류값_li = []
            for col in col_li:
                v = list(g[col])[0]
                if col in 스트링_cols:
                    분류값 = [v]
                else:
                    분류값 = v
                분류값_li = 분류값_li + 분류값

            g = g.loc[:,키_cols]
            g_dic = g.to_dict('records')[0]
            g_dic['분류값_li'] = 분류값_li
            db[tbl].insert_one(g_dic)

        mg.테이블의_중복제거(DB, tbl, where=None, subset=['대상명'])

    키_cols = ['대상명','출처']
    스트링_cols = ['콘텐츠타입','국가기관']
    리스트_cols = ['생각의틀','추상개념기술','데이터분석_프로세스','프로그래밍언어','lib_li']
    # 분류명_분류값li_맵 생성
    __스트링_cols의_분류값을_추출해서_분류명_분류값li_맵_생성(df, 스트링_cols)
    __리스트_cols의_분류값을_추출해서_저장(df, 리스트_cols)

    # 대상의_분류값_정의 생성
    __대상명에_대한_신규_테이블_생성(df, 키_cols)
