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
def handle_keywords(data):
    categories = ['Asset', 'Career', 'Interests', 'Lang', 'PJTS', 'Politiconomy', 'Tech', 'Travel', 'UPV', '수신', '학습']
    no_keywords = ['Favorites','Reading List','Imported']
    df = pd.DataFrame(data)

    df = json_normalize(data, 'keywords', ['name','url']).rename(columns={0:'keyword'})

    for kw in no_keywords:
        TF = df.keyword.str.contains(pat=f"^{kw}")
        df = df[~TF]

    data = []
    for n, g in df.groupby(['name','url']):
        data.append({'name':n[0],
                    'url':n[1],
                    'keywords':g.keyword.array})
    #
    df = pd.DataFrame(data)

    """category setup."""
    def add_category_from_list(keywords):
        for cate in categories:
            p_cat = re.compile(f"[=\s]+{cate}[=\s]+")
            for keyword in keywords:
                if p_cat.search(keyword) is None:
                    pass
                else:
                    return keyword
                    # keyword = p_cat.sub(repl=f"{cate}", string=keyword)

    df['category'] = df.keywords.apply(add_category_from_list)

    """category cleansing."""
    def clean_category_in_list(keywords):
        p = re.compile(f"([_=\s]+)([a-zA-Z가-힝]+)([_=\s]+)")
        return [k if p.search(k) is None else p.search(k).group(2) for k in keywords]

    df.keywords = df.keywords.apply(clean_category_in_list)

    df.keywords = df.keywords.apply(lambda x: sorted(set(x)))
    return df


@dbg.printfuncinit
def merge_keywords_from_name(df):
    pat = r'__\[(.+)\]'
    _df = df.name.str.extract(pat).rename(columns={0:'keywords1'})
    _df.keywords1 = _df.keywords1.apply(lambda x: x.split(',') if isinstance(x,str) else [])
    _df.keywords1 = _df.keywords1.apply(lambda x: [e.strip() for e in x])
    df = df.join(_df, on=None, how='left')
    df.keywords += df.keywords1
    df.pop('keywords1')
    df.keywords = df.keywords.apply(lambda x: sorted(set(x)))

    df.name = df.name.str.replace(pat, "")
    return df


@dbg.printfuncinit
def rename_category(df):
    def f(keywords):
        p = re.compile('^society$', flags=re.I)
        return [k if p.search(k) is None else p.sub('Politiconomy', k) for k in keywords]

    df.keywords = df.keywords.apply(f)
    df.keywords = df.keywords.apply(lambda x: sorted(set(x)))
    return df


@dbg.printfuncinit
def merge_name_and_keywords(df):
    df.name += df.keywords.apply(lambda x: f"__[{','.join(x)}]")
    df.pop('keywords')
    return df


@dbg.printfuncinit
def run(bmfpath='/Users/sambong/pjts/datamap/data/Safari Bookmarks.html'):
    with open(bmfpath, 'r') as f:
        bookmark = f.read()
        f.close()
    html = convert_bookmarkstyle_to_html(bookmark)
    s = BeautifulSoup(html, 'html.parser')
    data = parse_html(s)
    df = handle_keywords(data)
    df = merge_keywords_from_name(df)
    df = rename_category(df)
    df = merge_name_and_keywords(df)
    return df
