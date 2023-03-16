"""

0. (생략가능) "로컬 pdf파일" 테이블명으로 별도 저장
1. 대상_분류값li 테이블에 저장
2. 테이블 중복제거 및 백업
"""

from datamap import *





import pandas as pd


import __pymongo as mg


TBL = 'DataMap'


"""
============================== 저장 ==============================
대상_분류값li에_삽입
"""
def upsert_one(대상명, 출처, 대상내용=None, 분류값li=[], dbg_on=False, 사전검증=False):
    
    
    """
    ===== 사용법 =====
    DataMap.upsert_one(대상명, 출처, 대상내용=None, 분류값li=분류값li, dbg_on=False, 사전검증=False)
    upsert_one(대상명, 출처, 대상내용=None, 분류값li=분류값li, )
    """
    dic = {
        '대상명':대상명,
        '출처':출처,
        '대상내용':대상내용,
        '분류값li':분류값li,
    }
    query = {'대상명':대상명, '출처':출처}
    update = {'$set':dic}
    mg.update_one(db=DB, tbl=TBL, query=query, update=update, upsert=True, dbg_on=dbg_on, 사전검증=사전검증)



def deduplicate():
    

    mg.deduplicate_tbl(db=DB, tbl=TBL, query=None, subset=['대상명','출처'], dbg_on=False, 사전검증=True)
    mg.테이블의_특정_컬럼값이_리스트형인_경우_리스트를_중복제거(db=DB, tbl=TBL, col='분류값li')

"""
============================== 분석 ==============================
"""
"""
============================== Handler ==============================
"""
def delete_obj(obj_nm):
    
    
    """
    obj_nm = 'Data Science for Business__What you need to know about data mining and data analytic thinking__Foster Provost.pdf'
    """
    query = {'대상명':obj_nm}
    db[TBL].delete_one(filter=query)

"""
============================== Object_ClassifiedValueList_Reprot ==============================
"""
def regex_ObjContents(regex):
    
    
    """
    """
    query = {'대상내용':{'$regex':regex, '$options':'i'}}
    projection = {'대상내용':0,'_id':0}
    report_objnm_src(query, projection)


def report_objnm_src(query, projection=None):
    
    
    """
    대상명_출처_보고
    """
    df = pd.DataFrame(list(db[TBL].find(filter=query, projection=projection)))
    dbg.df_structure(df=df)

    df = df.loc[:,['대상명','출처']]
    df = df.sort_values('출처')
    dicli = df.to_dict('records')
    dicli_len = len(dicli)
    i=1
    for d in dicli:
        print('\n' + '-'*60 + '{}/{}'.format(i, dicli_len))
        pp.pprint(d)
        i+=1


def run():
    """
    from data_map.DataMap import *
    """
    #query = {'대상내용':{'$regex':'visualization', '$options':'i'}}
    query = {
        '대상명':{'$regex':'.pdf$', '$options':'i'},
        '출처':{'$regex':'^http:', '$options':'i'}
    }
    report_objnm_src(query=query, projection=None)
