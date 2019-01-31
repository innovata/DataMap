
from datamap import *
import itertools
from .models import Data, Keyword, KeywordCombination
from .imongo import *


class Cursor(Data, Keyword, KeywordCombination):
    """https://api.mongodb.com/python/current/api/pymongo/cursor.html
    """
    def __init__(self):
        self.d = Data()
        self.k = Keyword()
        self.kc = KeywordCombination()

    def explain(self):
        cursor = db[self.d.tblname].find()
        self.print_explain(cursor)

        cursor = db[self.k.tblname].find()
        self.print_explain(cursor)

        cursor = db[self.kc.tblname].find()
        self.print_explain(cursor)

    def print_explain(self, cursor):
        print(f"\n\n cursor_explain :\n")
        pp.pprint(cursor.explain())
