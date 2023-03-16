"""

0. 수집
1. 대상명, 대상내용을 검색해서 분류값li를 업데이트
2. 분류값을 대표어로 변경
"""

from datamap import *



import pandas as pd
, DESCENDING

from pandas.io.json import json_normalize


import __list as lh
import __pymongo as mg


from data_map.collector import 분류값li의_단어명칭_변경


SYN_TBL = '대표어_동의어li'









def 유일한_모든_분류값():
    
    li1 = sorted( db['분류명_분류값li_맵'].distinct('분류값li') )
    li2 = sorted( db['대상_분류값li'].distinct('분류값li') )
    li3 = sorted( 대표어_동의어li의_모든값을_리스트화() )
    li = li1+li2+li3

    pp.pprint({inspect.stack()[0][3]:{'리스트의_중복제거(li) 전':len(li)}})
    li = sorted( lh.리스트의_중복제거(li) )
    return li


def 분류값을_대표어로_변경(tbl='대상_분류값li', query={}):
    
    """
    언젠가 특정 row만 찾아서 동의어 처리하도록 바꿔야 할 시점이 올 것이다.
    """
    dicli = list( db[SYN_TBL].find({},{'_id':False}).sort('대표어',ASCENDING) )
    i = 1
    dicli_len = len(dicli)
    for dic in dicli:
        print('\n'+'-'*75+'{}, {}/{}, 대표어:{}'.format(inspect.stack()[0][3], i, dicli_len, dic['대표어']))
        동의어_li = dic['동의어li']
        for 동의어 in 동의어_li:
            분류값li의_단어명칭_변경(tbl, 동의어, dic['대표어'], query)
        i+=1

    mg.테이블의_특정_컬럼값이_리스트형인_경우_리스트를_중복제거(DB, tbl, '분류값li')
