

import os
import sys
PJTS_PATH = '/Users/sambong/pjts'
DATA_PATH = f"{PJTS_PATH}/datamap/data"
sys.path.append(f"{PJTS_PATH}/libs/ilib")
import ilib
sys.path.append(f"{PJTS_PATH}/libs/idebug")
import idebug as dbg
sys.path.append(f"{PJTS_PATH}/libs/imath")
#sys.path.append(f"{PJTS_PATH}/libs/i-nlp")
sys.path.append(f"{PJTS_PATH}/libs/iwiki")
sys.path.append(f"{PJTS_PATH}/libs/ipdf")
sys.path.append(f"{PJTS_PATH}/datamap/env/lib/python3.7/site-packages")
sys.path.append(f"{PJTS_PATH}/datamap")




import pandas as pd
from bs4 import BeautifulSoup
import itertools
import re
import json
from pandas.io.json import json_normalize
from bson.objectid import ObjectId
import copy

from datamap import models
from datamap import IPORTFOLIO_DATA_PATH


#============================================================
# Data 의 name 로부터 keywords 를 추출.
#============================================================

def main_process():
    DatanameExtractor().extract_by_datanameparser()
    KeywordStandardizer().standardize()
    KeywordCleaner().process()
    KeywordCategorizer().findset_category_from_keywords()
    KeywordTranslator().save_words_to_xls()
    KeywordCategorizer().save_category_per_keyword_to_xls()
    KeywordFrequency().process_about_all_categories()
    KeywordCombinationStrength().process_about_all_categories()

class DataNameParser:

    def __init__(self, name):
        self.name = name
        self.title = None
        self.keywords = []
        self.author = None
        self.publisher = None
        self.year = None

    def parse(self):
        self.split_keywords_part()
        self.split_title_part()
        return self

    def split_keywords_part(self):
        m = re.search(pattern='__\[.+\]$', string=self.name)
        if m is None:
            self.title = self.name
        else:
            self.title = self.name[:m.start()]
            keywords = self.name[m.start()+3:m.end()-1]
            self.keywords = re.split(pattern=',\s+|,', string=keywords)
        return self

    def split_title_part(self):
        # 확장자명 제거.
        root, ext = os.path.splitext(self.title)
        strings = re.split(pattern='__', string=root)
        self.title = strings[0]
        if len(strings) > 1:
            self.author = strings[1]
        if len(strings) > 2:
            self.publisher = strings[2]
        m = re.search(pattern='__\d+$', string=root)
        if m is not None:
            self.year = root[m.start()+2:]
        return self

class DatanameExtractor(models.Data):
    """Dataname(Keywords)Extractor
    extract keywords from dataname
    """
    def extract_by_datanameparser(self):
        self.load({'dtype':'bookmark'}, {'_id':1,'name':1,'keywords':1})
        loop = idbg.LoopReporter(title=self.__doc__, len=len(self.docs))
        for d in self.docs:
            dn = DataNameParser(name=d['name']).parse()
            d['name'] = dn.title
            d['keywords'] += dn.keywords
            d['keywords'] = list(set(d['keywords']))
        self.iter_updating_docs(by='_id')

class DatacontentsExtractor(models.Data):
    """Datacontents(Keywords)Extractor
    extract keywords from datacontents
    """

class DatanameExtractor2(models.Data):

    def __init__(self, filepath, useless_keywords=[], categories=[]):
        super().__init__()
        self.filepath = filepath
        self.useless_keywords = useless_keywords
        self.categories = categories

    def set_category_col(self):
        """카테고리로 설정한 키워드는 카테고리컬럼으로 복사하고, 키워드리스트에서 제거한다."""
        if len(self.useless_keywords) is not 0:
            for d in self.docs:
                for k in d['keywords']:
                    if k in self.categories:
                        d['category'] = k
                        d['keywords'].remove(k)
                        break
        return self

    def split_double_keyword_of_elem(self):
        """폴더명 중에 콤마(,)로 이루어진 두 개 이상의 키워드가 하나의 키워드로 인식되어 있는 것을 기존 리스트에 분할추가한다."""
        p = re.compile(pattern='.+,.+|.+,\s+.+')
        for d in self.docs:
            new_keywords = []
            for k in d['keywords']:
                m = p.match(string=k)
                if m is None:
                    new_keywords.append(k)
                else:
                    ks = k.split(',')
                    ks = [k.rstrip().lstrip() for k in ks]
                    new_keywords += ks
            d['keywords'] = new_keywords
        return self

    def delete_categoryless_data(self):
        df = self.get_df()
        df = df.dropna(axis='index', how='all', subset=['category'])
        self.docs = df.to_dict('records')
        return self

