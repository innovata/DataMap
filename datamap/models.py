
from datamap import *
from bs4 import BeautifulSoup


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
