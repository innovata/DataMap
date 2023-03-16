
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
import sys
sys.path.append('/Users/sambong/pjts/datamap')
from datamap import mongo


class Data(mongo.Model):

    def __init__(self):
        super().__init__(__class__)
        self.schema = ['name','url','contents','keywords','category','dtype','tokens']
        #self.handle_args(args)
        self.handle_flocals(inspect.currentframe())

    def load_matching_regex_keyword(self, regex, options, projection):
        filter = {'keywords':{'$elemMatch':{'$regex':regex}}}
        if options is not None:
            filter['keywords']['$elemMatch']['$options'] = options
        return self.load(filter, projection)



class Keyword(mongo.Model):

    def __init__(self):
        super().__init__(__class__)
        self.schema = ['keyword','category','freq']
        self.handle_flocals(inspect.currentframe())

    def load_keywords(self):
        df = self.load(projection={'_id':0, 'keyword':1}).get_df()
        self.keywords = list(df.keyword)

    def deduplicate(self):
        subset = ['category','keyword']

class KeywordCombination(mongo.Model):

    def __init__(self):
        super().__init__(__class__)
        self.schema = ['combination','strength']
        self.handle_flocals(inspect.currentframe())

class Bookmark(mongo.Model):

    def __init__(self, name=None, url=None, contents=None, keywords=[], category=None):
        super().__init__(inspect.currentframe())
        self.tblname = __class__.__name__
