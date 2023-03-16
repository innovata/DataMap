"""
모든 폴더명은 키워드다. 쓸모없는 키워드는 나중에 리스트에서 제거한다.
사파리든, 크롬이든, 북마크의 태그 구조는 동일하다.
"""
# ============================================================ Python.
import re
import os
# ============================================================ External-Library.
from bs4 import BeautifulSoup
import pandas as pd
from pandas.io.json import json_normalize
# ============================================================ My-Library.
import idebug as dbg
# ============================================================ Project.
from datamap import models
# ============================================================ Constant.
CATEGORIES = ['Asset', 'Career', 'Interests', 'Lang', 'PJTS', 'Politiconomy', 'Tech', 'Travel', 'UPV', '수신', '학습']
USELESS = ['Reading List','Bookmarks Menu']
NO_KEYWORDS = USELESS + ['Favorites','Imported']


@dbg.printfuncinit
def _read_bookmark(bmfpath):
    with open(bmfpath, 'r') as f:
        bookmark = f.read()
        f.close()
    return bookmark


@dbg.printfuncinit
def _convert_bookmark_to_html(html):
    html, number = re.subn(pattern='<DT>|<DL>', repl='', string=html)
    html = html.replace('</DL><p>','</p>')
    return html


@dbg.fruntime
def _parse_html(soup):
    links = soup.find_all('a')
    data = []
    for i, link in enumerate(links, start=1):
        datum = {'name':link.string, 'url':link.get('href'), 'keywords':[]}
        for k, parent in enumerate(link.parents):
            if parent is None:
                pass
            else:
                h3 = parent.find_previous_sibling('h3')
                if h3 is None:
                    pass
                else:
                    datum['keywords'].append(h3.string)
        data.append(datum)
    return data


@dbg.fruntime
def _manipulate_data(data):
    p_cat = re.compile(f"(=+)([a-zA-Z가-힝]+)(=+)")
    p_kw = re.compile('__\[(.*)\]')
    for d in data:
        """Add category and manipulate keywords."""
        for keyword in d['keywords']:
            m = p_cat.search(keyword)
            if m is None:
                pass
            else:
                d['keywords'].remove(keyword)
                d['category'] = m.group(2)

        """Manipulate name."""
        name = d['name']
        m = p_kw.search(name)
        if m is None:
            pass
        else:
            d['name'] = p_kw.sub("", name)
            d['keywords'] += m.group(1).split(',')
        d['keywords'] = [e.strip() for e in d['keywords'] if len(e) is not 0]
        d['keywords'] = sorted(set(d['keywords']))

        """Remove non-keywords from keywords."""
        for k in d['keywords']:
            if k in NO_KEYWORDS:
                d['keywords'].remove(k)

    return data


@dbg.fruntime
def _parse_existed_bookmark(bmfpath):
    bookmark = _read_bookmark(bmfpath)
    html = _convert_bookmark_to_html(bookmark)
    s = BeautifulSoup(html, 'html.parser')
    data = _parse_html(s)
    return _manipulate_data(data)


@dbg.fruntime
def dedup_keywords(tbl):
    cursor = tbl.find(None, {'keywords':1})
    for d in list(cursor):
        d['keywords'] = sorted(set(d['keywords']))
        tbl.update_one(
            {'_id':d['_id']},
            {'$set':{'keywords':d['keywords']}},
            upsert=False
        )


@dbg.fruntime
def rename_keyword(tbl, orgname, dstname):

    UpdateResult = tbl.update_many(
        {'keywords':{'$all':[orgname]}},
        {'$addToSet':{'keywords':dstname}},
        upsert=False,
    )
    dbg.clsattrs(UpdateResult, loose=True)

    UpdateResult = tbl.update_many(
        {'keywords':{'$all':[orgname]}},
        {'$pull':{'keywords':orgname}},
        upsert=False,
    )
    dbg.clsattrs(UpdateResult, loose=True)
    """검증."""
    cursor = tbl.find({'keywords':{'$all':[dstname]}})
    return pd.DataFrame(list(cursor))


