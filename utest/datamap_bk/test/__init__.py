import subprocess
import os


if __name__ == "__main__":
    print(f"{'*'*50}\n\n UnitTest Starts. {os.path.abspath(__file__)}\n\n{'*'*50}\n")

    # subprocess.run(f"python -m unittest {PKG_NAME}/test/__init__.py", shell=True, check=True)
    subprocess.run(f"python -m unittest datamap/test/bookmark.py", shell=True, check=True)
