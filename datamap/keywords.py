
from datamap import *

from .models import Data, Datum, Keyword, KeywordCombination
from bs4 import BeautifulSoup
import itertools
import inltk
from nltk.corpus import stopwords



class Analyzer(Keyword, KeywordCombination, Data):

    def __init__(self):
        self.k = Keyword()
        self.kc = KeywordCombination()
        self.d = Data()
        keywords = self.d.find(projection={'_id':0, 'keywords':1})
        self.df = pd.DataFrame(keywords)

    def calc_frequency(self, series=None):
        """키워드 당 빈도수를 계산해서 저장."""
        series = self.df.keywords if series is None else series
        keywords_li = list(series)
        li = []
        for keywords in keywords_li:
            for keyword in keywords:
                li.append(keyword)
        df = pd.DataFrame({'keyword':li, 'freq':1})
        gsum = df.groupby('keyword').sum()
        gsum['keyword'] = gsum.index
        return gsum.sort_values('freq')

    def insert_keyword_freq(self):
        self.k.data = self.calc_frequency().to_dict('records')
        self.k.insert_data()

    def make_combinations_col(self):
        """기본 keywords 당 조합을 만들어 저장."""
        def exec_combinations(x):
            if isinstance(x, list):
                if len(x) > 1:
                    tuples = list(itertools.combinations(set(x), 2))
                    return tuples

        self.df = self.df.assign(combinations= lambda x: x.keywords.apply(exec_combinations))

    def get_combinations(self):
        self.make_combinations_col()
        combinations_li = list(self.df.combinations)
        self.combinations = []
        for combinations in combinations_li:
            if (combinations is not None) and isinstance(combinations, list):
                for combination in combinations:
                    self.combinations.append(combination)

    def calc_combination_strengths(self):
        self.get_combinations()
        df = pd.DataFrame({'combination':self.combinations, 'strength':1})
        gsum = df.groupby('combination').sum()
        gsum['combination'] = gsum.index
        return gsum.sort_values('strength')

    def insert_combination_strengths(self):
        df = self.calc_combination_strengths()
        InsertManyResult = db[self.kc.tblname].insert_many(documents=df.to_dict('records'))
        dbg.InsertManyResult(InsertManyResult)

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

class Provider(Keyword, KeywordCombination):
    """웹서버에게 키워드 분석결과 전달"""
    def __init__(self):
        self.k = Keyword()
        self.kc = KeywordCombination()

    def get_nodes(self):
        df = self.k.find(projection={'_id':0, 'keyword':1, 'freq':1})
        nodes = df.rename(columns={'keyword':'id', 'freq':'group'})
        return nodes.to_dict('records')

    def get_links(self):
        df = self.kc.find(projection={'_id':0, 'combination':1, 'strength':1})
        df['source'] = df.combination.apply(lambda x: x[0])
        df['target'] = df.combination.apply(lambda x: x[1])
        del(df['combination'])
        links = df.rename(columns={'strength':'value'})
        return links.to_dict('records')

class ContentsExtractor(Data):

    def __init__(self):
        Data.__init__(self)
        filter = {'contents':{'$ne':None}}
        projection = {'_id':1, 'contents':1}
        self.data = self.find(filter, projection)

    #def extract_keywords(self):

    def update_many_keywords(self):
        self.tokenize_contents()
        for d in self.data:
            filter = {'_id':d['_id']}
            update = {'$set':{'keywords':d['tokens']}}
            UpdateResult = db[self.tblname].update_one(filter, update, upsert=False)
            print(f"\n\n UpdateResult :\n\n{UpdateResult}")

    def tokenize_contents(self):
        data = self.data
        self.data = []
        for d in data:
            d['tokens'] = inltk.get_tokens(text=d['contents'], lang='english')
            self.data.append(d)

    def report_term_frequency(self):
        self.get_tbl_of_contents()
        df = pd.DataFrame(self.data)
        inltk.count_tokens(texts=list(df.contents), lang='english')

class NameExtractor(Data):

    def __init__(self):
        Data.__init__(self)

class
