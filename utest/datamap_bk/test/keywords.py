
from datamap import *

from datamap.keywords import *
from datamap import models
from datamap import ifile


import unittest
import re
from bson.objectid import ObjectId
from pandas.io.json import json_normalize



@unittest.skip("showing class skipping")
class DataNameParserTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test___split_keywords_part__unmatched(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        name = "[JTBC 대선토론] 2017 대통령 후보 초청 토론회 -1부 다시보기- - YouTube"
        d = DataNameParser(name)
        d.split_keywords_part()

        self.assertEqual(len(d.keywords), 0)
        self.assertTrue(name is d.title)

    @unittest.skip("demonstrating skipping")
    def test___split_keywords_part__matched(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        name = "3.30(금) 김어준의뉴스공장 / 송영길, 나경원, 강윤기, 안원구, 황교익, 김은지__[천안함사건,연평도포격]"
        d = DataNameParser(name)
        d.split_keywords_part()

        self.assertEqual(len(d.keywords), 2)
        self.assertFalse(name is d.title)

    @unittest.skip("demonstrating skipping")
    def test___split_title_part__pdf(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        name = "Visual-Reconstruction__Andrew-Blake, Andrew-Zisserman__The-MIT-Press-Cambridge__ISBN-0-262-02271-0__1987.pdf"
        d = DataNameParser(name)
        d.split_keywords_part().split_title_part()

        self.assertEqual(d.title, 'Visual-Reconstruction')
        self.assertEqual(d.author, 'Andrew-Blake, Andrew-Zisserman')
        self.assertEqual(d.publisher, 'The-MIT-Press-Cambridge')
        self.assertEqual(d.year, '1987')

    @unittest.skip("demonstrating skipping")
    def test___split_title_part__bookmark(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        name = "3.30(금) 김어준의뉴스공장 / 송영길, 나경원, 강윤기, 안원구, 황교익, 김은지__[천안함사건,연평도포격]"
        d = DataNameParser(name)
        d.parse()

        self.assertEqual(d.title, '3.30(금) 김어준의뉴스공장 / 송영길, 나경원, 강윤기, 안원구, 황교익, 김은지')
        self.assertEqual(d.author, None)
        self.assertEqual(d.publisher, None)
        self.assertEqual(d.year, None)

    #@unittest.skip("demonstrating skipping")
    def test___parse_bookmark(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        docs = models.Data().load(filter={'dtype':'bookmark'}).docs
        for d in docs:
            dn = DataNameParser(name=d['name'])
            dn.parse()
            d['name'] = dn.title
            d['keywords'] += dn.keywords
        dbg.print_dics(docs)

@unittest.skip("showing class skipping")
class DatanameExtractorTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        de = DatanameExtractor()

        #dbg.print_obj(de)
        self.assertEqual(de.tblname, 'Data')

    #@unittest.skip("demonstrating skipping")
    def test__extract_by_datanameparser(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        de = DatanameExtractor()
        de.extract_by_datanameparser()

        if True:# 테스트가 아니면 DB에서 재로딩.
            de.load({'dtype':'bookmark'}, {'_id':1,'name':1,'keywords':1})
        dbg.print_docs(de)

@unittest.skip("showing class skipping")
class DatanameExtractor2TestCase(unittest.TestCase):

    categories = ['Society','Interests','Tech','Lang','UPV','Asset','수신(修身)','Career']

    @unittest.skip("demonstrating skipping")
    def test__set_category_col(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        b = Bookmark(self.filepath, self.useless_keywords, self.categories)
        b.docs = [
            {'keywords': ['Career'],
            'name': 'LinkedIn',
            'url': 'https://www.linkedin.com/mynetwork/'},
            {'keywords': ['음악', 'Interests'],
            'name': 'Programme - Breakbot | Shazam',
            'url': 'https://www.shazam.com/ko/track/58735033/programme#referrer=shazamformac'},
        ]
        b.set_category_col()
        df = b.get_df()
        keywords_li = list(df.keywords)
        self.assertTrue(len(keywords_li[0]) is 0)
        self.assertEqual(keywords_li[1], ['음악'])
        self.assertEqual(set(list(df.category)), set(['Career','Interests']))
        dbg.print_docs(b)

    @unittest.skip("demonstrating skipping")
    def test__split_double_keyword_of_elem(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        b = Bookmark(self.filepath, self.useless_keywords, self.categories)
        b.docs = [{
            'keywords': ['Career',
                'double1, double2',
                'double3,double4',
                'double5,   double6'],
            'name': 'LinkedIn',
            'url': 'https://www.linkedin.com/mynetwork/'
        }]
        b.split_double_keyword_of_elem()
        self.assertEqual(set(b.docs[0]['keywords']), set(['Career','double1','double2','double3','double4','double5','double6']))
        dbg.print_docs(b)

    @unittest.skip("demonstrating skipping")
    def test__delete_categoryless_data(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        b = Bookmark(self.filepath, self.useless_keywords, self.categories)
        b.docs = [
            {'keywords': ['Career'],
            'name': 'LinkedIn',
            'url': 'https://www.linkedin.com/mynetwork/',
            'category':'test_cate'},
            {'keywords': ['음악', 'Interests'],
            'name': 'Programme - Breakbot | Shazam',
            'url': 'https://www.shazam.com/ko/track/58735033/programme#referrer=shazamformac'},
        ]
        b.delete_categoryless_data()
        self.assertTrue(len(b.docs) is 1)
        dbg.print_docs(b)

#============================================================
# keywords를 표준화, 청소(제거), 번역
#============================================================

@unittest.skip("showing class skipping")
class KeywordStandardizerTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ks = KeywordStandardizer()

        self.assertTrue(ks.tblname is 'Data')
        # 규칙적용 순서 점검.
        pp.pprint(ks.rules)
        for r in ks.rules:
            self.assertTrue(r['seq'] is 1)
            break

    @unittest.skip("demonstrating skipping")
    def test__standardize__manually(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ks = KeywordStandardizer()
        ks.rules = [{
            'keyword_regex': '^중용$',
            'standard': '중용(中庸)',
            'work': 'replace',
        }]
        ks.standardize()

        dbg.print_docs(ks)

    @unittest.skip("demonstrating skipping")
    def test__standardize__specialchars(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ks = KeywordStandardizer()
        df = pd.DataFrame(ks.rules)
        df = df.query('work == "special_char"')
        ks.rules = df.to_dict('records')
        pp.pprint(ks.rules)
        ks.standardize()

        dbg.print_docs(ks)

    @unittest.skip("demonstrating skipping")
    def test__standardize__capitalize(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ks = KeywordStandardizer()
        df = pd.DataFrame(ks.rules)
        df = df.query('work == "capitalize"')
        ks.rules = df.to_dict('records')
        pp.pprint(ks.rules)
        ks.standardize()

        dbg.print_docs(ks)

    @unittest.skip("demonstrating skipping")
    def test__standardize__upper(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ks = KeywordStandardizer()
        df = pd.DataFrame(ks.rules)
        df = df.query('work == "upper"')
        ks.rules = df.to_dict('records')
        pp.pprint(ks.rules)
        ks.standardize()

        dbg.print_docs(ks)

    @unittest.skip("demonstrating skipping")
    def test__standardize__replace(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ks = KeywordStandardizer()
        df = pd.DataFrame(ks.rules)
        df = df.query('work == "replace"')
        ks.rules = df.to_dict('records')
        pp.pprint(ks.rules)
        ks.standardize()

        dbg.print_docs(ks)

    @unittest.skip("demonstrating skipping")
    def test__standardize__split(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ks = KeywordStandardizer()
        df = pd.DataFrame(ks.rules)
        df = df.query('work == "split"')
        ks.rules = df.to_dict('records')
        pp.pprint(ks.rules)
        ks.standardize()

        dbg.print_docs(ks)

    #@unittest.skip("demonstrating skipping")
    def test__standardize(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ks = KeywordStandardizer().standardize()

        ks.load()
        dbg.print_docs(ks)

@unittest.skip("showing class skipping")
class KeywordTranslatorTestCase(unittest.TestCase):

    dictpath = f"{DATA_PATH}/Keywords-translation - Sheet1.csv"
    orig = 'korean'
    dest = 'english'

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        kt = KeywordTranslator(self.dictpath)

        df = pd.DataFrame(kt.dict)
        self.assertEqual(set(['english','korean','spanish']), set(list(df.columns)))

    #@unittest.skip("demonstrating skipping")
    def test__get_words(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        kt = KeywordTranslator(self.dictpath)
        words = kt.get_words()
        pp.pprint(words)
        #kt.save_words_to_xls()

    @unittest.skip("demonstrating skipping")
    def test__translate_keywords__manually(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        kt = KeywordTranslator(self.dictpath)
        kt.dict =  [{'english': 'Open data', 'korean': '오픈데이터', 'spanish': 'Datos abiertos'}]

        d = models.Data()
        orig_word = kt.dict[0][self.orig]
        projection = {'_id':1,'keywords':1,'category':1}
        d.load_matching_regex_keyword(f"^{orig_word}$", None, projection)
        d.docs = kt.translate_keywords(d.docs, self.orig, self.dest)

        dbg.print_docs(d)
        if len(d.docs) is not 0:
            df = json_normalize(d.docs, 'keywords').rename(columns={0:'keyword'})
            self.assertNotIn(kt.dict[0][self.orig], list(df.keyword.unique()))

    @unittest.skip("demonstrating skipping")
    def test__translate_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        kt = KeywordTranslator(self.dictpath)

        filter = {'category':{'$ne':None}}
        projection = {'_id':1,'keywords':1,'category':1}
        d = models.Data().load(filter, projection)
        d.docs = kt.translate_keywords(d.docs, self.orig, self.dest)

        # 사전의 번역대상인 orig의 단어들은 최종 docs에 있으면 안된다.
        df = pd.DataFrame(kt.dict)
        orig_keywords = list(df[self.orig])
        df = json_normalize(d.docs, 'keywords').rename(columns={0:'keyword'})
        unq_keywords = list(df.keyword.unique())
        for keyword in orig_keywords:
            self.assertNotIn(keyword, unq_keywords)
        dbg.print_docs(d)

@unittest.skip("showing class skipping")
class KeywordCleanerTestCase(unittest.TestCase):

    filepath = f"{DATA_PATH}/KeywordRemover.txt"

    @unittest.skip("demonstrating skipping")
    def test__load_existed_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordRemover(self.filepath)
        #dbg.print_obj(k)
        self.assertTrue( isinstance(k.keywords, list) )
        print(f"\n k.keywords :\n\n{k.keywords}\n")

    @unittest.skip("demonstrating skipping")
    def test__save_usless_keyword(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCleaner()
        k.save_usless_keyword(keyword='test__keyword')
        text = ifile.open_file(self.filepath)
        print(f"\n text :\n\n{text}\n")
        self.assertRegex(text, 'test__kw')

    #@unittest.skip("demonstrating skipping")
    def test__remove_useless_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        filepath = f"{DATA_PATH}/useless-keywords - Sheet1.csv"
        kc, k, kb = KeywordCleaner(filepath).remove_useless_keywords()

        df = pd.read_csv(filepath)
        useless_keywords = list(df.keyword)

        # Data-Table 조사.
        filter = {'keywords':{'$elemMatch':{'$in':useless_keywords}}}
        projection = {'_id':0,'keywords':1}
        kc.load(filter, projection)
        self.assertTrue(len(kc.docs) is 0)
        ## 오류일때 확인용.
        if len(kc.docs) is not 0: dbg.print_docs(kc)

        # Keyword-Table 조사.
        filter = {'keyword':{'$in':useless_keywords}}
        k.load(filter, {'_id':0,'keyword':1})
        self.assertTrue(len(k.docs) is 0)
        ## 오류일때 확인용.
        if len(k.docs) is not 0: dbg.print_docs(k)

        # KeywordCombination-Table 조사.
        filter = {'combination':{'$elemMatch':{'$in':useless_keywords}}}
        kb.load(filter, {'_id':0,'combination':1})
        self.assertTrue(len(kb.docs) is 0)
        ## 오류일때 확인용.
        if len(kb.docs) is not 0: dbg.print_docs(kb)

    @unittest.skip("demonstrating skipping")
    def test__delete_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordRemover(self.filepath)
        #dbg.print_obj(k)
        k.delete_keywords()
        dbg.print_DeleteResult(k.DeleteResult)

    @unittest.skip("demonstrating skipping")
    def test__save_and_delete_keywords(self):
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

    @unittest.skip("demonstrating skipping")
    def test__remove_keywords_of_target(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordRemover()
        id = ObjectId('5c65eb72b46a3a106c44311f')
        keyword = '사전'
        k.remove_keywords_of_target(id, keyword)

        d = models.Data()
        d.load({'_id':id})
        d.doc = d.docs[0]
        self.assertFalse(keyword in d.doc['keywords'])
        dbg.print_docs(d)

    @unittest.skip("demonstrating skipping")
    def test__merge_longkeyword_into_name(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        filepath = f"{DATA_PATH}/long-keywords - Sheet1.csv"
        kc = KeywordCleaner(filepath).merge_longkeyword_into_name()

        df = pd.read_csv(filepath)
        long_keywords = list(df.keyword)
        filter = {'keywords':{'$elemMatch':{'$in':long_keywords}}}
        projection = {'_id':0,'name':1,'keywords':1}
        kc.load(filter, projection)
        self.assertTrue(len(kc.docs) is 0)
        dbg.print_docs(kc)

    @unittest.skip("demonstrating skipping")
    def test__deduplicate_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordConverter()
        #k.deduplicate_keywords()

        k.load()
        df = k.get_df()
        keywords = list(df.keywords)
        keywords = [k for k in keywords if len(k) is not 0]
        pp.pprint(keywords)

#============================================================
# Data의 keywords를 분석.
#============================================================

@unittest.skip("showing class skipping")
class KeywordCategorizerTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCategorizer()
        #dbg.print_obj(k)
        self.assertEqual(k.tblname, 'Data')

    #@unittest.skip("demonstrating skipping")
    def test__findset_category_from_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        kc = KeywordCategorizer()
        kc.load(None, {'_id':1,'keywords':1,'category':1})
        kc.findset_category_from_keywords()

        if True:
            kc.load({'category':None})
            dbg.print_docs(kc)
            self.assertEqual(len(kc.docs), 0)
        else:# 땜질 수직업.
            kc.load({'keywords':{'$elemMatch':{'$in':['학습사이트']}}})
            for d in kc.docs:
                d['keywords'].append('Tech')
            kc.iter_updating_docs(by='_id')

    @unittest.skip("demonstrating skipping")
    def test__clean(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        filter = {'dtype':'bookmark'}
        projection = {'_id':0, 'keywords':1, 'category':1}
        k = KeywordCategorizer().load(filter, projection)
        df = k.clean(k.get_df())

        dbg.print_df(df)
        self.assertEqual(set(list(df.columns)), set(['keyword','category']))

    @unittest.skip("demonstrating skipping")
    def test__get_category_keywords(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        kc = KeywordCategorizer()
        kc.load({'catgory':None},{'_id':0,'keywords':1,'name':1})
        dbg.print_docs(kc)


    @unittest.skip("demonstrating skipping")
    def test__change_category_of_keyword(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCategorizer()
        keyword = '^사전$'
        category = 'Lang'
        filter = {'keywords':{'$elemMatch':{'$regex':keyword}}}
        update = {'$set':{'category':category}}
        k.update_many(filter, update, False)

        dbg.print_UpdateResult(k.UpdateResult)
        k.load(filter)
        dbg.print_docs(k)

    @unittest.skip("demonstrating skipping")
    def test__save_category_per_keyword_to_xls(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        ks = KeywordCategorizer()
        ks.save_category_per_keyword_to_xls()

        dbg.print_df(ks.get_df().sort_values(['category','keyword']))

@unittest.skip("showing class skipping")
class KeywordFrequencyTestCase(unittest.TestCase):

    filter = {'dtype':'bookmark'}
    projection = {'_id':0, 'keywords':1, 'category':1}

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordFrequency()

        #dbg.print_obj(k)
        self.assertEqual(k.tblname, 'Keyword')

    @unittest.skip("demonstrating skipping")
    def test__load_data(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordFrequency().load_data(self.filter, self.projection)

        df = k.get_df()
        self.assertEqual(set(list(df.columns)), set(['keywords','category']))

    @unittest.skip("demonstrating skipping")
    def test__deduplicate(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordFrequency().deduplicate()

        dbg.print_docs(k)

    @unittest.skip("demonstrating skipping")
    def test__calc_frequency(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordFrequency().load_data(self.filter, self.projection)
        k.calc_frequency()

        dbg.print_docs(k)
        df = k.get_df()
        #dbg.print_df(df)
        self.assertEqual(set(list(df.columns)), set(['keyword','freq']))

    @unittest.skip("demonstrating skipping")
    def test__process(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordFrequency().load_data(self.filter, self.projection)
        k.drop()
        k.calc_frequency().update_docs(upsert=True)

        df = k.load(projection = {'_id':0, 'keyword':1,'freq':1}).get_df()
        dbg.print_df(df.sort_values('freq'))
        self.assertEqual(set(list(df.columns)), set(['keyword','freq']))

    #@unittest.expectedFailure
    #@unittest.skip("demonstrating skipping")
    def test__process_about_all_categories(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordFrequency()
        k.process_about_all_categories()

        df = k.load(projection={'_id':0,'category':1}).get_df()
        categories = KeywordCategorizer([None]).categories
        #categories.remove('Asset')
        self.assertEqual(set(categories), set(list(df.category.unique())))

@unittest.skip("showing class skipping")
class KeywordCombinationStrengthTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength()

        #dbg.print_obj(k)
        self.assertEqual(k.tblname, 'KeywordCombination')

    @unittest.skip("demonstrating skipping")
    # 키워드 조합을 만들기 위한 재료는 Data 테이블의 keywords 컬럼이다.
    def test__load_data(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength().load(None, None)

        dbg.print_docs(k)

    @unittest.skip("demonstrating skipping")
    def test__make_combinations_col(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength().load_data(None, None)
        k.make_combinations_col()

        dbg.print_docs(k)
        df = k.get_df()
        self.assertEqual(set(list(df.columns)), set(['keywords','combinations']))
        sample_tuples = list(df.combinations)[0]
        print(f"\n sample_tuples : {sample_tuples}\n")
        # 인덱스 값을 랜덤넘버로 바꿔라.
        self.assertTrue( isinstance(sample_tuples[0], tuple) )

    @unittest.skip("demonstrating skipping")
    def test__get_unq_combinations(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength().load_data(None, None)
        k.make_combinations_col().get_unq_combinations()

        # 인덱스 값을 랜덤넘버로 바꿔라.
        sample_combination = list(k.combinations)[0]
        print(f"\n sample_combination : {sample_combination}\n")
        self.assertTrue( isinstance(sample_combination, tuple) )

    @unittest.skip("demonstrating skipping")
    def test__calc_combination_strengths(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength().load_data(None, None)
        k.make_combinations_col().get_unq_combinations().calc_combination_strengths()

        df = k.get_df()
        dbg.print_df(df)
        self.assertEqual(set(list(df.columns)), set(['combination','strength']))

    @unittest.skip("demonstrating skipping")
    def test__process(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        filter = {'dtype':'bookmark'}
        projection = {'_id':0,'keywords':1,'category':1}
        k = KeywordCombinationStrength().load_data(filter, projection)
        k.docs = add_categoryvalue_to_keywords(k.docs)
        k.process()

        k.load(projection={'_id':0})
        dbg.print_docs(k)
        df = k.get_df()
        #dbg.print_df(df)
        self.assertEqual(set(list(df.columns)), set(['combination','strength']))

    #@unittest.expectedFailure
    #@unittest.skip("demonstrating skipping")
    def test__process_about_all_categories(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        k = KeywordCombinationStrength()
        k.process_about_all_categories()

        df = k.load(projection={'_id':0,'category':1}).get_df()
        categories = KeywordCategorizer([None]).categories
        categories.remove('Asset')
        self.assertEqual(set(categories), set(list(df.category.unique())))

#============================================================
# 모듈 함수 모음.
#============================================================

#@unittest.skip("showing class skipping")
class ModuleFunctionTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__main_process(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        main_process()

    @unittest.skip("demonstrating skipping")
    def test__add_categoryvalue_to_keywords(self):
        print(f"\n{'='*60}\n test_funcname : {inspect.stack()[0][3]}\n")
        docs = [{
            'category': 'UPV',
            'keywords': ['취업(Job-Search)'],
            'name': 'Pràctiques en Empresa per a Informátics a la Xarxa',
            'url': 'https://www.inf.upv.es/int/peix/alumnos/listado_ofertas.php'
        }]

        docs = add_categoryvalue_to_keywords(docs)
        self.assertIn('UPV', docs[0]['keywords'])
        dbg.print_dics(docs)




def main():
    unittest.main()
