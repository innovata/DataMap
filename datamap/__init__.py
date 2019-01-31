
PJT_NAME = 'datamap'
import os
ROOT_PATH = os.environ['PJTS_PATH']
PJT_PATH = f"{ROOT_PATH}/{PJT_NAME}"
PKG_PATH = f"{ROOT_PATH}/{PJT_NAME}/{PJT_NAME}"
DATA_PATH = f"{ROOT_PATH}/{PJT_NAME}/data"
LIB_PATH = f"{ROOT_PATH}/ilibs"

import sys
sys.path.append(LIB_PATH)
import idbg as dbg

import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
from datetime import datetime
from pymongo import MongoClient
db = MongoClient()[PJT_NAME]
import pandas as pd



from . import models
from . import sources
from . import tests
