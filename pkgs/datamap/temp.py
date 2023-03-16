"""
Temporary Packages Loader.
"""
print(f"{'@'*50} {__name__}")

import os
import sys

for p in ['idebug','ipymongo','imatplotlib','itensorflow','iipython','inlp','iwiki','ipdf']:
    sys.path.append(f"{os.environ['HOME']}/pjts/{p}")
