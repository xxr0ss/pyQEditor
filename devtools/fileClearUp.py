import os, shutil
import re
from typing import Callable, Iterable


def removeAllUicFiles():
    files_dir = os.sep.join((os.getcwd(), 'src', 'QEditor', 'ui'))
    checker = lambda f: f.startswith('ui_') and f.endswith('.py')
    removeFiles([files_dir], checker)

def removeAllRcFiles():
    files_dir = os.sep.join((os.getcwd(), 'src', 'QEditor'))
    checker = lambda f: f.startswith('rc_') and f.endswith('.py')
    removeFiles([files_dir], checker)


def removeAllPycFiles():
    searchPath = [
        os.getcwd(),
        os.sep.join((os.getcwd(), 'devtools')),
        os.sep.join((os.getcwd(), 'src', 'QEditor' 'ui'))
    ]


    for dir in searchPath:
        if '__pycache__' in os.listdir(dir):
            # print(dir)
            shutil.rmtree(os.sep.join((dir, '__pycache__')))


def removeFiles(search_paths: Iterable[str], check_target: Callable[[str], bool]):
    for path in search_paths:
        files = os.listdir(path)

        to_remove = []
        for f in files:
            if not os.path.isfile(path+os.sep+f):
                continue

            if check_target(f):
                to_remove.append(path+os.sep+f)
        
    print('files to remove:')
    for f in to_remove:
        print(f)
    
    option = input('remove? [y/n]')
    if option == 'y':
        for f in to_remove:
            os.remove(f)
        print('all files removed')
    else:
        print('canceled')
