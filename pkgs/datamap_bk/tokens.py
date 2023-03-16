# ============================================================ Python.
import sys
import itertools
import re
import json
import os
# ============================================================ External-Library.
from bs4 import BeautifulSoup
import pandas as pd
# ============================================================ My-Library.
import idebug as dbg
from iipython import ifile
import inlp
import iwiki
# ============================================================ Project.
from datamap import models
from datamap import PJT_PATH
# ============================================================ Constant.
DATA_PATH = f"{PJT_PATH}/data"




#============================================================
"""
# Data 의 name, contents 로부터 keywords 를 추출.
사전작업
- 데이터명 구조 파싱
- 타이틀의 쓸모없는 문자열을 패턴삭제
본작업
- 타이틀의 언어 분리
- pos 분석 후 명사 추출
- 키워드 선정
"""
#============================================================

def main_process():
    DataNameExtractor().process()
    #ContentsExtractor().process()
    KeywordFrequency().analysis_process()
    KeywordCombinationStrength().analysis_process()
    KeywordRemover().delete_keywords()
    KeywordFilter().save_all_keywords_in_file()

class DataNameParser:

    def __init__(self, name):
        self.name = name
        self.title = None
        self.keywords = []
        self.author = None
        self.publisher = None
        self.year = None

    def parse(self):
        self.parse_keywords_part()
        self.parse_title_part()
        return self

    def parse_keywords_part(self):
        m = re.search(pattern='__\[.+\]$', string=self.name)
        if m is None:
            self.title = self.name
        else:
            self.title = self.name[:m.start()]
            keywords = self.name[m.start()+3:m.end()-1]
            self.keywords = re.split(pattern=',\s+|,', string=keywords)

    def parse_title_part(self):
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

class TextCleaner:

    def __init__(self):
        self.patterns = [
            " - YouTube",
            " - Google (Drive|Docs|Sheets|Search)",
            " - Gmail",
            " - Wikipedia",
            " - Quora",
            " - By Schools",
            "\| Coding Dojo",
            "\| freeCodeCamp",
            "\| edX|edX \|",
            "- WebsiteSetup",
            "\| Django[a-zA-Z ]+",
            "\| Udemy",
            "- KOCW",
            "\| Europass",
            "\[외국인[ 가-힣]+ \| 코리안브로스\]",
            "\[외국인[ 가-힣]+ \| 코리안브로스[ a-zA-Z가-힣]+\]",
            "\|\|[ a-zA-Z ]+",
        ]
        self.convert_pattern_str()
        self.p = re.compile(pattern=self.pattern)

    def convert_pattern_str(self):
        # 중복제거.
        self.patterns = list(set(self.patterns))

        self.pattern = ''
        for pat in self.patterns:
            self.pattern += f"|{pat}"
        return self

    def update_pattern(self, addi_pattern):
        self.patterns.append(addi_pattern)
        self.convert_pattern_str()
        self.p = re.compile(pattern=self.pattern)
        return self

    def return_patterns(self):
        return list(self.__dict__.values())

    def clean(self, text):
        new_text, numbers = self.p.subn(repl='', string=text)
        return new_text

class Extractor:
    """text : dataname or datacontents"""
    def __init__(self, text, keywords):
        self.text = text
        self.keywords = keywords

    def split_langs(self):
        self.linguistic_text = inlp.lang.LatinHangulSpliter(self.text)
        return self

    def extract_keywords_from_each_lang(self):
        t = self.linguistic_text
        k = inlp.pos.Konlpy(t.hangul, 'korean')
        k_nouns = k.postag().remove_useless_words_and_get_nouns()
        n = inlp.pos.NLTK(t.latin, 'latin')
        n_nouns = n.postag().remove_useless_words_and_get_nouns()
        self.keywords += (k_nouns + n_nouns)

    def deduplicate_keywords(self):
        self.keywords = list(set(self.keywords))

class DataNameExtractor(models.Data):
    """extract keywords from name"""
    def __init__(self):
        super().__init__()
        projection = {'_id':1, 'name':1, 'keywords':1}
        self.docs = self.load(projection=projection).docs

    def process(self):
        self.extract_keywords()
        self.iter_updating_docs()

    def extract_keywords(self):
        tc = TextCleaner()
        loop = idbg.LoopReporter(title=self.__doc__, len=len(self.docs))
        for d in self.docs:
            dn = DataNameParser(name=d['name']).parse()
            title = tc.clean(text=dn.title)
            e = Extractor(text=title, keywords=d['keywords'])
            e.split_langs()
            e.extract_keywords_from_each_lang()
            e.deduplicate_keywords()
            d['keywords'] = e.keywords
            loop.report()
        return self

class ContentsExtractor(models.Data):
    """extract keywords from contents"""

    def __init__(self):
        super().__init__()
        filter = {'contents':{'$ne':None}}
        projection = {'_id':1, 'contents':1}
        self.docs = self.load(filter, projection)

    def update_many_keywords(self):
        self.tokenize_contents()
        for d in self.docs:
            filter = {'_id':d['_id']}
            update = {'$set':{'keywords':d['tokens']}}
            UpdateResult = db[self.tblname].update_one(filter, update, upsert=False)
            print(f"\n\n UpdateResult :\n\n{UpdateResult}")

    def tokenize_contents(self):
        data = self.docs
        self.docs = []
        for d in data:
            d['tokens'] = inlp.nltk.get_tokens(text=d['contents'], lang='english')
            self.docs.append(d)

    def report_term_frequency(self):
        self.get_tbl_of_contents()
        df = pd.DataFrame(self.docs)
        inlp.nltk.count_tokens(texts=list(df.contents), lang='english')

