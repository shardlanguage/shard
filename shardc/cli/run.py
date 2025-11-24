from shardc.cli.utils import compile_file, compile_file_to_executable, compile_file_to_object, lex_file, parse_file, preprocess_file

def run_command(args):
    backend = "c"
    output = "output"
    target = "clang"
    target_flags = []
    keep_all = False
    no_main = False
    no_std = False

    if args.backend:
        backend = args.backend

    if args.output:
        output = args.output

    if args.target:
        target = args.target

    if args.target_flags:
        target_flags.extend(args.target_flags)

    if args.keep_all:
        keep_all = args.keep_all
    
    if args.no_main:
        no_main = args.no_main

    if args.nostd:
        no_std = args.nostd

    if args.lex:
        tokens = lex_file(args.lex)
        for tok in tokens:
            print(tok)

    if args.parse:
        parse_file(args.parse)

    if args.tree:
        tree = parse_file(args.tree)
        for node in tree:
            print(node)

    if args.preprocess:
        preprocess_file(args.preprocess)

    if args.compile:
        compile_file(args.compile, backend, output, keep_all, not no_main, no_std)

    if args.to_object:
        compile_file_to_object(args.to_object, backend, output, target, target_flags, keep_all)

    if args.to_executable:
        compile_file_to_executable(args.to_executable, backend, output, target, target_flags, keep_all)