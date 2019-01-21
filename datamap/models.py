
from datamap import *


class Datum:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.tblname = 'data'

    def doc(self):
        return {'name':self.name, 'url':self.url}


class Data:
    def __init__(self):
        self.tblname = 'data'
        self.data = []

    def stack(self, name, url, keywords=[]):
        self.data.append({'name':name, 'url':url, 'keywords':keywords})

    def insert_many(self):
        """http://api.mongodb.com/python/current/api/pymongo/results.html#pymongo.results.InsertManyResult
        """
        return db[self.tblname].insert_many(self.data)

    def print(self):
        print('\n\n data :\n')
        pp.pprint(self.data)

    def find(self, filter=None, projection=None):
        cursor = db[self.tblname].find(filter, projection)
        return list(cursor)


    def __저장_중복제거_백업(self):
        """d = dic.copy()
        DataMap.대상_분류값li에_삽입(d['대상명'], d['출처'], d['대상내용'])
        DataMap.대상_분류값li_중복제거_백업()"""

class Bookmark:
    def __init__(self):
        self.tblname = ''
