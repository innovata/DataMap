"""
파싱 :
- 정상 pdf파일(문자열로 인식가능한)의 목차를 읽어서 대상내용 컬럼에 저장.
- 비정상 pdf파일(이미지로 인식해야하는) 상동.
#'contents':__fitz.read_official_pdf(folder_path, f, list(range(20))),
"""
from datamap import *
from .models import Datum
import os


def collect(path):
    # path가 폴더경로이면 폴더 하위 모든 폴더 및 파일에 대해 파일경로를 리스트로 생성
    if os.path.isdir(path):
        pdfs = []
        for root, dirs, files in os.walk(top=path, topdown=True):
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == ".pdf":
                    pdfs.append((root, file))
        pdfs = sorted(pdfs)
    # path가 파일경로이면 길이 1 인 리스트 생성.
    else:
        pdfs = [path]

    # 리스트를 반복하며 파일 하나씩 작업.
    d = Data()
    for pdf in pdfs:
        # 정식 pdf 파일의 목차 부분까지 읽어들인다.
        d.stack(name=pdf[1], url=os.path.join(pdf[0],pdf[1]), keywords=[])

    #__저장
    d.insert_many(data)
