
from datamap import *
from bs4 import BeautifulSoup
import itertools
from ipdf import ifitz
import fitz
import inltk

from .models import Data, Datum


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

def get_filepaths(path):
    filepaths = []
    for root, dirs, files in os.walk(top=path, topdown=True):
        #print(f"\n\n root: {root}\n\n dirs: {dirs}\n\n files: {files}")
        for file in files:
            if file not in ['.DS_Store']:
                filepaths.append(os.path.join(root, file))
    return filepaths

class PDF(Data):

    def __init__(self, path):
        Data.__init__(self)
        filepaths = get_filepaths(path)
        self.pdfs = []
        for filepath in filepaths:
            root, ext = os.path.splitext(filepath)
            if ext == '.pdf': self.pdfs.append(f"file://{filepath}")

    def process(self):
        self.get_ebook_ToC()
        self.get_noebook_ToC()
        self.insert_data()

    def get_ebook_ToC(self):
        for pdf in self.pdfs:
            head, tail = os.path.split(pdf)
            contents = ifitz.get_tbl_of_contents(pdf)
            d = Datum(name=tail, url=pdf, contents=contents)
            self.data.append(d.get_doc())

    def get_noebook_ToC(self):
        df = pd.DataFrame(self.data)
        df1 = df[ df.contents.isin([None]) ]
        df2 = df[ ~df.contents.isin([None]) ]
        df1.contents = df1.url.apply(ifitz.get_text)
        self.data = pd.concat([df1, df2]).to_dict('records')

class Course(Data):

    Data.modeltype = 'course'
