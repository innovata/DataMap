"""
모든 폴더명은 키워드다. 쓸모없는 키워드는 나중에 리스트에서 제거한다.
사파리든, 크롬이든, 북마크의 태그 구조는 동일하다.
"""
# ============================================================ Python.
import os
import re
from datetime import datetime
# ============================================================ External-Library.
from bs4 import BeautifulSoup
import pandas as pd
from pandas.io.json import json_normalize
# ============================================================ My-Library.
from iipython import ifile
import idebug as dbg
# ============================================================ Project.
from datamap import models
# ============================================================ Constant.



@dbg.printfuncinit
def assign_keywordtags_to_atag_text(soup):
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
        keywords = sorted(sorted(set(keywords)))
        if len(keywords) is not 0:
            a.string = f"{li[0]}__[{','.join(keywords)}]".lstrip().rstrip()
    return soup


@dbg.printfuncinit
def rearrange_atag_location(soup):
    p = re.compile('__\[')
    for a in soup.find_all('a'):
        li = p.split(string=a.string)
        dataname = li[0]
        if len(li) is 2:
            keywords = li[1].replace(']','').split(',')
            keywords = [e.lstrip().rstrip() for e in keywords]
        else:
            keywords = []


@dbg.printfuncinit
def convert_atags_to_df(soup):
    atags = soup.find_all('a')
    for a in atags:
        li = a.string.split('__[')
        name = li[0]
        if len(li) < 2:
            keywords = []
        else:
            keywords = li[1].replace(']','').split(',')
        docs.append({'name':name, 'url':a['href'], 'keywords':keywords})
    return get_df()


@dbg.printfuncinit
def get_uniq_keywords(df):
    keywords_li = list(df.keywords)
    li = []
    for keywords in keywords_li:
        li += keywords
    return sorted(sorted(set(li)))


@dbg.printfuncinit
def deduplicate_atags_by_url(df):
    dics = []
    for n, g in df.groupby(['url']):
        dic = {'url':n, 'name':''}
        dupls = g.to_dict('records')
        keywords = []
        for dupl in dupls:
            if len(dupl['name']) > len(dic['name']):
                dic['name'] = dupl['name']
            keywords += dupl['keywords']
        dic['keywords'] = sorted(sorted(set(keywords)))
        dics.append(dic.copy())
    return pd.DataFrame(dics)


@dbg.printfuncinit
def save_soup_as_bookmark(soup, bmfpath=None):
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
    if bmfpath is None:
        bmfpath = savebmfpath
    with open(file=bmfpath, mode='w') as f:
        f.write(html)
        f.close()


@dbg.printfuncinit
def remove_useless_keywords():

    def remove(li):
        for e in li:
            if e in useless_keywords:
                li.remove(e)
        return li

    if len(useless_keywords) is not 0:
        df = get_df()
        df.keywords = df.keywords.apply(remove)
    return df


@dbg.printfuncinit
def replace_keywords(df):
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


@dbg.printfuncinit
def produce_subcategory_tags(soup):
    for category in categories:
        cate_p = soup.find('h3',string=category).find_next_sibling(name='p')
        subcate = soup.new_tag('h3',folded="")
        subcate.string = f"__{category}__"
        cate_p.a.insert_before(subcate)
        subcate_p = soup.new_tag('p')
        cate_p.h3.insert_after(subcate_p)
    return soup


@dbg.printfuncinit
def rewrite_atag_text_having_category(soup, df):
    """서브카테고리 폴더 밑에 new_a_tag를 생성해서 추가."""
    for a in soup.find_all('a'):
        a.decompose()
    for category in categories:
        TF = df.keywords.apply(lambda x: True if category in x else False)
        df1 = df[TF]
        dics = df1.to_dict('records')
        for d in dics:
            atag = soup.new_tag('a',href=d['url'])
            atag.string = f"{d['name']}__[{', '.join(d['keywords'])}]"
            #print(soup.find('h3',string=f"__{category}__").find_next_sibling(name='p').prettify())
            soup.find('h3',string=f"__{category}__").find_next_sibling(name='p').append(atag)
    return soup


@dbg.printfuncinit
def some_keywords_cannot_coexist(df):
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


@dbg.printfuncinit
def rewrite_atag_text_without_category(soup, df):
    def exists_category_in_keywords(li):
        for e in li:
            if e in categories:
                return True

    df['TF'] = df.keywords.apply(exists_category_in_keywords)
    df1 = df[df.TF.isna()]
    dics = df1.to_dict('records')
    for d in dics:
        atag = soup.new_tag('a',href=d['url'])
        atag.string = f"{d['name']}__[{', '.join(d['keywords'])}]"
        soup.find('h3',string=f"수신(修身)").find_next_sibling(name='p').append(atag)
    return soup


@dbg.printfuncinit
def check_url_duplicated(df):
    df = get_df()
    for n, g in df.groupby('url'):
        if len(g) > 1:
            print(f"{'-'*60}\n{g}")


