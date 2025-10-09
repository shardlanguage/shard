from shardc.cli.utils import lex_file

def execute_args(args):
    if args.lex:
        tokens = lex_file(args.lex)
        for tok in tokens:
            print(tok)