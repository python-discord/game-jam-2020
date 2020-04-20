import shutil
import os

BASE = os.path.dirname(os.path.abspath(__file__))
files = os.listdir(BASE)

for file in filter(lambda filename: not filename.endswith(".py"), files):
    before = file
    after = file.replace("knight iso ", "")
    after = after.replace("char_idle", "idle")
    after = after.replace("char_run ", "run_")
    after = after.replace("char_slice ", "slice_")
    print(f'"{before}" -> "{after}"')
    shutil.move(before, after)