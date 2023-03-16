
import unittest

from datamap.data import *
from datamap import DATA_PATH






@unittest.skip("showing class skipping")
class LocalfileTestCase(unittest.TestCase):

    path = "/Users/sambong/stand-alone-ebook"

    @unittest.skip("demonstrating skipping")
    def test__filter_useful_filepaths(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        l = Localfile(self.path)
        filepaths = ifile.get_filepaths(l.path)
        l.filter_useful_filepaths(filepaths)
        pp.pprint(l.filepaths)

    #@unittest.skip("demonstrating skipping")
    def test__make_data(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        l = Localfile(self.path)
        filepaths = ifile.get_filepaths(l.path)
        l.filter_useful_filepaths(filepaths)
        l.make_data()

        dbg.print_docs(l)
        self.assertFalse(len(l.docs) is 0)
        df = l.get_df()
        self.assertEqual(set(['name','url','keywords']), set(list(df.columns)))

    @unittest.skip("demonstrating skipping")
    def test__process(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        l = Localfile(self.path)
        l.process()
        exp = l.find(filter={'dtype':'localfile'}).explain_cursor()
        self.assertEqual(len(l.docs), exp['executionStats']['nReturned'])

    def test__empty_keywords_col(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        l = Localfile(self.path)

        filter = {'keywords':None}
        l.load(filter)
        dbg.print_docs(l)
        update = {'$set':{'keywords':[]}}
        l.update_many(filter, update, False)
        dbg.print_UpdateResult(l.UpdateResult)


@unittest.skip("showing class skipping")
class DataHandlerTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test__change_keyword_manually(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordConverter()

        k.docs = [
            {'id': ObjectId('5c65eb72b46a3a106c4433c0'),
            'keywords': ['드라마','중국어','듣기','읽기'],
            'name': '致我们单纯的小美好(S01E02)'},
            {'id': ObjectId('5c65eb72b46a3a106c4433c1'),
            'keywords': ['드라마','중국어','듣기','읽기'],
            'name': '致我们单纯的小美好 - Google Search'},
        ]
        k.change_keyword_manually()

        df = k.get_df()
        dbg.print_df(df)
        ids = list(df.id)
        k.load(filter={"_id":{'$in':ids}})
        dbg.print_docs(k)


def main():
    unittest.main()
