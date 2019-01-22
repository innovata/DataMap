
from datamap import *
from .models import Data
from bs4 import BeautifulSoup

class Safari:
    def __init__(self, filepath):
        self.filepath = filepath
        self.sections = ['즐겨찾기','Repository']
        self.meaningless_folders = ['책갈피 메뉴','읽기 목록'] + self.sections
        self.folder_tag = 'h3'

    def collect(self):
        self.parse()
        self.insert_many()

    def parse(self):
        with open(file=self.filepath, mode='r') as f:
            text = f.read()
            f.close()

        d = Data()
        soup = BeautifulSoup(text, 'html.parser')
        for section in self.sections:
            section = soup.find(self.folder_tag, string=section)
            section = section.find_next_sibling('dl')
            links = section.find_all('a')
            for link in links:
                foldernames = []
                dls = link.find_parents('dl')
                for dl in dls:
                    folder_tag = dl.find_previous_sibling(self.folder_tag)
                    if folder_tag is not None:
                        foldernames.append(folder_tag.string)

                # 의미없는 폴더명 제거.
                foldernames = list(set(foldernames))
                for u in self.meaningless_folders:
                    if u in foldernames: foldernames.remove(u)

                d.stack(name=link.string, url=link['href'], keywords=foldernames)
        d.print_data()

    def insert_many(self):
        d.insert_many()

def main():
    s = Safari(filepath="/Users/sambong/pjts/datamap/data/Safari-책갈피__2019-01-20.html")
    s.collect()
