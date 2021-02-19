from devtools import fileClearUp, fileGen
import argparse
import os


def rm(args):
    if not any((args.uic, args.pyc, args.rcc)):
        print('Please specify type of files to remove')
        return

    if args.uic:
        fileClearUp.removeAllUicFiles()
    if args.pyc:
        fileClearUp.removeAllPycFiles()
    if args.rcc:
        fileClearUp.removeAllRcFiles()


def uic(args):
    if args.all:
        fileGen.compileAllUi()
    elif args.uifilename is not None:
        files_dir = os.sep.join((os.getcwd(), 'QEditor', 'ui'))
        for f in args.uifilename:
            if not f.endswith('.ui'):
                f += '.ui'
            fileGen.compileUi(os.path.join(files_dir, f))


def rcc(args):
    if args.all:
        fileGen.compile_all_qrc()
    elif args.qrcfilename is not None:
        files_dir = os.sep.join((os.getcwd(), 'QEditor'))
        for f in args.uifilename:
            if not f.endswith('.qrc'):
                f += '.qrc'
            fileGen.compileUi(os.path.join(files_dir, f))


def main_parse():
    parser = argparse.ArgumentParser(description="Dev Tools")
    parser.add_argument('-v', '--verbose', action='store_true', help='show more information')

    # parser.add_argument('rm', help='remove specified type of files')
    subparsers = parser.add_subparsers(
        title='supported commands', help='sub-command help')

    # parser to handle file deletion
    parser_rm = subparsers.add_parser(
        'rm', help='remove files of specified type')
    parser_rm.add_argument('--uic', action='store_true',
                           help='remove all uic compiled files')
    parser_rm.add_argument('--pyc', action='store_true',
                           help='remove all pyc files')
    parser_rm.add_argument('--rcc', action='store_true', help='remove all rc files')
    parser_rm.set_defaults(func=rm)

    # parser to handle .ui compiling
    parser_uic = subparsers.add_parser('uic', help='compile ui files')
    parser_uic.add_argument(
        '-a', '--all', action='store_true', help='compile all ui files')
    parser_uic.add_argument(dest='uifilename', metavar='filename', nargs='*')
    parser_uic.set_defaults(func=uic)

    parser_rcc = subparsers.add_parser('rcc', help='compile rcc files')
    parser_rcc.add_argument(
        '-a', '--all', action='store_true', help='compile all rcc files')
    parser_rcc.add_argument(dest='qrcfilename', metavar='filename', nargs='*')
    parser_rcc.set_defaults(func=rcc)

    return parser.parse_args()


def main():
    parse_args = main_parse()
    if parse_args.verbose:
        print(parse_args)
    parse_args.func(parse_args)



if __name__ == '__main__':
    main()
