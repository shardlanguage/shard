from shardc.cli.utils import compile_file, compile_file_to_executable, compile_file_to_object, lex_file, parse_file, preprocess_file

def run_command(args):
    backend = args.backend or "c"
    output = args.output or "output"
    target = args.target or "clang"
    target_flags = args.target_flags or ""
    keep_all = args.keep_all or False
    no_main = args.no_main or False
    no_std = args.nostd or False
    main = not no_main

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
        compile_file(args.compile, lang=backend, output=output, keep_all=keep_all, main=main, no_std=no_std)

    if args.to_object:
        compile_file_to_object(args.to_object, lang=backend, output=output, target=target, exflags=target_flags, keep_all=keep_all, main=main, no_std=no_std)

    if args.to_executable:
        compile_file_to_executable(args.to_executable, lang=backend, output=output, target=target, exflags=target_flags, keep_all=keep_all, main=main, no_std=no_std)