import os
import re

def compileAll(uipath: str):
    files = os.listdir(uipath)
    to_compile = []
    pat = re.compile(r'.*\.ui')
    for f in files:
        if pat.match(f):
            to_compile.append(f)
    
    for f in to_compile:
        compileUi(os.path.join(uipath, f))

def compileUi(filepath: str):
    if os.path.exists(filepath):
        os.system(f'pyside6-uic -o ui_{filepath}.py {filepath}')
    else:
        print('there is no ui files named: ' + filepath)