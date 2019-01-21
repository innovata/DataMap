"""
데이터맵에서 제공할 대상목록
- 책갈피 [bookmark]
- pdf이북 [pdf]
- 온라인강좌 [course]
- YouTube playlist
- 로컬 파일들 [localfile]
"""

"""패키지 전역 라이브러리"""

PJT_NAME = 'datamap'
DB_v1 = '데이터맵'
# root path
ROOT_PATH = '/Users/sambong/pjts'
# project level path
PJT_PATH = f"{ROOT_PATH}/{PJT_NAME}"
LIB_PATH = f"{ROOT_PATH}/lib"
PKG_PATH = f"{PJT_PATH}/{PJT_NAME}"
DATA_PATH = f"{PJT_PATH}/data"

import sys
sys.path.append(LIB_PATH)
import __debug as dbg

import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
from datetime import datetime
from pymongo import MongoClient
db = MongoClient()[PJT_NAME]
import pandas as pd


from datamap import pdf
from datamap import bookmark
