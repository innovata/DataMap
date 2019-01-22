
"""패키지 전역 라이브러리"""

PJT_NAME = 'datamap'
DB_v1 = '데이터맵'
# root path
ROOT_PATH = '/Users/sambong/pjts'
# project level path
PJT_PATH = f"{ROOT_PATH}/{PJT_NAME}"
PKG_PATH = f"{ROOT_PATH}/{PJT_NAME}/{PJT_NAME}"
LIB_PATH = f"{ROOT_PATH}/lib"
DATA_PATH = f"{ROOT_PATH}/{PJT_NAME}/data"

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
from datamap import models
from datamap import tests
