from shardc.cli.utils import compile_file, lex_file, parse_file

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

    if args.assembly:
        if args.output:
            compile_file(args.assembly, args.output)
        else:
            compile_file(args.assembly)