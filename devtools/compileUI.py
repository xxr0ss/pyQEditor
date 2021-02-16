import os
import re


def _filepathFix(filepath):
    if filepath.find('/'):
        filepath.replace('/', os.sep)
    if filepath.find('\\'):
        filepath.replace('\\', os.sep)
    return filepath

def compileAll():
    # TODO 考虑把搜索路径移出去作为命令行解析的一部分
    searchpath = os.sep.join((os.getcwd(), 'src', 'ui'))
    files = os.listdir(searchpath)
    to_compile = []
    pat = re.compile(r'.*\.ui')
    for f in files:
        if pat.match(f):
            to_compile.append(f)
    
    for f in to_compile:
        compileUi(os.path.join(searchpath, f))

def compileUi(filepath: str):
    filepath = _filepathFix(filepath)
    if os.path.exists(filepath):
        fileDirName = os.sep.join(filepath.split(os.sep)[:-1])
        fileBasenameNoExtension = filepath.split(os.sep)[-1].removesuffix('.ui')
        cmd = f'pyside6-uic -o {fileDirName}{os.sep}ui_{fileBasenameNoExtension}.py {filepath}'
        # print(cmd)
        os.popen(cmd)
    else:
        print('there is no ui files named: ' + filepath)