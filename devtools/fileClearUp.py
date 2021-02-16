import os, shutil
import re


def removeAllUicFiles():
    files_dir = os.sep.join((os.getcwd(), 'src', 'ui'))
    files = os.listdir(files_dir)
    to_remove = []
    pat = re.compile(r'^ui_.*\.py')
    for f in files:
        if pat.match(f):
            to_remove.append(f)

    if len(to_remove) == 0:
        print('no uic files found at: ' + files_dir)
        return

    print('files to remove:')
    for f in to_remove:
        print(f)
    
    option = input('remove? [y/n]')
    if option == 'y':
        for f in to_remove:
            os.remove(os.path.join(files_dir, f))
        print('uic files removed')
    else:
        print('remove canceled')


def removeAllPycFiles():
    searchPath = [
        os.getcwd(),
        os.sep.join((os.getcwd(), 'devtools')),
        os.sep.join((os.getcwd(), 'src', 'ui'))
    ]

    for dir in searchPath:
        if '__pycache__' in os.listdir(dir):
            # print(dir)
            shutil.rmtree(os.sep.join((dir, '__pycache__')))