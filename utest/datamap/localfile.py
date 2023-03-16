print(f"{'@'*50} {__name__}")
# ============================================================ Python.
import os
# ============================================================ External-Library.
# ============================================================ My-Library.
# from iipython import ifile
# ============================================================ Project.
# ============================================================ Constant.




def remove_dash_from_fname(path, topdown=True):
    for root, dirs, files in os.walk(top=path, topdown=topdown):
        for i, file in enumerate(files, start=1):
            print(f"\n{'-'*50} i:{i}")
            fn, ext = os.path.splitext(file)
            if ext == '.pdf':
                print(f"{root}/{file}")
                fn = fn.replace('-', ' ')
                print(f"{root}/{fn}{ext}")
                os.rename(f"{root}/{file}", f"{root}/{fn}{ext}")
                # break
        # break

def remove_dash_from_dirname(path, topdown=True):
    for root, dirs, files in os.walk(top=path, topdown=topdown):
        for i, dir in enumerate(dirs, start=1):
            print(f"\n{'-'*50} i:{i}")
            # fn, ext = os.path.splitext(file)
            print(f"{root}/{dir}")
            _dir = dir.replace('-', ' ')
            print(f"{root}/{_dir}")
            os.rename(f"{root}/{dir}", f"{root}/{_dir}")
            break
        break
