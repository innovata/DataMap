"""

"""

from datamap import *







import __pymongo as mg


TBL = '대표어_동의어li'

"""
============================== Saver ==============================
"""
def 대표어_동의어li에_삽입(대표어, 동의어li=[]):
    db[tbl].insert_one({
        '대표어':대표어,
        '동의어li':동의어li,
    })


def 대표어_동의어li_중복제거_백업():
    

    mg.테이블의_중복제거(DB, tbl, subset=['대표어'])
    mg.테이블의_특정_컬럼값이_리스트형인_경우_리스트를_중복제거(DB, tbl, '동의어li')
    mg.테이블의_백업csv_생성(DB, tbl, DATA_PATH)

"""
============================== analyzer ==============================
"""
def 대표어_동의어li의_모든값을_리스트화():
    
    tbl =
    li1 = list( db[TBL].distinct('대표어') )
    li2 = list( db[TBL].distinct('동의어li') )
    li = li1 + li2
    return li