#============================================================
# keywords를 표준화, 청소(제거), 번역, 약자화,
#============================================================

class KeywordStandardizer(models.Data):

    def __init__(self, rulespath=None):
        super().__init__()
        rulespath = f"{DATA_PATH}/Keywords-standardization - Sheet1.csv" if rulespath is None else rulespath
        df = pd.read_csv(rulespath)
        # 규칙적용 순서를 결정해야 한다. 광범위한 것부터 개별경우로 좁혀가면서.
        df = df.sort_values('seq')
        self.rules = df.to_dict('records')
        self.purify_rules()

    def purify_rules(self):
        # 구글스프레드시트 덕분에 이런 더러운 코드를 작성해야 된다. 씨발 구글.
        for r in self.rules:
            print(f"\n rule :\n {r}\n")
            r['work'] = r['work'].rstrip().lstrip()
            r['keyword_regex'] = r['keyword_regex'].rstrip().lstrip()
            new = r['standard']
            r['standard'] = new.rstrip().lstrip() if isinstance(new, str) else new
        return self

    def standardize(self):
        for r in self.rules:
            work = r['work']
            old = r['keyword_regex']
            new = r['standard']

            projection = {'_id':1,'keywords':1,'category':1}
            self.load_matching_regex_keyword(regex=old, options='i', projection=projection)
            p = re.compile(pattern=old, flags=re.I)
            for d in self.docs:
                keywords = d['keywords'].copy()
                for keyword in keywords:
                    m = p.search(string=keyword)
                    if m is not None:
                        d['keywords'].remove(keyword)
                        # 경고! 구글스프레드시트의 문자열을 사용할 경우, 'is'는 안통하고 '=='를 사용해야 한다.
                        # 빌어먹을 구글!! 도대체 무슨 문자열 데이터타입을 사용하는거야!
                        if work == 'replace':
                            addi_keywords = [new]
                        elif work == 'special_char':
                            addi_keywords = [keyword.replace('-',' ')]
                        elif work == 'capitalize':
                            addi_keywords = [keyword.capitalize()]
                        # 약어는 모두 대문자화.
                        elif work == 'upper':
                            addi_keywords = [keyword.upper()]
                        elif work == 'split':
                            if isinstance(new, list):
                                addi_keywords = new
                            else:
                                print(f"\n Input-Error. new는 리스트여야한다.\n")
                                new_li = new.split(',')
                                new_li = [e.rstrip().lstrip() for e in new_li]
                                addi_keywords = new_li
                        else:# 빈깡통을 주면 영향없다.
                            addi_keywords = []

                        for addi in addi_keywords:
                            d['keywords'].append(addi)
                d['keywords'] = list(set(d['keywords']))
            self.iter_updating_docs(by='_id')
        return self

class KeywordTranslator:
    """단일 언어로 번역한 키워드를 DB에 저장할 필요없다.
    분석, 시각화 단계에서 표준화하기 위해서 메모리상에서만 작업해서 결과를 돌려준다.
    """
    def __init__(self, dictpath=None):
        dictpath = f"{DATA_PATH}/Keywords-translation - Sheet1.csv" if dictpath is None else dictpath
        df = pd.read_csv(dictpath)
        df = df.dropna(axis=0,how='all')
        self.dict = df.to_dict('records')

    #def collect_dict_from_gdrive(self):

    def translate(self, data_docs, olang, dlang):
        """사전에서 타겟언어 컬럼만 걸러내기."""
        df = pd.DataFrame(self.dict)
        df = df.reindex(columns=[olang, dlang])
        dict = df.to_dict('records')
        for dic in dict:
            p = re.compile(pattern=f"^{dic[olang]}$", flags=re.I)
            for d in data_docs:
                """루핑하기 위해 복사"""
                keywords = d['keywords'].copy()
                for keyword in keywords:
                    if p.search(string=keyword) is not None:
                        d['keywords'].remove(keyword)
                        d['keywords'].append(dic[dlang])
        return data_docs

    def save_words_to_xls(self):
        words = self.get_words()
        if words is not None:
            df = pd.DataFrame({'word':words})
            df['bytes'] = df.word.apply(lambda x: sys.getsizeof(x))
            df.to_excel(f"{DATA_PATH}/Translating-words.xlsx", sheet_name='Sheet1')

    def get_words(self):
        d = models.Data().load(None, {'_id':0,'keywords':1})
        if len(d.docs) is not 0:
            df = json_normalize(d.docs, 'keywords').rename(columns={0:'keyword'})
            df = df.dropna(axis=0, how='all')
            df = df.drop_duplicates(keep='first', subset=['keyword'])
            keywords = sorted(df.keyword)
            categories = sorted(d.distinct(key='category', filter=None))
            return categories + keywords

