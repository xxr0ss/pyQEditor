import os, sys
import re



def removeAllUiFiles():
    files_dir = os.path.join(os.getcwd(), 'ui')
    files = os.listdir(files_dir)
    to_remove = []
    pat = re.compile('ui_*.py')
    for f in files:
        if re.match(pat):
            to_remove.add(f)
    for f in to_remove:
        os.remove(os.path.join(files_dir, f))


if __name__ == '__main__':
    removeAllUiFiles()