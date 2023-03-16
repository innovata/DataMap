
import os
import sys
PJTS_PATH = '/Users/sambong/pjts'
DATA_PATH = f"{PJTS_PATH}/datamap/data"
sys.path.append(f"{PJTS_PATH}/libs/ilib")
import ilib
sys.path.append(f"{PJTS_PATH}/libs/idebug")
import idebug as dbg
sys.path.append(f"{PJTS_PATH}/libs/imath")
#sys.path.append(f"{PJTS_PATH}/libs/i-nlp")
sys.path.append(f"{PJTS_PATH}/libs/iwiki")
sys.path.append(f"{PJTS_PATH}/libs/ipdf")
sys.path.append(f"{PJTS_PATH}/datamap/env/lib/python3.7/site-packages")
sys.path.append(f"{PJTS_PATH}/datamap")


from datamap import models
from datamap import ifile
from bs4 import BeautifulSoup
import re
import pandas as pd
import copy



def mark_dtype(clss, dtype):
    df = clss.get_df()
    df = df.assign(dtype= dtype)
    clss.docs = df.to_dict('records')
    return clss

class Bookmark(models.Data):
    """모든 폴더명은 키워드다. 쓸모없는 키워드는 나중에 리스트에서 제거한다.
    사파리든, 크롬이든, 북마크의 태그 구조는 동일하다.
    """
    def __init__(self, filepath, useless_keywords):
        super().__init__()
        self.filepath = filepath
        filename = os.path.basename(filepath)
        root, ext = os.path.splitext(filename)
        self.savefilepath = f"{DATA_PATH}/{root}_new{ext}"
        self.useless_keywords = useless_keywords
        self.categories = ['Interests','Asset','Lang','Tech','Society','Career','UPV']
        self.dtype = 'bookmark'

    def save(self):
        html = ifile.open_file(self.savefilepath)
        html = self.convert_bookmarkstyle_to_html(html)
        soup = BeautifulSoup(html, 'html.parser')
        #print(soup.prettify())
        p = re.compile('__\[')
        for a in soup.find_all('a'):
            li = p.split(string=a.string)
            self.name = li[0]
            self.url = a['href']
            if len(li) > 1:
                keywords = li[1].replace(']','').split(',')
                self.keywords = [e.lstrip().rstrip() for e in keywords]
            else:
                self.keywords = []

            for category in self.categories:
                if category in self.keywords:
                    self.category = category
            self.update_doc({'url':self.url}, True)

    def convert_bookmarkstyle_to_html(self, html):
        html, number = re.subn(pattern='<DT>|<DL>', repl='', string=html)
        html = html.replace('</DL><p>','</p>')
        return html

    def assign_keywordtags_to_atag_text(self, soup):
        p = re.compile(pattern='__\[')
        for a in soup.find_all('a'):
            li = p.split(string=a.string)
            if len(li) is 2:
                keywords = li[1].replace(']','').split(',')
                keywords = [e.lstrip().rstrip() for e in keywords]
            else:
                keywords = []

            for parent in a.parents:
                if parent is None:
                    print("parent is None")
                else:
                    if parent.name == 'p':
                        h3 = parent.find_previous_sibling('h3')
                        if h3 is None:
                            print("h3 is None")
                        else:
                            if h3.get_text() not in ['즐겨찾기','책갈피 메뉴','읽기 목록']:
                                keywords.append(h3.get_text())
            keywords = sorted(list(set(keywords)))
            if len(keywords) is not 0:
                a.string = f"{li[0]}__[{','.join(keywords)}]".lstrip().rstrip()
        return soup

    def rearrange_atag_location(self, soup):
        p = re.compile('__\[')
        for a in soup.find_all('a'):
            li = p.split(string=a.string)
            dataname = li[0]
            if len(li) is 2:
                keywords = li[1].replace(']','').split(',')
                keywords = [e.lstrip().rstrip() for e in keywords]
            else:
                keywords = []

    def convert_atags_to_df(self, soup):
        atags = soup.find_all('a')
        for a in atags:
            li = a.string.split('__[')
            name = li[0]
            if len(li) < 2:
                keywords = []
            else:
                keywords = li[1].replace(']','').split(',')
            self.docs.append({'name':name, 'url':a['href'], 'keywords':keywords})
        return self.get_df()

    def get_uniq_keywords(self, df):
        keywords_li = list(df.keywords)
        li = []
        for keywords in keywords_li:
            li += keywords
        return sorted(list(set(li)))

    def deduplicate_atags_by_url(self, df):
        dics = []
        for n, g in df.groupby(['url']):
            dic = {'url':n, 'name':''}
            dupls = g.to_dict('records')
            keywords = []
            for dupl in dupls:
                if len(dupl['name']) > len(dic['name']):
                    dic['name'] = dupl['name']
                keywords += dupl['keywords']
            dic['keywords'] = sorted(list(set(keywords)))
            dics.append(dic.copy())
        return pd.DataFrame(dics)

    def refine_upon_bookmark(self):
        html = ifile.open_file(self.filepath)
        html = self.convert_bookmarkstyle_to_html(html)
        soup = BeautifulSoup(html, 'html.parser')
        soup = self.assign_keywordtags_to_atag_text(soup)
        df = self.convert_atags_to_df(soup)
        df = self.deduplicate_atags_by_url(df)
        df = self.replace_keywords(df)
        soup = self.produce_subcategory_tags(soup)
        df = self.some_keywords_cannot_coexist(df)
        soup = self.rewrite_atag_text_having_category(soup, df)
        soup = self.rewrite_atag_text_without_category(soup, df)
        self.save_soup_as_bookmark(soup)
        return soup

    def save_soup_as_bookmark(self, soup, filepath=None):
        h3 = soup.find(name='h3',string='책갈피 메뉴')
        h3.find_next_sibling().decompose()
        h3.decompose()
        h3 = soup.find(name='h3',string='읽기 목록')
        h3.find_next_sibling().decompose()
        h3.decompose()

        html = soup.prettify()
        html, number = re.subn(pattern='\n', repl='', string=html)
        html, number = re.subn(pattern='>\s+', repl='>', string=html)
        html, number = re.subn(pattern='\s+<', repl='<', string=html)
        html, number = re.subn(pattern='<html>', repl='\n<HTML>', string=html)
        html, number = re.subn(pattern='</html>', repl='\n</HTML>', string=html)
        html, number = re.subn(pattern='<meta', repl='\n<META', string=html)
        html, number = re.subn(pattern='<title>', repl='\n<Title>', string=html)
        html, number = re.subn(pattern='<h1>', repl='\n<H1>', string=html)
        html, number = re.subn(pattern='<h3', repl='\n<DT><H3', string=html)
        html, number = re.subn(pattern='<p>', repl='\n<DL><p>', string=html)
        html, number = re.subn(pattern='</p>', repl='\n</DL><p>', string=html)
        html, number = re.subn(pattern='<a', repl='\n<DT><A', string=html)
        html, number = re.subn(pattern='</a>', repl='</A>', string=html)
        if filepath is None:
            filepath = self.savefilepath
        with open(file=filepath, mode='w') as f:
            f.write(html)
            f.close()

    def remove_useless_keywords(self):

        def remove(li):
            for e in li:
                if e in self.useless_keywords:
                    li.remove(e)
            return li

        if len(self.useless_keywords) is not 0:
            df = self.get_df()
            df.keywords = df.keywords.apply(remove)
        return self

    def replace_keywords(self, df):
        def replace_element(li, before, after):
            if before in li:
                li.remove(before)
                li.append(after)
            return li

        def redefine_keyword(li):
            li = replace_element(li,'R','_R_')
            li = replace_element(li,'Mac','macOS')
            li = replace_element(li,'call_python','connector')
            li = replace_element(li,'connect_to_MongoDB','connector')
            li = replace_element(li,'d3.js','D3.js')
            li = replace_element(li,'도올','도올 김용옥')
            li = replace_element(li,'MIT','MIT OpenCourseWare')
            li = replace_element(li,'MIT','Big-data Big data')
            li = replace_element(li,'AI','Artificial Intelligence')
            return li

        df.keywords = df.keywords.apply(redefine_keyword)
        return df

    def produce_subcategory_tags(self, soup):
        for category in self.categories:
            cate_p = soup.find('h3',string=category).find_next_sibling(name='p')
            subcate = soup.new_tag('h3',folded="")
            subcate.string = f"__{category}__"
            cate_p.a.insert_before(subcate)
            subcate_p = soup.new_tag('p')
            cate_p.h3.insert_after(subcate_p)
        return soup

    def rewrite_atag_text_having_category(self, soup, df):
        """서브카테고리 폴더 밑에 new_a_tag를 생성해서 추가."""
        for a in soup.find_all('a'):
            a.decompose()
        for category in self.categories:
            TF = df.keywords.apply(lambda x: True if category in x else False)
            df1 = df[TF]
            dics = df1.to_dict('records')
            for d in dics:
                atag = soup.new_tag('a',href=d['url'])
                atag.string = f"{d['name']}__[{', '.join(d['keywords'])}]"
                #print(soup.find('h3',string=f"__{category}__").find_next_sibling(name='p').prettify())
                soup.find('h3',string=f"__{category}__").find_next_sibling(name='p').append(atag)
        return soup

    def some_keywords_cannot_coexist(self, df):
        def rule(li):
            """Lang와 Interests 는 양립할 수 없다."""
            if ('Lang' in li) and ('Interests' in li):
                li.remove('Interests')
            if ('사전' in li) and ('Interests' in li):
                li.remove('Interests')
                li.append('Lang')
            if ('실시간방송' in li) and ('Interests' in li):
                li.remove('Interests')
                li.append('Lang')
            if ('Tech' in li) and ('Interests' in li):
                li.remove('Interests')
            if ('UPV' in li) and ('Lang' in li):
                li.remove('Lang')
            if ('Career' in li) and ('Tech' in li):
                li.remove('Tech')
            return li

        df.keywords = df.keywords.apply(rule)
        return df

    def rewrite_atag_text_without_category(self, soup, df):
        def exists_category_in_keywords(li):
            for e in li:
                if e in self.categories:
                    return True

        df['TF'] = df.keywords.apply(exists_category_in_keywords)
        df1 = df[df.TF.isna()]
        dics = df1.to_dict('records')
        for d in dics:
            atag = soup.new_tag('a',href=d['url'])
            atag.string = f"{d['name']}__[{', '.join(d['keywords'])}]"
            soup.find('h3',string=f"수신(修身)").find_next_sibling(name='p').append(atag)
        return soup

    def check_url_duplicated(self, df):
        df = self.get_df()
        for n, g in df.groupby('url'):
            if len(g) > 1:
                print(f"{'-'*60}\n{g}")

