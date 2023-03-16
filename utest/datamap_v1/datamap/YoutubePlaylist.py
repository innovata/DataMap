"""

1. YouTube의 내계정의 재생목록 화면으로 들어간 뒤 아래끝까지 스크롤 한 후 HTML을 다운받아서 파싱-저장
- 다운로드한_유투브_플레이리스트_HTML을_파싱후_저장
2. YouTube API를 사용
"""

from datamap import *



from bs4 import BeautifulSoup




import __pymongo as mg


from data_map import DataMap


"""
============================== HTML Download ==============================
다운로드한_유투브_플레이리스트_HTML을_파싱후_저장
"""
def save_DL_html(file_name='Innovata I - YouTube - YouTube.html', ):
    
    
    """
    """
    with open(DATA_PATH + '/' + file_name) as f:
        read_data = f.read()

    soup = BeautifulSoup(read_data, 'html.parser')
    cont_li = soup.find_all(class_="style-scope ytd-grid-renderer use-ellipsis")
    cont_li_len = len(cont_li)
    i=1
    for cont in cont_li:
        print('\n' + '='*60 + '{}/{}'.format(i, cont_li_len))
        a = cont.find('a', id='meta')
        for string in a.h3.stripped_strings:
            대상명 = string

        dic = {
            '대상명':대상명,
            '출처':a.attrs['href'],
        }
        d = dic.copy()
        DataMap.upsert_one(대상명=d['대상명'], 출처=d['출처'], 대상내용=None, 분류값li=[], dbg_on=dbg_on, 사전검증=사전검증)
        i+=1
"""
============================== HTML scrape ==============================
"""
def __파싱저장(res):

    dicli = res['items']
    pp.pprint({inspect.stack()[0][3]:{"res['items'] 길이":len(res['items'])}})
    for dic in dicli:
        d = dic['snippet'].copy()
        d['id'] = dic['id']
        #pp.pprint({inspect.stack()[0][3]:{'d':d}})
        #db[TBL].insert_one(d)
    mg.테이블의_중복제거(DB, TBL, subset=['title'])

def 재생목록_파싱저장후_대상분류값li로_변환저장(res):
    
    __파싱저장(res)
"""
============================== Handler ==============================
"""
def __유투브_리스트를_대상_분류값li로_변환저장():
    DataMap.TBL = '대상_분류값li'
    dicli = list( db['유투브_리스트'].find() )
    for dic in dicli:
        d = {
            '대상명':dic['title'],
            '출처':'https://www.youtube.com/playlist?list='+dic['id'],
        }
        pp.pprint({inspect.stack()[0][3]:{'d':d}})
        대상_분류값li에_삽입(d['대상명'], d['출처'])
        db[DataMap.TBL].insert_one(d)

    mg.테이블의_중복제거(DB, DataMap.TBL, subset=['대상명','출처'])
    mg.테이블의_백업csv_생성(DB, DataMap.TBL, DATA_PATH)
