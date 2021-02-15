from buildtools import clearUi
import argparse


def parse():
    parser = argparse.ArgumentParser(description='Dev Tools')
    parser.add_argument('-rm', choices=['uic', 'pyc'], help='remove certain files')

    return parser.parse_args()
    
rm_actions = {
    'uic': clearUi.removeAllUicFiles,
    'pyc': lambda: print('Not implemented')
}


if __name__ == '__main__':
    args = parse()
    rm_actions[args.rm]()
    