@dbg.fruntime
def normalize_keyword_format(tbl):
    cursor = tbl.find(None, {'keywords':1})
    for d in list(cursor):
        d['keywords'] = [e.replace(" ","-") for e in d['keywords']]
        tbl.update_one(
            {'_id':d['_id']},
            {'$set':{'keywords':d['keywords']}},
            upsert=False
        )


@dbg.fruntime
def show_unique_keywords(tbl):
    cursor = tbl.find(None, {'keywords':1})
    df = json_normalize(list(cursor), 'keywords').rename(columns={0:'keyword'})
    return sorted(df.keyword.unique())


@dbg.fruntime
def _merge_keywords_into_name(soup, data):
    for d in data:
        if len(d['keywords']) is 0:
            pass
        else:
            a = soup.find('a', attrs={'href':d['url']})
            if a is None:
                pass
            else:
                a.string = f"{d['name']}__[{','.join(sorted(d['keywords']))}]"
    return soup


@dbg.fruntime
def _write_bookmark_from_soup(soup, bmfpath):
    for e in USELESS:
        h3 = soup.find('h3', string=e)
        if h3 is not None:
            h3.find_next_sibling().decompose()
            h3.decompose()

    html = soup.prettify()
    html, n = re.subn(pattern='\n', repl='', string=html)
    html, n = re.subn(pattern='>\s+', repl='>', string=html)
    html, n = re.subn(pattern='\s+<', repl='<', string=html)
    html, n = re.subn(pattern='<html>', repl='\n<HTML>', string=html)
    html, n = re.subn(pattern='</html>', repl='\n</HTML>', string=html)
    html, n = re.subn(pattern='<meta', repl='\n<META', string=html)
    html, n = re.subn(pattern='<title>', repl='\n<Title>', string=html)
    html, n = re.subn(pattern='<h1>', repl='\n<H1>', string=html)
    html, n = re.subn(pattern='<h3', repl='\n<DT><H3', string=html)
    html, n = re.subn(pattern='<p>', repl='\n<DL><p>', string=html)
    html, n = re.subn(pattern='</p>', repl='\n</DL><p>', string=html)
    html, n = re.subn(pattern='<a', repl='\n<DT><A', string=html)
    html, n = re.subn(pattern='</a>', repl='</A>', string=html)

    path = os.path.dirname(bmfpath)
    file = os.path.basename(bmfpath)
    fs = list(os.path.splitext(file))
    bmfpath = f"{path}/{fs[0]}_New{fs[1]}"
    with open(file=bmfpath, mode='w') as f:
        f.write(html)
        f.close()


@dbg.fruntime
def create_new_bookmark(bmfpath, tbl):
    bookmark = _read_bookmark(bmfpath)
    html = _convert_bookmark_to_html(bookmark)
    soup = BeautifulSoup(html, 'html.parser')

    data = list(tbl.find())
    soup = _merge_keywords_into_name(soup, data)
    _write_bookmark_from_soup(soup, bmfpath)


class Bookmark(models.Bookmark):

    def __init__(self, bmfpath=None):
        super().__init__()
        if bmfpath is None:
            self.bmfpath = '/Users/sambong/pjts/datamap/data/Safari Bookmarks.html'
        else:
            self.bmfpath = bmfpath

    def alldocs(self):
        return pd.DataFrame(list(self.tbl.find()))

    @dbg.fruntime
    def parser(self):
        data = _parse_existed_bookmark(self.bmfpath)
        for d in data:
            self.tbl.update_one(
                {e:d[e] for e in self.id_cols},
                {'$set':{e:d[e] for e in self.schema if e in d}},
                upsert=True)

        return self.alldocs()

    @dbg.fruntime
    def creator(self):
        create_new_bookmark(self.bmfpath, self.tbl)
        return self.alldocs()