def print_extraction_result(self):
    df = self.get_df()
    del(df['_id'])
    print(f"\n\n df :\n\n {df}")
#============================================================
# Data의 keywords를 분석.
#============================================================

class KeywordFrequency(models.Keyword):

    def __init__(self):
        super().__init__()
        projection = {'_id':0, 'keywords':1}
        self.df = models.Data().load(projection=projection).get_df()

    def analysis_process(self):
        self.drop()
        self.calc_frequency()
        self.docs = self.freqdf.to_dict('records')
        self.insert_docs()

    def calc_frequency(self, series=None):
        """키워드 당 빈도수를 계산해서 저장."""
        if len(self.df) is not 0:
            series = self.df.keywords if series is None else series
            keywords_li = list(series)
            li = []
            for keywords in keywords_li:
                for keyword in keywords:
                    li.append(keyword)
            df = pd.DataFrame({'keyword':li, 'freq':1})
            gsum = df.groupby('keyword').sum()
            gsum['keyword'] = gsum.index
            gsum.index = list(range(len(gsum)))
            self.freqdf = gsum.sort_values('freq')

class KeywordCategorizer(models.Keyword):

    def __init__(self):
        super().__init__()
        self.docs = self.load(projection={'_id':1, 'keyword':1})

    def mark_category(self):
        i=1
        for d in self.docs:
            d['existance'] = iwiki.search_existance(word=d['keyword'], lang='en')
            if i == 10:
                break
            i+=1

class KeywordCombinationStrength(models.KeywordCombination):

    def __init__(self):
        super().__init__()
        projection = {'_id':0, 'keywords':1}
        self.df = models.Data().load(projection=projection).get_df()

    def analysis_process(self):
        self.make_combinations_col()
        self.get_combinations()
        self.calc_combination_strengths()
        self.convert_tuple_into_list()
        self.drop()
        self.insert_docs()

    def make_combinations_col(self):
        """기본 keywords 당 조합을 만들어 저장."""
        def exec_combinations(x):
            if isinstance(x, list):
                if len(x) > 1:
                    tuples = list(itertools.combinations(set(x), 2))
                    return tuples

        self.df = self.df.assign(combinations= lambda x: x.keywords.apply(exec_combinations))
        return self

    def get_combinations(self):
        combinations_li = list(self.df.combinations)
        self.combinations = []
        for combinations in combinations_li:
            if (combinations is not None) and isinstance(combinations, list):
                for combination in combinations:
                    self.combinations.append(combination)
        return self

    def calc_combination_strengths(self):
        df = pd.DataFrame({'combination':self.combinations, 'strength':1})
        gsum = df.groupby('combination').sum()
        gsum['combination'] = gsum.index
        gsum.index = list(range(len(gsum)))
        self.gsum = gsum.sort_values('strength')
        return self

    def convert_tuple_into_list(self):
        self.gsum.combination = self.gsum.combination.apply(lambda x: list(x))
        self.docs = self.gsum.to_dict('records')
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

class KeywordRemover(models.Keyword):

    def __init__(self, filepath=f"{DATA_PATH}/KeywordRemover.txt"):
        super().__init__()
        self.data_filepath = filepath
        self.load_existed_keywords()

    def load_existed_keywords(self):
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

    def delete_keywords(self):
        # Data-Table 의 keywords 컬럼에서 삭제.

        # Keyword-Table 의 keyword 컬럼에서 삭제.
        filter = {'keyword':{'$in':self.keywords}}
        self.delete_many(filter)

        # KeywordCombination 에서도 해당 키워드가 있는 조합을 전부 삭제.
        kc = models.KeywordCombination()
        #df = kc.load().get_df()
        filter = {'combination':{'$elemMatch':{'$in':self.keywords}}}
        kc.delete_many(filter)
        return self, kc

class KeywordFilter(models.Keyword):

    def __init__(self, filepath=f"{DATA_PATH}/KeywordFilter.txt"):
        super().__init__()
        self.filepath = filepath#f"{DATA_PATH}/{__class__.__name__}.txt"

    def save_all_keywords_in_file(self):
        df = self.load(projection={'_id':0}).get_df()
        keywords = sorted(df.keyword)
        # 모두
        text = json.dumps(keywords, ensure_ascii=False)
        # 수작업으로 키워드를 골라내기 쉽게 포멧을 조작.
        text = re.sub(pattern='^\[', repl='', string=text)
        text = re.sub(pattern='\]$', repl='', string=text)
        text = re.sub(pattern='", "', repl='",\n"', string=text)
        ifile.write_file(self.filepath, text)
        # xls 파일로 내보내기.
        df = df.sort_values('keyword')
        df.index = list(range(len(df)))
        df = df.reindex(columns=['keyword'])
        df.to_excel(f"{DATA_PATH}/KeywordFilter.xlsx", sheet_name='Sheet1')
