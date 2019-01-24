
import unittest
from datamap import *
from datamap.models import Bookmark, Data


class DataTestCase(unittest.TestCase):

    def test_open_file(self):
        b = Bookmark(filepath="/Users/sambong/pjts/datamap/data/Safari-책갈피__2019-01-20.html")
        b.open_file()
        self.assertFalse(b.text is None)

    def test_get_unique_keywords(self):
        d = Data()
        keywords = d.get_unique_keywords()
        self.assertTrue(isinstance(keywords, list))


class BookmarkTestCase(unittest.TestCase):

    def test_invalid_keywords(self):
        b = Bookmark(filepath="/Users/sambong/pjts/datamap/data/Safari-책갈피__2019-01-20.html")
        b.parse()
        df = pd.DataFrame(b.data)
        keywords_li = list(df.keywords)
        uq_keywords = []
        for keywords in keywords_li:
            uq_keywords += keywords
        uq_keywords = list(set(uq_keywords))
        for e in b.meaningless_keywords:
            self.assertFalse(e in uq_keywords)


def main():
    unittest.main()

if __name__ == "__main__":
    unittest.main()
