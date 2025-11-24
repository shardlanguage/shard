import argparse

from shardc.cli.run import run_command

def cli():
    parser = argparse.ArgumentParser(description="The shardc compiler")

    parser.add_argument("-l", "--lex", type=str, help="Lex source code")
    parser.add_argument("-p", "--parse", type=str, help="Parse source code")
    parser.add_argument("-t", "--tree", type=str, help="Print AST of source code")
    parser.add_argument("-P", "--preprocess", type=str, help="Only execute the preprocessor")
    parser.add_argument("-c", "--compile", type=str, help="Compile source code")
    parser.add_argument("-to-o", "--to-object", type=str, help="Compile source code to object file")
    parser.add_argument("-to-x", "--to-executable", type=str, help="Compile source code to executable")

    parser.add_argument("-o", "--output", type=str, help="Output filename")
    parser.add_argument("-b", "--backend", type=str, help="Compiler backend")
    parser.add_argument("-T", "--target", type=str, help="Target compiler/interpreter")
    parser.add_argument("-tflags", "--target-flags", type=list[str], help="Pass flags to target specified with -T")
    parser.add_argument("--keep-all", action="store_true", help="Keep intermediate files")
    parser.add_argument("--no-main", action="store_true", help="Do not generate main() automatically")
    parser.add_argument("-nostd", action="store_true", help="Disable dependencies to std")

    args = parser.parse_args()
    run_command(args)