def refine_upon_bookmark():
    b = Bookmark(f"{DATA_PATH}/Safari-책갈피__2019-03-30.html",['bookmark','즐겨찾기','책갈피 메뉴','읽기 목록'])
    b.refine_upon_bookmark()
refine_upon_bookmark()

self = Bookmark(f"{DATA_PATH}/Safari-책갈피__2019-03-30.html",['bookmark','즐겨찾기','책갈피 메뉴','읽기 목록'])
self.save()
#dbg.obj(self)

df



class Localfile(models.Data):
    """
    - 정상 pdf파일(문자열로 인식가능한)의 목차를 읽어서 대상내용 컬럼에 저장.
    - 비정상 pdf파일(이미지로 인식해야하는) 상동.
    """
    def __init__(self, path, ftypes=[]):
        super().__init__()
        self.path = path
        self.define_useful_ftypes(ftypes)

    def process(self):
        filepaths = ifile.get_filepaths(self.path)
        self.filter_useful_filepaths(filepaths)
        self.make_data()
        self = mark_dtype(self, 'localfile')
        #self.insert_docs()

    def define_useful_ftypes(self, ftypes):
        apple_docs = ['.pages', '.numbers', '.key']
        ms_docs = ['.docx', '.xlsx', '.pptx']
        docs = ['.pdf', '.hwp'] + apple_docs + ms_docs
        pics = ['.jpg', '.jpeg', '.png']
        self.ftypes = (docs + pics + ftypes)

    def filter_useful_filepaths(self, filepaths):
        useful_filepaths = []
        for filepath in filepaths:
            root, ext = os.path.splitext(filepath)
            if ext in self.ftypes:
                useful_filepaths.append(filepath)
        self.filepaths = useful_filepaths
        return self

    def make_data(self):
        for filepath in self.filepaths:
            head, tail = os.path.split(filepath)
            self.docs.append({'name':tail, 'url':f"file://{filepath}", 'keywords':[]})
        return self

class Gdrive(models.Data):

    def __init__(self):
        super().__init__()
