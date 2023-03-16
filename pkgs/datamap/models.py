print(f"{'@'*50} {__name__}")
# ============================================================ Python.
# ============================================================ External-Library.
# ============================================================ My-Library.
from ipymongo import mongo
# ============================================================ Project.
# ============================================================ Constant.
class Bookmark(mongo.Model):
    sample_schema = {
        'name':'',
        'url':'',
        'keywords':[],
        'category':''
    }
    id_cols = ['name','url']
    schema = list(sample_schema)
    def __init__(self):
        self.modeling(__class__)


# class Data(mongo.Model):
#
#     def __init__(self):
#         super().__init__(__class__)
#         self.handle_flocals(inspect.currentframe())
#         #self.handle_args(args)
#         self.schema = ['name','url','dtype','keywords','contents','category','tokens']
#
#     def load_matching_regex_keyword(self, regex, options, projection):
#         filter = {'keywords':{'$elemMatch':{'$regex':regex}}}
#         if options is not None:
#             filter['keywords']['$elemMatch']['$options'] = options
#         return self.load(filter, projection)
#
#     def emit_csv(self):
#         df = self.load({},{'_id':0}).get_df()
#         df.to_csv(f"{DATA_PATH}/model_data.csv",index=False)
#
#
# class Keyword(mongo.Model):
#
#     def __init__(self):
#         super().__init__(__class__)
#         self.handle_flocals(inspect.currentframe())
#         self.schema = ['keyword','category','freq','lang']
#
#     def deduplicate(self):
#         subset = ['category','keyword']
#
#
# class KeywordCombination(mongo.Model):
#
#     def __init__(self):
#         super().__init__(__class__)
#         self.schema = ['combination','strength']
#         self.handle_flocals(inspect.currentframe())
