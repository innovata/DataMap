# ============================================================ Python.
import json
import os
import sys
# ============================================================ External-Library.
import pandas as pd
# ============================================================ My-Library.
# ============================================================ Project.
from datamap import models, keywords
# ============================================================ Constant.


def produce_nodes(keywords, category):
    k = models.Keyword()
    filter = {'keyword':{'$in':keywords}, 'category':category}
    #if category is not None: filter.update({'category':category})
    projection={'_id':0, 'keyword':1, 'freq':1}
    k.load(filter, projection)
    if len(k.docs) is not 0:
        df = k.get_df()
        # d3.js 전용 컬럼명으로 변경.
        df = df.rename(columns={'keyword':'id', 'freq':'group'})
        df = df.sort_values('id')
        df.to_csv()


def get_links(category):
    kc = models.KeywordCombination()
    filter = {'category':category}
    projection={'_id':0, 'combination':1, 'strength':1}
    kc.load(filter, projection)
    if len(kc.docs) is not 0:
        # d3.js 전용 자료구조에 맞게 변경.
        df = get_df()
        df['source'] = df.combination.apply(lambda x: x[0])
        df['target'] = df.combination.apply(lambda x: x[1])
        del(df['combination'])
        # d3.js 전용 컬럼명으로 변경.
        df = df.rename(columns={'strength':'value'})


def get_unqkeywords_in_combination(category):
    filter = {'category':category}
    projection={'_id':0, 'combination':1}
    # distinct() 함수로 바꿀 것.
    df = load(filter, projection).get_df()
    combinations = list(df.combination)
    keywords = []
    for combination in combinations:
        for c in combination:
            keywords.append(c)
    return list(set(keywords))


def get_mapdata(category=None):
    links = get_links(category)
    keywords = get_unqkeywords_in_combination(category)
    nodes = get_nodes(keywords, category)
    return json.dumps({'nodes': nodes, 'links': links})


def apply_useless_keyword(keyword, saved_filepath=None):
    """키워드 삭제 적용 전, 유저에게 최종 확인 팝업 필요
    자동 갱신 필요"""
