
from datamap import *

from datamap.models import *

import unittest

#@unittest.skip("showing class skipping")
class DataTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        d = Data()

        self.assertTrue(d.tblname is 'Data')

    #@unittest.skip("demonstrating skipping")
    def test__load_matching_regex_keyword(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        d = Data()
        regex = "^중용"
        projection = {'_id':1,'keywords':1,'category':1}
        d.load_matching_regex_keyword(regex, 'i', projection)

        dbg.print_docs(d)
        #self.assertTrue(len(d.docs) is 0)

@unittest.skip("showing class skipping")
class KeywordTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        k = Keyword('Neuro-linguistic programming','Tech')

        dbg.print_obj(k)
        k.insert_doc()
        k.load(filter={'keyword':'Neuro-linguistic programming'})
        dbg.print_docs(k)

@unittest.skip("showing class skipping")
class KeywordCombinationTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n\n testfuncname : {inspect.stack()[0][3]}")
        k = KeywordCombination()
        #dbg.print_obj(k)
        self.assertEqual(k.tblname, 'KeywordCombination')

    @unittest.skip("demonstrating skipping")
    def test__load(self):
        print(f"\n\n testfuncname : {inspect.stack()[0][3]}")
        k = KeywordCombination()
        df = k.load()




def main():
    unittest.main()
