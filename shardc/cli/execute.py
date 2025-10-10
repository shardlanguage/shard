from shardc.cli.utils import lex_file, parse_file

def execute_args(args):
    if args.lex:
        tokens = lex_file(args.lex)
        for tok in tokens:
            print(tok)

    if args.parse:
        parse_file(args.parse)

    if args.tree:
        ast = parse_file(args.tree)
        for node in ast:
            print(node)