import unittest


from datamap import DATA_PATH
from datamap import dbg


from datamap.bookmark import *



#@unittest.skip("showing class skipping")
class ParserTestCase(unittest.TestCase):

    filepath = f"{DATA_PATH}/Safari-책갈피__2019-02-20.html"
    target_rootfolder = 'bookmark'
    useless_keywords = ['bookmark','즐겨찾기','책갈피 메뉴','읽기 목록']

    @dbg.utestfunc
    #@unittest.skip("demonstrating skipping")
    def test__parse(self):
        b = Bookmark(self.filepath, self.target_rootfolder, self.useless_keywords)
        b.parse()
        dbg.print_docs(b)

    @dbg.utestfunc
    @unittest.skip("demonstrating skipping")
    def test__remove_useless_keywords(self):
        b = Bookmark(self.filepath, self.target_rootfolder, self.useless_keywords)
        b.docs = [{
            'keywords': ['즐겨찾기','Career'],
            'name': 'LinkedIn',
            'url': 'https://www.linkedin.com/mynetwork/'
        }]
        self.drop()
        b.remove_useless_keywords()

        self.assertEqual(b.docs[0]['keywords'], ['Career'])
        dbg.print_docs(b)

    @dbg.utestfunc
    @unittest.skip("demonstrating skipping")
    def test__process(self):
        b = Bookmark(self.filepath, self.target_rootfolder, self.useless_keywords)
        b.process()

        newdocs_len = len(b.docs)
        dbg.print_docs(b)
        dbg.print_UpdateResults(b)
        b.load({'dtype':'bookmark'})
        self.assertEqual(newdocs_len, len(b.docs))


@unittest.skip("test")
class GeneratorTestCase(unittest.TestCase):

    filepath = f"{DATA_PATH}/Safari Bookmarks__2019-10-10.html"

    def setUp(self):
        self.cls = Generator(self.filepath)

    @dbg.utestfunc
    def test00__setUp(self):
        # dbg.clsattrs(cls=self.cls)
        dbg.clsdict(cls=self.cls)

    @dbg.utestfunc
    def test01__handle_filenames(self):
        self.cls.handle_filenames()
        print(self.cls.basehtml)
        print(self.cls.ofilepath)

    @dbg.utestfunc
    def test02__parse(self):
        rv = self.cls.parse()
        print(rv)

    @dbg.utestfunc
    @unittest.skip("test")
    def test__merge_keywords_into_name(self):
        b = Generator(self.filepath)
        b.docs = [{
            'category': 'UPV',
            'keywords': ['취업(Job-Search)', 'UPV'],
            'name': 'Pràctiques en Empresa per a Informátics a la Xarxa',
            'url': 'https://www.inf.upv.es/int/peix/alumnos/listado_ofertas.php'
        }]
        b.merge_keywords_into_name()
        dbg.print_docs(b)
        self.assertEqual(b.docs[0]['name'], 'Pràctiques en Empresa per a Informátics a la Xarxa__[취업(Job-Search), UPV]')

    @dbg.utestfunc
    @unittest.skip("test")
    def test__write_data_into_html(self):
        b = Generator(self.filepath)
        b.docs = [{
            'category': 'UPV',
            'keywords': ['취업(Job-Search)', 'UPV'],
            'name': 'Pràctiques en Empresa per a Informátics a la Xarxa',
            'url': 'https://www.inf.upv.es/int/peix/alumnos/listado_ofertas.php'
        }]
        b.merge_keywords_into_name()
        b.write_data_into_html()
        print(f"\n b.soup.prettify():\n\n{b.soup.prettify()}\n")
        #print(f"\n html :\n\n{b.html}\n")


def main():
    unittest.main()
