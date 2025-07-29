# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains the shardc CLI.
# =====================================================================

# Import modules
import argparse
import os

from utils.file import *

# Main function
def main():
    parser = argparse.ArgumentParser(prog='shardc', description='Shard language compiler.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', dest='mode', action='store_const', const='c', help='Compile Shard to C source file')
    group.add_argument('-o', dest='mode', action='store_const', const='o', help='Compile C to object file')
    group.add_argument('-x', dest='mode', action='store_const', const='x', help='Compile object file to executable')
    group.add_argument('-cox', dest='mode', action='store_const', const='cox', help="Execute -c -o -x in a single time")

    parser.add_argument('input_file', help='Input .shd file')
    parser.add_argument('--keep-all', action="store_true", help="Don't remove C and object files when -cox is used")
    parser.add_argument('--dbg-err', action="store_true", help="Display error traceback, only used for shardc features development")

    args = parser.parse_args()

    if args.mode == 'c':
        compile_to_c(args.input_file, errdbg=True if args.dbg_err else False)

    elif args.mode == 'o':
        compile_c_to_object(args.input_file)

    elif args.mode == 'x':
        link_object_to_executable(args.input_file)

    elif args.mode == 'cox':
        c = compile_to_c(args.input_file)
        o = compile_c_to_object(c)
        link_object_to_executable(o)

        if not args.keep_all:
            os.remove(c)
            os.remove(o)

if __name__ == "__main__":
    main()