self = KeywordTranslator()
df = pd.DataFrame(self.dict)
df
#class KeywordAbbreviator:

class KeywordCleaner(models.Data):

    def process(self):
        self.merge_longkeyword_into_name()
        self.remove_useless_keywords()

    def load_existed_keywords(self, filepath):
        self.data_filepath = filepath
        text = ifile.open_file(self.data_filepath)
        li = json.loads(text)
        if isinstance(li, list):
            self.keywords = li
        else:
            print(f"\n 에러! data_filepath 안의 내용은 반드시 리스트-타입어야 한다.\n")
            self.keywords = []
        return self

    def save_usless_keyword(self, keyword):
        # 추가.
        self.keywords += [keyword]
        # 중복제거.
        self.keywords = list(set(self.keywords))
        # 파일로 저장. 기존 파일내용은 무시.
        text = json.dumps(self.keywords)
        ifile.write_file(self.data_filepath, text)
        return self

    def remove_keywords_of_target(self, id, keyword):
        # Data-Table 의 keywords 컬럼에서 삭제.
        d = models.Data()
        filter = {'_id':id}
        projection = {'_id':1, 'keywords':1}
        d.load(filter, projection)
        d.doc = d.docs[0]
        d.doc['keywords'].remove(keyword)
        d.update_doc()

    def remove_useless_keywords(self, filepath=None):
        filepath = f"{DATA_PATH}/useless-keywords - Sheet1.csv" if filepath is None else filepath
        df = pd.read_csv(filepath)
        useless_keywords = list(df.keyword)

        # Data-Table 의 keywords 컬럼에서 해당 키워드만 삭제.
        filter = {'keywords':{'$elemMatch':{'$in':useless_keywords}}}
        self.load(filter, {'_id':1,'keywords':1})
        for d in self.docs:
            keywords = copy.deepcopy(d['keywords'])
            for k in keywords:
                if k in useless_keywords:
                    d['keywords'].remove(k)
        #self.iter_updating_docs(by='_id')

        # Keyword-Table 의 docs 자체를 삭제.
        k = models.Keyword()
        filter = {'keyword':{'$in':useless_keywords}}
        k.delete_many(filter)

        # KeywordCombination-Table 에서 해당 키워드가 있는 조합은 docs 자체를 삭제.
        kc = models.KeywordCombination()
        filter = {'combination':{'$elemMatch':{'$in':useless_keywords}}}
        kc.delete_many(filter)
        return self, k, kc

    def deduplicate_keywords(self):
        """전체 데이터에 대해서 앞자리만 대문자화하는 것은 의미가 없다."""
        projection = {'_id':1,'keywords':1}
        self.load(None, projection)
        for d in self.docs:
            keywords = d['keywords'].copy()
            keywords = [keyword.capitalize() for keyword in keywords]
            d['keywords'] = list(set(keywords))

    def merge_longkeyword_into_name(self, filepath=None):
        filepath = f"{DATA_PATH}/long-keywords - Sheet1.csv" if filepath is None else filepath
        df = pd.read_csv(filepath)
        long_keywords = list(df.keyword)
        for long_kw in long_keywords:
            # 구글스프레스시트의 좃같은 문자열 타입때문에.
            long_kw = long_kw.lstrip().rstrip()
            # regex 검색을 위한 파이썬특수기호에 대한 처리.
            long_kw = long_kw.replace('(','\(').replace(')','\)').replace('?','\?')
            self.load_matching_regex_keyword(regex=f"^{long_kw}$", options=None, projection={'_id':1,'name':1,'keywords':1})
            p = re.compile(pattern=f"^{long_kw}$")
            for d in self.docs:
                keywords = d['keywords']
                for k in keywords:
                    if p.search(string=k) is not None:
                        d['keywords'].remove(k)
                        d['name'] = f"{k}({d['name']})"
            self.iter_updating_docs(by='_id')
        return self

