import os, sys
import re



def removeAllUicFiles():
    files_dir = os.path.join(os.getcwd(), 'ui')
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


if __name__ == '__main__':
    removeAllUicFiles()