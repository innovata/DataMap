# ============================================================ Python.
import re
import copy
# ============================================================ External-Library.
from bs4 import BeautifulSoup
import pandas as pd
# ============================================================ My-Library.
from iipython import ifile
# ============================================================ Project.
from datamap import models
from datamap import DATA_PATH
# ============================================================ Constant.





def mark_dtype(clss, dtype):
    df = clss.get_df()
    df = df.assign(dtype= dtype)
    clss.docs = df.to_dict('records')
    return clss





def refine_upon_bookmark():
    b = Bookmark(f"{DATA_PATH}/Safari-책갈피__2019-03-30.html",['bookmark','즐겨찾기','책갈피 메뉴','읽기 목록'])
    b.refine_upon_bookmark()


class Localfile(models.Data):
    """
    - 정상 pdf파일(문자열로 인식가능한)의 목차를 읽어서 대상내용 컬럼에 저장.
    - 비정상 pdf파일(이미지로 인식해야하는) 상동.
    """
    def __init__(self, path, ftypes=[]):
        super().__init__()
        self.path = path
        self.define_useful_ftypes(ftypes)

    def process(self):
        filepaths = ifile.get_filepaths(self.path)
        self.filter_useful_filepaths(filepaths)
        self.make_data()
        self = mark_dtype(self, 'localfile')
        #self.insert_docs()

    def define_useful_ftypes(self, ftypes):
        apple_docs = ['.pages', '.numbers', '.key']
        ms_docs = ['.docx', '.xlsx', '.pptx']
        docs = ['.pdf', '.hwp'] + apple_docs + ms_docs
        pics = ['.jpg', '.jpeg', '.png']
        self.ftypes = (docs + pics + ftypes)

    def filter_useful_filepaths(self, filepaths):
        useful_filepaths = []
        for filepath in filepaths:
            root, ext = os.path.splitext(filepath)
            if ext in self.ftypes:
                useful_filepaths.append(filepath)
        self.filepaths = useful_filepaths
        return self

    def make_data(self):
        for filepath in self.filepaths:
            head, tail = os.path.split(filepath)
            self.docs.append({'name':tail, 'url':f"file://{filepath}", 'keywords':[]})
        return self


class Gdrive(models.Data):

    def __init__(self):
        super().__init__()
