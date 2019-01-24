
from datamap import *
from bs4 import BeautifulSoup
import itertools

class Datum:

    def __init__(self, name, url, keywords=[]):
        self.name = name
        self.url = url
        self.keywords = keywords
        self.contents = None

    def get_doc(self):
        return {'name':self.name, 'url':self.url, 'keywords':self.keywords}

class Data:

    def __init__(self):
        self.tblname = 'data'
        self.data = []

    def process_analysis():
        print('')

    def open_file(self):
        with open(file=self.filepath, mode='r') as f:
            self.text = f.read()
            f.close()

    def stack(self, name, url, keywords=[]):
        d = Datum(name, url, keywords)
        self.data.append(d.get_doc())

    def print_data(self):
        print('\n\n data :\n')
        pp.pprint(self.data)

    def insert_many(self):
        """http://api.mongodb.com/python/current/api/pymongo/results.html#pymongo.results.InsertManyResult
        """
        return db[self.tblname].insert_many(self.data)

    def find(self, filter=None, projection=None):
        cursor = db[self.tblname].find(filter, projection)
        return list(cursor)

    def docs_to_csv(self, filename):
        docs = self.find(projection={'_id':0})
        df = pd.DataFrame(docs)
        df.to_csv(f"{DATA_PATH}/{filename}")

    def __저장_중복제거_백업(self):
        """d = dic.copy()
        DataMap.대상_분류값li에_삽입(d['대상명'], d['출처'], d['대상내용'])
        DataMap.대상_분류값li_중복제거_백업()"""

class Bookmark(Data):
    """# 상속받은 클래스 검사.
    print(f"\n\n Data : {Data}")
    print(f"\n\n dir(Data) :\n\n {dir(Data)}")
    print(f"\n\n Data.__dict__ :\n\n {Data.__dict__}")
    """
    """# 상속받은 후 초기화를 하면 기존 상속받은 클래스는 날라 간다.
    def __init__(self):
        self.book = 'book'
        print(f"\n\n self.book : {self.book}")
        test_print()
    """
    """# 신규 변수 셋업. --> 정상.
    Data.book = 'book'
    print(f"\n\n Data.book : {Data.book}")
    Data.modeltype = 'bookmark'
    Data.filepath = 'filepath'
    Data.sections = ['즐겨찾기','Repository']
    Data.meaningless_keywords = ['책갈피 메뉴','읽기 목록'] + Data.sections
    Data.folder_tag = 'h3'
    """

    def __init__(self, filepath):
        Data.__init__(self)
        self.modeltype = 'bookmark'
        self.filepath = filepath
        self.sections = ['즐겨찾기','Repository']
        self.meaningless_keywords = ['책갈피 메뉴','읽기 목록'] + self.sections
        self.folder_tag = 'h3'

    def print_self(self):
        print(f"\n\n self : {self}")
        print(f"\n\n dir(self) :\n\n {dir(self)}")
        print(f"\n\n self.__dict__ :\n")
        pp.pprint(self.__dict__)

    def collect(self):
        self.parse()
        self.print_data()
        self.insert_many()

    def parse(self):
        self.open_file()

        soup = BeautifulSoup(self.text, 'html.parser')
        for section in self.sections:
            section = soup.find(self.folder_tag, string=section)
            section = section.find_next_sibling('dl')
            links = section.find_all('a')
            for link in links:
                foldernames = []
                dls = link.find_parents('dl')
                for dl in dls:
                    folder_tag = dl.find_previous_sibling(self.folder_tag)
                    if folder_tag is not None:
                        foldernames.append(folder_tag.string)

                # 의미없는 폴더명 제거.
                foldernames = list(set(foldernames))
                for u in self.meaningless_keywords:
                    if u in foldernames: foldernames.remove(u)

                self.stack(name=link.string, url=link['href'], keywords=foldernames)

class Localfile(Data):

    Data.modeltype = 'localfile'

class Course(Data):

    Data.modeltype = 'course'

class Keyword(Data):

    def __init__(self):
        self.tblname = 'keyword'
        self.keywords = []

    def process(self):
        print('Flow.')

    def load_data(self):
        d = Data()
        docs = d.find(projection={'_id':0})
        return pd.DataFrame(docs)

    def get_unique_keywords(self):
        df = self.load_data()
        keywords_li = list(df.keywords)
        uq_keywords = []
        for keywords in keywords_li:
            for keyword in keywords:
                uq_keywords.append(keyword)
        self.keywords = sorted(set(uq_keywords))

    def get_keywords_frequency(self):
        df = self.load_data()
        keywords_li = list(df.keywords)
        li = []
        for keywords in keywords_li:
            for keyword in keywords:
                li.append(keyword)
        df = pd.DataFrame({'keyword':li, 'cnt':1})
        gsum = df.groupby('keyword').sum()
        gsum['keyword'] = gsum.index
        gsum = gsum.rename(columns={'cnt':'freq'})
        self.keywords_freq = gsum.to_dict('records')

    def add_keywords_combinations_col(self):
        def combinations(x):
            if isinstance(x, list):
                if len(x) > 1:
                    tuples = list(itertools.combinations(set(x), 2))
                    return tuples#[list(tuple) for tuple in tuples]

        df = self.load_data()
        df = df.assign(kw_combs= lambda x: x.keywords.apply(combinations))
        # 필터링이 안되네....
        #df = df[ df['kw_combs'] != None ]
        self.df = df

    def get_keywords_combinations(self):
        self.add_keywords_combinations_col()
        kw_combs_li = list(self.df.kw_combs)
        uq_kw_combs = []
        for kw_combs in kw_combs_li:
            if (kw_combs is not None) and isinstance(kw_combs, list):
                for kw_comb in kw_combs:
                    uq_kw_combs.append(kw_comb)

        self.kw_combinations = list(set(uq_kw_combs))

    def calc_combination_strength(self):

        class Combination:

            def __init__(self, combination):
                self.comb = combination
                self.strength = 0

            def calc_strength(self, x):
                if isinstance(x, list) and (self.comb in x):
                    self.strength += 1

            def print(self):
                print(f"\n\n combination : {self.comb}")
                print(f"\n strength : {self.strength}")

            def get_doc(self):
                return {'combination':self.comb, 'strength':self.strength}

        self.add_keywords_combinations_col()
        df = self.df
        self.get_keywords_combinations()
        self.combination_strengths = []
        for combination in self.kw_combinations:
            c = Combination(combination)
            df.kw_combs.apply(lambda x: c.calc_strength(x))
            self.combination_strengths.append(c.get_doc())

    def make_keyword_relation(self):
        self.calc_combination_strength()
        relations = pd.DataFrame(self.combination_strengths)
        relations['keyword'] = relations.combination.apply(lambda x: x[0])
        relations['name'] = relations.combination.apply(lambda x: x[1])
        del(relations['combination'])

        self.get_keywords_frequency()
        keywords = pd.DataFrame(self.keywords_freq).rename(columns={'keyword':'name'}).to_dict('records')
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
