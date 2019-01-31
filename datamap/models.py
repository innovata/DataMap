
from datamap import *
from bs4 import BeautifulSoup
import itertools
from .imongo import *

class Datum:

    def __init__(self, name, url, keywords=[], contents=None):
        self.name = name
        self.url = url
        self.keywords = keywords
        self.contents = contents

    def get_doc(self):
        return {'name':self.name, 'url':self.url, 'keywords':self.keywords, 'contents':self.contents}

    #def update_one(self):


class Data:

    def __init__(self):
        self.tblname = 'Data'
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

    def insert_data(self):
        """http://api.mongodb.com/python/current/api/pymongo/results.html#pymongo.results.InsertManyResult
        """
        self.InsertManyResult = db[self.tblname].insert_many(self.data)

    def drop_tbl(self):
        db[self.tblname].drop()

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

    def rename_tbl(self, new_name):
        db[self.tblname].rename(new_name)

class Keyword:

    def __init__(self):
        self.tblname = 'Keyword'

    def find(self, filter=None, projection=None):
        return find(self, filter, projection)

    def update_one(self):
        update_one(self, filter, update)

    def insert_data(self):
        insert_data(self)

    def delete_many(self, filter):
        db[self.tblname].delete_many(filter)

    def drop_tbl(self):
        db[self.tblname].drop()

    def rename_tbl(self, new_name):
        db[self.tblname].rename(new_name)

class KeywordCombination:

    def __init__(self):
        self.tblname = 'KeywordCombination'

    def find(self, filter=None, projection=None):
        return find(self, filter, projection)

    def insert_data(self):
        insert_data(self)
