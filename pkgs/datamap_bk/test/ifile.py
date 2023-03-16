
from datamap import *

from datamap.ifile import *

import unittest


#@unittest.skip("showing class skipping")
class ModuleFuncsTestCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_open_file(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        filepath = "/Users/sambong/pjts/Packaging Python Projects.txt"
        text = open_file(filepath)
        print(f"\n text :\n\n{text}\n")
        self.assertTrue(len(text) is not 0)
        self.assertTrue( isinstance(text, str) )

    @unittest.skip("demonstrating skipping")
    def test_write_file(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        filepath = f"{DATA_PATH}/test_write_file.txt"
        text = "['때','Full']"
        write_file(filepath, text)
        text = open_file(filepath)
        print(f"\n text :\n\n{text}\n")
        self.assertTrue(len(text) is not 0)
        self.assertTrue( isinstance(text, str) )

    #@unittest.skip("demonstrating skipping")
    def test_update_file(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        filepath = f"{DATA_PATH}/test_write_file.txt"
        new_text = "['Tv']"
        update_file(filepath, new_text)
        text = open_file(filepath)
        print(f"\n text :\n\n{text}\n")
        self.assertRegex(text, new_text)






def main():
    unittest.main()