@dbg.printfuncinit
def save():
    html = ifile.open_file(savebmfpath)
    html = convert_bookmarkstyle_to_html(html)
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    p = re.compile('__\[')
    for a in soup.find_all('a'):
        li = p.split(string=a.string)
        name = li[0]
        url = a['href']
        if len(li) > 1:
            keywords = li[1].replace(']','').split(',')
            keywords = [e.lstrip().rstrip() for e in keywords]
        else:
            keywords = []

        for category in categories:
            if category in keywords:
                category = category
        update_doc({'url':url}, True)


@dbg.printfuncinit
def run_v1(bmfpath):
    html = ifile.open_file(bmfpath)
    html = convert_bookmarkstyle_to_html(html)
    soup = BeautifulSoup(html, 'html.parser')
    soup = assign_keywordtags_to_atag_text(soup)
    df = convert_atags_to_df(soup)
    df = deduplicate_atags_by_url(df)
    df = replace_keywords(df)
    soup = produce_subcategory_tags(soup)
    df = some_keywords_cannot_coexist(df)
    soup = rewrite_atag_text_having_category(soup, df)
    soup = rewrite_atag_text_without_category(soup, df)
    save_soup_as_bookmark(soup)
    return soup


class Parser:

    def __init__(self, bmfpath):
        super().__init__()
        self.bmfpath = bmfpath
        filename = os.path.basename(bmfpath)
        root, ext = os.path.splitext(filename)
        self.savebmfpath = f"{DATA_PATH}/{root}_new{ext}"
        # self.useless_keywords = useless_keywords
        # self.categories = CATES
        self.dtype = 'bookmark'

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

    def run(self):
        # read bookmark
        html = ifile.open_file(self.bmfpath)

        # parse
        html = convert_bookmarkstyle_to_html(html)
        soup = BeautifulSoup(html, 'html.parser')
        soup = assign_keywordtags_to_atag_text(soup)
        df = convert_atags_to_df(soup)
        df = deduplicate_atags_by_url(df)
        df = replace_keywords(df)
        soup = produce_subcategory_tags(soup)
        df = some_keywords_cannot_coexist(df)
        soup = rewrite_atag_text_having_category(soup, df)
        soup = rewrite_atag_text_without_category(soup, df)


        save_soup_as_bookmark(soup)
        return soup

    def save_soup_as_bookmark(self, soup, bmfpath=None):
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
        if bmfpath is None:
            bmfpath = self.savebmfpath
        with open(file=bmfpath, mode='w') as f:
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

    def save(self):
        html = ifile.open_file(self.savebmfpath)
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


class Generator(models.Data):
    """사파리에서 사용할 북마크파일을 생성한다.
    카테고리 폴더는 만들지 않는다. 즐겨찾기와 동일한 레벨의 'Repository' 폴더에 모든 데이터를 삽입한다.
    각 데이터에 해당하는 카테고리 값은 별도 모듈/클래스에서 자동으로 할당하도록 개발한다.
    기존 할당된 카테고리 값은 키워드로 삽입해서 브라우저에서 검색가능하도록 한다.
    """

    def __init__(self, bmfpath):
        super().__init__()
        self.bmfpath = bmfpath
        # bmfpath로 들어온 파일을 base.html로 변환한다.
        # 그러나 지금은... 수작업으로 만든 것을 사용한다.
        filter = {'dtype':'bookmark'}
        projection = {'_id':0, 'dtype':0}
        # self.docs = self.load(filter, projection).docs

    def handle_filenames(self):
        file = self.bmfpath.split('__')
        self.basehtml = f"{DATA_PATH}/{file[0]}__base.html"
        self.obmfpath = f"{DATA_PATH}/{file[0]}__transform.html"

    def parse(self):
        p = Parser(bmfpath=self.bmfpath, useless_keywords=[])

    def merge_keywords_into_name(self):
        for d in self.docs:
            dn = keywords.DataNameParser(d['name']).parse()
            d['name'] = f"{dn.title}__[{', '.join(d['keywords'])}]"
        return self

    def make_full_dataname(self):
        for d in self.docs:
            keywords = d['keywords'] + [d['category']]
            keywords_part = f"__[{', '.join(keywords)}]"
            d['name'] += keywords_part
        return self

    def write_data_into_html(self):
        html = ifile.open_file(self.basehtml)
        soup = BeautifulSoup(html, 'html.parser')
        p = soup.new_tag('p')
        soup.h1.insert_after(p)
        for d in self.docs:
            a_tag = soup.new_tag('a', href=d['url'])
            a_tag.append(d['name'])
            p.append(a_tag)
        self.soup = soup
        # 북마크 스타일로 변형.
        s = str(soup).replace('<p>', '\n<dl><p>').replace('</p>', '\n</dl><p>').replace('<a', '\n<dt><a')
        self.html = s
        return self

    def process(self):
        self.handle_filenames()
        self.docs = keywords.add_categoryvalue_to_keywords(self.docs)
        self.merge_keywords_into_name()
        self.write_data_into_html()
        ifile.write_file(self.obmfpath, self.html)