#============================================================
# Data의 keywords를 분석.
#============================================================

class KeywordCategorizer(models.Data):
    """키워드로부터 카테고리값을 결정짓는다."""
    def __init__(self, categories=[]):
        super().__init__()
        """북마크 저장시 유저의 주관적 판단에 의한 카테고리값을 이용"""
        self.categories = categories + ['Society','Interests','Tech','Lang','UPV','Asset','수신(修身)','Career']
        self.load(None, {'_id':1,'keywords':1,'category':1})

    def findset_category_from_keywords(self):
        for d in self.docs:
            keywords = d['keywords']
            for k in keywords:
                if k in self.categories:
                    d['category'] = k
                    d['keywords'].remove(k)

        self.iter_updating_docs(by='_id')
        return self

    def predict_category_from_given_keywords(self):
        projection = {'_id':0, 'keywords':1}
        docs = models.Data().load(projection=projection).docs
        #for d in docs:

    def save_category_per_keyword_to_xls(self):
        """Keyword-Table에 1:1 매핑관계를 업데이트저장."""
        self.clean()
        # xls 파일로 내보내기.
        df = self.get_df().sort_values(['category','keyword'])
        df.index = list(range(len(df)))
        df.to_excel(f"{DATA_PATH}/standard_category-keywords.xlsx", sheet_name='Sheet1')

    def clean(self):
        df = self.get_df()
        df = df.dropna(axis='index', how='all')
        df = json_normalize(df.to_dict('records'), 'keywords', ['category']).rename(columns={0:'keyword'})
        df = df.drop_duplicates(keep='first')
        self.docs = df.to_dict('records')
        return self

    def get_category_keywords(self):
        df = self.get_df()
        dics = []
        for n,g in df.groupby(['category']):
            dics.append({n: list(g.keyword)})
        return dics

def add_categoryvalue_to_keywords(docs):
    for d in docs:
        d['keywords'] += [d['category']]
    return docs

def remove_empty_keywords_docs(df):
    df.keywords = df.keywords.apply(lambda x: None if len(x) is 0 else x)
    return df.dropna(axis='index', how='all', subset=['keywords'])

class KeywordFrequency(models.Keyword):

    def calc_frequency(self, olang, dlang):
        """키워드 당 빈도수를 계산해서 저장.
        카테고리와 키워드 간의 중첩현상으로 인해 카테고-키워드를 묶어서 그룹핑해야 한다.
        """
        d = models.Data().load({},{'_id':0})
        kt = KeywordTranslator()
        d.docs = kt.translate(d.docs, 'korean', 'english')
        df = d.get_df()
        df = remove_empty_keywords_docs(df)
        if len(df) is 0:
            self.docs = []
        else:
            df = json_normalize(df.to_dict('records'), 'keywords', ['category'], errors='ignore').rename(columns={0:'keyword'})
            df.keyword = df.keyword.apply(lambda x: None if len(x) is 0 else x)
            df = df.dropna(axis=0, subset=['keyword'])
            df = df.assign(freq= 1)
            gsum = df.groupby('keyword').sum()
            del(df['freq'])
            df = df.join(gsum, how='left', on='keyword').drop_duplicates(subset=['keyword'])
            df = df.assign(lang= dlang)
            self.docs = df.sort_values('freq').to_dict('records')
        return self

    def save(self, upsert=False):
        if len(self.docs) is not 0:
            for d in self.docs:
                self.attributize(d)
                self.update_doc({'lang':self.lang, 'keyword':self.keyword}, True)
        return self

    def emit_csv(self):
        """로컬 테스트용 자료방출."""
        df = self.load({},{'_id':0}).get_df()
        df.to_csv(f"{PJTS_PATH}/iportfolio/datamap/data/{__class__.__name__}.csv", index=False)
        """서버로 자료올리기."""

self = KeywordFrequency()
self.calc_frequency('korean', 'english')
self.get_df()
self.save().emit_csv()

df = self.load({},{'_id':0}).get_df()
df.head()
df.groupby('category').count()
df.query('category == "수신(修身)"')

