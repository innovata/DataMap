"""

0. (생략가능) "로컬 pdf파일" 테이블명으로 별도 저장
1. 대상_분류값li 테이블에 저장
2. 테이블 중복제거 및 백업
"""
"""
========== 대상_분류값li 저장 관련 기본 작업 순서 ==========
1. 대상_분류값li 테이블에 저장
    1-1. 수집 또는 로딩
    1-2. 파싱
    1-3. 저장
2. 대상명, 대상내용을 검색해서 분류값li를 업데이트
3. 분류값을 대표어로 변경
4. 테이블 중복제거 및 백업
    4-1. 중복제거
    4-2. 백업
"""
from datamap import *







import __pymongo as mg


TBL = '분류명_분류값li_맵'

def 분류값li의_단어명칭_변경(tbl, 전, 후, query={}):

    query.update({'분류값li':{'$regex':전, '$options':'i'}})
    pp.pprint({'query':query})
    dicli = list(db[tbl].find(query, {'_id':1}))
    pp.pprint({'len(dicli)':len(dicli)})
    if len(dicli) == 0:
        return 0
    else:
        i=1
        dicli_len = len(dicli)
        for dic in dicli:
            print('\n'+'-'*75+'{}, {}/{}'.format(inspect.stack()[0][3], i, dicli_len))
            pp.pprint({'dic':dic})
            db[tbl].update_one(
                {'_id':dic['_id']},
                {'$pull':query}#{'분류값li':전}
            )
            db[tbl].update_one(
                {'_id':dic['_id']},
                {'$push':{'분류값li':후}}
            )
            i+=1
#query = {'대상명':'LEARN PYTHON THE HARD WAY(A Very Simple Introduction to the Terrifyingly Beautiful World of Computers and Code)__Zed A. Shaw__Third Edition__2014.pdf'}
#분류값li의_단어명칭_변경('대상_분류값li','John nash', 'John Nash', query)


def 분류명_분류값li에_삽입(분류명, 분류값li=[]):
    tbl = '분류명_분류값li_맵'
    db[tbl].insert_one({
        '분류명':분류명,
        '분류값li':분류값li,
    })


def 분류명_분류값li_중복제거_백업():

    tbl = '분류명_분류값li_맵'
    mg.테이블의_중복제거(DB, tbl, subset=['분류명'])
    mg.테이블의_특정_컬럼값이_리스트형인_경우_리스트를_중복제거(DB, tbl, '분류값li')
    mg.테이블의_백업csv_생성(DB, tbl, DATA_PATH)


"""
============================== analyzer ==============================
"""
def classification():
    대상명_대상내용을_검색해서_분류값li를_업뎃()
    분류값을_대표어로_변경()


def 대상_분류값_분류명_결합():

    df = pd.DataFrame(list( db['대상_분류값li'].find({'분류값li':{'$exists':True}}) ))
    pp.pprint({
        inspect.stack()[0][3]:{"db['대상_분류값li'] 길이":len(df)}
    })
    df = df.fillna('_')
    df1 = json_normalize( df.to_dict('records'), '분류값li', ['대상명','대상내용','출처'] ).rename(columns={0:'분류값'})

    df = pd.DataFrame(list( db['분류명_분류값li_맵'].find({'분류값li':{'$exists':True}}) ))
    pp.pprint({
        inspect.stack()[0][3]:{"db['분류명_분류값li_맵'] 길이":len(df)}
    })
    df = df.fillna('_')
    df2 = json_normalize( df.to_dict('records'), '분류값li', ['분류명'] ).rename(columns={0:'분류값'})

    df = df1.join(df2.set_index('분류값'), on='분류값')
    df = df.fillna('_')
    return df


def 대상명_대상내용을_검색해서_분류값li를_업뎃(tbl='대상_분류값li', query={}):

    분류값_li = 유일한_모든_분류값()

    i=1
    분류값_li_len = len(분류값_li)
    for 분류값 in 분류값_li:
        print('\n'+'-'*75+'{}, {}/{}, 분류값:{}'.format(inspect.stack()[0][3], i, 분류값_li_len, 분류값))
        q = __분류값에_따른__re_query(분류값)
        query.update(q)
        pp.pprint({'query':query})
        dicli = list( db[tbl].find(query, {'_id':1}) )
        if len(dicli)==0:
            pass
        else:
            print('len(dicli):', len(dicli))
            for dic in dicli:
                db[tbl].update_one(
                    {'_id':dic['_id']},
                    {'$push':{'분류값li':분류값}}
                )
        i+=1


def __분류값에_따른__re_query(분류값):

    #__대소문자 구별
    if 분류값 in ['Java','Go','ANN','NLP','SW']:
        r = 분류값
        query = {'$or':[ {'대상명':{'$regex':r}}, {'대상내용':{'$regex':r}} ]}
    #__특정패턴 부여
    elif 분류값 == 'C++':
        r = 'C\+\+'
        query = {'$or':[ {'대상명':{'$regex':r, '$options':'i'}}, {'대상내용':{'$regex':r, '$options':'i'}} ]}
    elif 분류값 == 'R':
        r = 'R '
        query = {'$or':[ {'대상명':{'$regex':r}}, {'대상내용':{'$regex':r}} ]}
    #__일반적
    else:
        r = 분류값
        query = {'$or':[ {'대상명':{'$regex':r, '$options':'i'}}, {'대상내용':{'$regex':r, '$options':'i'}} ]}
    return query
