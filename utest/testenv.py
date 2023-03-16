"""
Automatic-Setup UnitTest Environment.
"""
print(f"{'*'*50} {__name__}\n{__doc__}")
import os
import sys
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=2)
# ============================================================
print(f"os.curdir : {os.path.abspath(os.curdir)}")
PJT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['PXFILE_PATH'] = f"{os.environ['HOME']}/pjts/proxylist.html"
# ============================================================
for i, k in enumerate(sorted(os.environ), start=1):
    print(f"{'-'*50} {i}/{len(os.environ)}")
    print(f"{k} : {os.environ[k]}")
# ============================================================
for p in ['idebug','ipymongo','imatplotlib','itensorflow','iipython','inlp','iwiki','ipdf']:
    sys.path.append(f"{os.environ['HOME']}/pjts/{p}")
pp.pprint(sorted(set(sys.path)))