class KeywordCombinationStrength(models.KeywordCombination):

    def load_data(self, filter=None, projection={'_id':0,'keywords':1}):
        self.docs = models.Data().load(filter, projection).docs
        return self

    def process(self):
        d = models.Data().load({},{'_id':0})
        kt = KeywordTranslator()
        d.docs = kt.translate(d.docs, 'korean', 'english')
        df = d.get_df()
        df = self.make_combinations_col(df, 'korean', 'english')
        all_combinations = self.get_all_combinations(df)
        gsum = self.calc_combination_strengths(all_combinations)
        self.save(gsum)
        self.emit_csv()

    def make_combinations_col(self, df, olang, dlang):
        """기초 keywords 당 조합을 만들어 신규 컬럼에 저장."""
        def exec_combinations(x):
            if isinstance(x, list) and (len(x) > 1):
                tuples = list(itertools.combinations(set(x), 2))
                return tuples

        df = remove_empty_keywords_docs(df)
        if len(df) is not 0:
            df['combinations'] = df.keywords.apply(exec_combinations)
            df = df.dropna(axis='index', how='any', subset=['combinations'])
            return df

    def get_all_combinations(self, df):
        combinations_li = list(df.combinations)
        all_combinations = []
        for combinations in combinations_li:
            if isinstance(combinations, list):
                for combination in combinations:
                    all_combinations.append(combination)
        return all_combinations

    def calc_combination_strengths(self, all_combinations):
        df = pd.DataFrame({'combination':all_combinations, 'strength':1})
        gsum = df.groupby('combination').sum()
        gsum['combination'] = gsum.index
        gsum.index = range(len(gsum))
        return gsum

    def save(self, df):
        self.docs = df.to_dict('records')
        self.drop()
        self.insert_docs()
        return self

    def emit_csv(self):
        """로컬 테스트용 자료방출."""
        df = self.load({},{'_id':0}).get_df()
        """시각화용 키워드로 변경."""
        df.to_csv(f"{IPORTFOLIO_DATA_PATH}/{__class__.__name__}.csv", index=False)

    def convert_tuple_into_list(self):
        """추후, 분석 시 데이터베이스 직접 검색을 위해서."""
        df = self.get_df()
        df.combination = df.combination.apply(lambda x: list(x))
        self.docs = df.to_dict('records')
        return self

    def calc_comb_count(self):
        """키워드 당 조합의 수를 계산해서 저장."""
        self.calc_combination_strengths()
        df = pd.DataFrame(self.combination_strengths)
        df.combination = df.combination.apply(lambda x: list(x))
        return self.calc_frequency(df.combination)

    def make_keyword_relation(self):
        relations = pd.DataFrame(self.get_links()).rename(columns={'node1':'keyword', 'node2':'name'})
        keywords = pd.DataFrame(self.get_nodes()).rename(columns={'id':'name'}).to_dict('records')
        keyword_relations = []
        for keyword in keywords:
            df = relations[ relations.keyword == keyword['name'] ]
            if len(df) is 0:
                keyword['relations'] = []
            else:
                del(df['keyword'])
                keyword['relations'] = df.to_dict('records')
            keyword_relations.append(keyword)
        self.keyword_relations = keyword_relations

    def process_about_all_categories(self):
        self.drop()
        kt = KeywordTranslator()
        categories = KeywordCategorizer([None]).categories
        for category in categories:
            filter = {'category':{'$ne':None}}
            if category is not None:
                filter.update({'category':category})
            projection = {'_id':0, 'keywords':1, 'category':1}
            self.load_data(filter, projection)
            self.docs = add_categoryvalue_to_keywords(self.docs)
            self.docs = kt.translate(self.docs, 'korean', 'english')
            self.make_combinations_col()
            if len(self.docs) is not 0:
                self.get_all_combinations()
                self.calc_combination_strengths()
                self.convert_tuple_into_list()
                df = self.get_df()
                df = df.assign(category= category)
                self.docs = df.to_dict('records')
                print(self.get_df())
                self.insert_docs()

self = KeywordCombinationStrength()

d = models.Data().load({},{'_id':0})
kt = KeywordTranslator()
d.docs = kt.translate(d.docs, 'korean', 'english')
df = d.get_df()
df = self.make_combinations_col(df, 'korean', 'english')
all_combinations = self.get_all_combinations(df)
gsum = self.calc_combination_strengths(all_combinations)
self.save(gsum)
self.emit_csv()





gsum.sort_values('strength')
self.docs = gsum.sort_values('strength').to_dict('records')


df.head()
