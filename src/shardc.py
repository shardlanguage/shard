import argparse
from utils.file import *

def main():
    parser = argparse.ArgumentParser(prog='shardc', description='Shard language compiler.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', dest='mode', action='store_const', const='c', help='Compile to C source file')
    group.add_argument('-o', dest='mode', action='store_const', const='o', help='Compile to object file')
    group.add_argument('-x', dest='mode', action='store_const', const='x', help='Compile to executable')

    parser.add_argument('input_file', help='Input .shd file')
    parser.add_argument('-out', help='Output file name')

    args = parser.parse_args()

    if args.mode == 'c':
        compile_to_c(args.input_file)

    elif args.mode == 'o':
        c_file = compile_to_c(args.input_file)
        compile_c_to_object(c_file)
        os.remove(c_file)

    elif args.mode == 'x':
        c_file = compile_to_c(args.input_file)
        o_file = compile_c_to_object(c_file)
        link_object_to_executable(o_file)
        os.remove(c_file)
        os.remove(o_file)

if __name__ == "__main__":
    main()