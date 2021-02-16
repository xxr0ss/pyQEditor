from devtools import fileClearUp, compileUI
import argparse
import os


def parse():
    parser = argparse.ArgumentParser(description='Dev Tools')
    parser.add_argument('-rm', choices=['uic', 'pyc'], help='remove certain files')
    parser.add_argument('-uic', default='--all', help='compile uic files, default to recompile all')

    return parser.parse_args()
    
rm_actions = {
    'uic': fileClearUp.removeAllUicFiles,
    'pyc': lambda: print('Not implemented')
}


if __name__ == '__main__':
    args = parse()
    if args.rm != None:
        rm_actions[args.rm]()
    if args.uic != None:
        uipath = os.path.join(os.getcwd(), 'ui')
        if args.uic == '--all':
            compileUI.compileAll(uipath)
        else:
            compileUI.compileUi(os.path.join(args.uic))
