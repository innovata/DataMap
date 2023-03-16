
from datamap import *

from datamap.keywords import *
from datamap import ifile

import unittest
import re
from bson.objectid import ObjectId

@unittest.skip("showing class skipping")
class DataNameParserTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__parse_keywords_part__unmatched(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        name = "[JTBC 대선토론] 2017 대통령 후보 초청 토론회 -1부 다시보기- - YouTube"
        d = DataNameParser(name)
        d.parse_keywords_part()
        self.assertEqual(len(d.keywords), 0)
        self.assertTrue(name is d.title)

    #@unittest.skip("demonstrating skipping")
    def test__parse_keywords_part__matched(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        name = "3.30(금) 김어준의뉴스공장 / 송영길, 나경원, 강윤기, 안원구, 황교익, 김은지__[천안함사건,연평도포격]"
        d = DataNameParser(name)
        d.parse_keywords_part()
        self.assertEqual(len(d.keywords), 2)
        self.assertFalse(name is d.title)

    #@unittest.skip("demonstrating skipping")
    def test__parse_title_part__pdf(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        name = "Visual-Reconstruction__Andrew-Blake, Andrew-Zisserman__The-MIT-Press-Cambridge__ISBN-0-262-02271-0__1987.pdf"
        d = DataNameParser(name)
        d.parse_keywords_part()
        d.parse_title_part()
        self.assertEqual(d.title, 'Visual-Reconstruction')
        self.assertEqual(d.author, 'Andrew-Blake, Andrew-Zisserman')
        self.assertEqual(d.publisher, 'The-MIT-Press-Cambridge')
        self.assertEqual(d.year, '1987')

    #@unittest.skip("demonstrating skipping")
    def test__parse_title_part__bookmark(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        name = "3.30(금) 김어준의뉴스공장 / 송영길, 나경원, 강윤기, 안원구, 황교익, 김은지__[천안함사건,연평도포격]"
        d = DataNameParser(name)
        d.parse()
        self.assertEqual(d.title, '3.30(금) 김어준의뉴스공장 / 송영길, 나경원, 강윤기, 안원구, 황교익, 김은지')
        self.assertEqual(d.author, None)
        self.assertEqual(d.publisher, None)
        self.assertEqual(d.year, None)

@unittest.skip("showing class skipping")
class TextCleanerTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test_init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        t = TextCleaner()
        #dbg.print_obj(t)
        self.assertTrue( isinstance(t.patterns, list) )
        self.assertTrue( isinstance(t.pattern, str) )

    #@unittest.skip("demonstrating skipping")
    def test_update_pattern(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        t = TextCleaner()
        t.update_pattern(addi_pattern='test_pat')
        self.assertRegex(t.pattern, 'test_pat')
        self.assertIn('test_pat', t.patterns)

    #@unittest.skip("demonstrating skipping")
    def test_clean(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        t = TextCleaner()

        title = "외국인이 말하는 한국에 대한 오해 [외국인 반응 | 코리안브로스]"
        title = t.clean(text=title)
        self.assertEqual(title, "외국인이 말하는 한국에 대한 오해 ")

        title = "외국인이 말하는 한식 오해와 편견 [외국인 반응 | 코리안브로스 X 한국바로알림서비스]__[스페인여자-라라]"
        title = t.clean(text=title)
        self.assertEqual(title, "외국인이 말하는 한식 오해와 편견 __[스페인여자-라라]")

        title = "6.13(수) 김어준의 뉴스공장 / 정세현, 박지원, 김준형, 양지열 - YouTube"
        title = t.clean(text=title)
        self.assertEqual(title, "6.13(수) 김어준의 뉴스공장 / 정세현, 박지원, 김준형, 양지열")

@unittest.skip("showing class skipping")
class ExtractorTestCase(unittest.TestCase):

    text = "외국인이 말하는 한식 오해와 편견 [외국인 반응 | 코리안브로스 X 한국바로알림서비스]__[스페인여자-라라]"
    keywords = ['스페인여자-라라']

    #@unittest.skip("demonstrating skipping")
    def test_split_langs(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        e = Extractor(self.text, self.keywords)
        e.split_langs()
        print(f"\n e.linguistic_text : {e.linguistic_text}\n")
        self.assertTrue( isinstance(e.linguistic_text, object) )

    #@unittest.skip("demonstrating skipping")
    @unittest.expectedFailure
    def test_extract_keywords_from_each_lang(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        d = DataNameParser(name=self.text).parse()
        title = TextCleaner().clean(text=d.title)

        e = Extractor(text=title, keywords=d.keywords)
        e.split_langs()
        e.extract_keywords_from_each_lang()
        self.assertEqual(set(e.keywords), set(['스페인여자-라라','외국인','한식','오해','편견']))

@unittest.skip("showing class skipping")
class DataNameExtractorTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        dn = DataNameExtractor()
        #dbg.print_obj(dn)
        self.assertEqual(dn.tblname, 'Data')
        self.assertTrue( isinstance(dn.docs, list) )
        self.assertIsNot(len(dn.docs), 0)

        # docs 로딩 projection 이 올바른지 확인.
        df = dn.get_df()
        cols = list(df.columns)
        #print(f"\n\n cols : {cols}\n\n")
        self.assertEqual(set(cols), set(['_id','name','keywords']))

    @unittest.skip("demonstrating skipping")
    def test_check_cols(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        dn = DataNameExtractor()

    @unittest.skip("demonstrating skipping")
    def test_extract_keywords_one_cycle(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        dn = DataNameExtractor()
        # 강제 변환.
        dn.docs = [{
            '_id': ObjectId('5c560da0b46a3a088a215a30'),
            'keywords': ['coding-skill'],
            'name': 'CS50 Lecture by Mark Zuckerberg '
        }]
        dn.extract_keywords()
        #dbg.print_obj(n)
        predicted_keywords = ['Cs','Lecture','Mark','Zuckerberg']
        for kw in predicted_keywords:
            print(f"\n keyword : {kw}\n")
            self.assertIn(kw, dn.docs[0]['keywords'])

    #@unittest.skip("demonstrating skipping")
    def test_process(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        dn = DataNameExtractor()
        dn.process()

@unittest.skip("showing class skipping")
class KeywordFrequencyTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordFrequency()
        #dbg.print_obj(k)
        self.assertEqual(k.tblname, 'Keyword')
        self.assertEqual(list(k.df.columns), ['keywords'])

    @unittest.skip("demonstrating skipping")
    def test_calc_frequency(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordFrequency()
        k.calc_frequency()
        print(f"\n k.freqdf :\n\n {k.freqdf}\n")
        self.assertEqual(set(list(k.freqdf.columns)), set(['keyword','freq']))

    #@unittest.skip("demonstrating skipping")
    def test_analysis_process(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordFrequency()
        k.analysis_process()
        df = k.load(projection = {'_id':0}).get_df()
        dbg.print_df(df)
        self.assertEqual(set(list(df.columns)), set(['keyword','freq']))

@unittest.skip("showing class skipping")
class KeywordCombinationStrengthTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength()
        #dbg.print_obj(k)
        self.assertEqual(k.tblname, 'KeywordCombination')
        # 키워드 조합을 만들기 위한 재료는 Data 테이블의 keywords 컬럼이다.
        self.assertEqual(list(k.df.columns), ['keywords'])

    @unittest.skip("demonstrating skipping")
    def test_make_combinations_col(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength()
        k.make_combinations_col()
        self.assertEqual(set(list(k.df.columns)), set(['keywords','combinations']))
        sample_tuples = list(k.df.combinations)[0]
        self.assertTrue( isinstance(sample_tuples[0], tuple) )

    @unittest.skip("demonstrating skipping")
    def test_get_combinations(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength()
        k.make_combinations_col()
        k.get_combinations()
        sample_combination = list(k.combinations)[0]
        self.assertTrue( isinstance(sample_combination, tuple) )

    @unittest.skip("demonstrating skipping")
    def test_calc_combination_strengths(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength()
        k.make_combinations_col().get_combinations().calc_combination_strengths()
        df = k.get_df()
        dbg.print_df(df)
        self.assertEqual(set(list(df.columns)), set(['combination','strength']))

    @unittest.skip("demonstrating skipping")
    def test_analysis_process(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength()
        k.analysis_process()
        df = k.load(projection = {'_id':0}).get_df()
        dbg.print_df(df)
        self.assertEqual(set(list(df.columns)), set(['combination','strength']))

@unittest.skip("showing class skipping")
class KeywordRemoverTestCase(unittest.TestCase):

    filepath = f"{DATA_PATH}/KeywordRemover.txt"

    #@unittest.skip("demonstrating skipping")
    def test_load_existed_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordRemover(self.filepath)
        #dbg.print_obj(k)
        self.assertTrue( isinstance(k.keywords, list) )
        print(f"\n k.keywords :\n\n{k.keywords}\n")

    @unittest.skip("demonstrating skipping")
    def test_save_usless_keyword(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordRemover(self.filepath)
        #dbg.print_obj(k)
        k.save_usless_keyword(keyword='test_keyword')
        text = ifile.open_file(self.filepath)
        print(f"\n text :\n\n{text}\n")
        self.assertRegex(text, 'test_kw')

    @unittest.skip("demonstrating skipping")
    def test_delete_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordRemover(self.filepath)
        #dbg.print_obj(k)
        k.delete_keywords()
        dbg.print_DeleteResult(k.DeleteResult)

    #@unittest.skip("demonstrating skipping")
    def test_save_and_delete_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordRemover(self.filepath)
        #dbg.print_obj(k)
        k, kc = k.save_usless_keyword(keyword='말').delete_keywords()
        dbg.print_DeleteResult(k.DeleteResult)
        dbg.print_DeleteResult(kc.DeleteResult)
        # 눈으로 확인 및 신규 쓸모없는 키워드 수동으로 추적.
        k = KeywordCombinationStrength()
        df = k.load(projection = {'_id':0}).get_df()
        dbg.print_df(df)

#@unittest.skip("showing class skipping")
class KeywordFilterTestCase(unittest.TestCase):

    filepath = f"{DATA_PATH}/KeywordFilter.txt"

    #@unittest.skip("demonstrating skipping")
    def test_save_all_keywords_in_file(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordFilter(self.filepath)
        k.save_all_keywords_in_file()
        #text = ifile.open_file(self.filepath)
        #print(f"\n text :\n\n{text}\n")

    @unittest.skip("demonstrating skipping")
    def test_find_valuable_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        df = KeywordFilter(self.filepath).load(projection={'_id':0}).get_df()
        print(f"\n df :\n\n {df}\n")
        print(f"\n keywords :\n\n{sorted(df.keyword)}\n")

@unittest.skip("showing class skipping")
class MainTestCase(unittest.TestCase):

    def test_main_process(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        main_process()



def main():
    unittest.main()
