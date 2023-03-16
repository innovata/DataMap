# ============================================================ Python.
import sys
import re
# ============================================================ External-Library.
import requests
# ============================================================ My-Library.
from ipdf import PyMuPDF as ifitz
# ============================================================ Project.
from datamap import models
from datamap import PJTS_PATH
# ============================================================ Constant.


class PDF(models.Data):

    def __init__(self):
        super().__init__()
        filter = {'name':{'$regex':'\.pdf$', '$options':'i'}}
        projection = {'_id':1, 'name':1, 'url':1}
        cursor = db[self.tblname].find(filter, projection)
        self.docs = list(cursor)

    def process(self):
        self.get_ebook_ToC()
        self.get_noebook_ToC()
        self.update_data()

    def get_ebook_ToC(self):
        for d in self.docs:
            pdf = d['url'].replace('file://','')
            head, tail = os.path.split(pdf)
            d['contents'] = ifitz.get_tbl_of_contents(pdf)
            self.data.append(d)

    def get_noebook_ToC(self):
        df = pd.DataFrame(self.data)
        #df1 = df[ df.contents.isin([None]) ]
        #df2 = df[ ~df.contents.isin([None]) ]
        df1 = df[ df.contents.isna() ]
        df2 = df[ ~df.contents.isna() ]
        df1.contents = df1.url.apply(ifitz.get_text)
        self.data = pd.concat([df1, df2]).to_dict('records')

    def update_data(self):
        for d in self.data:
            """handle_pandas_error : '_id' => '_0'
            """
            filter = {'_id':d['_0']}
            update = {'$set':{'contents':d['contents']}}
            db[self.tblname].update_one(filter, update)


class HTML(models.Data):

    def __init__(self):
        super().__init__()
        filter = {'url':{'$regex':'http.://'}}
        projection = {'_id':1, 'name':1, 'url':1}
        self.cursor = db[self.tblname].find(filter, projection)
        docs = list(self.cursor)
        p = re.compile(pattern='youtube.com')
        for d in docs:
            if p.search(string=d['url']) is None:
                self.data.append(d)

    def process(self):
        #self.get_ebook_ToC()
        #self.get_noebook_ToC()
        self.update_data()

    def collect_contents(self):
        """https://scrapy.org"""


class YouTube(models.Data):

    def __init__(self):
        super().__init__()
        filter = {'url':{'$regex':'http.://.+youtube.com'}}
        projection = {'_id':1, 'name':1, 'url':1}
        self.cursor = db[self.tblname].find(filter, projection)
        self.data = list(self.cursor)

    def process(self):
        #self.get_ebook_ToC()
        #self.get_noebook_ToC()
        self.update_data()

    def collect_contents(self):
        """
        방법1
        유투브로부터 음성만 다운로드 후,
        방법2
        유투브 영상 다운로드 후, 영상으로부터 음성을 별도로 추출
        공통
        음성인식으로 텍스트를 추출하여 저장.
        """
