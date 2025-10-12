from shardc.backend.codegen.x86_64 import x86_64
from shardc.backend.visitor import CodeGenerator
from shardc.frontend.lexer import ShardLexer
from shardc.frontend.parser import ShardParser
from shardc.utils.checks import check_path

def lex_file(path: str) -> list:
    check_path(path)

    with open(path, 'r', encoding="utf-8") as f:
        content = f.read()

    lexer = ShardLexer()
    lexer.build()
    tokens = lexer.lex_code(content)

    return tokens

def parse_file(path: str) -> list:
    check_path(path)

    with open(path, 'r', encoding="utf-8") as f:
        content = f.read()

    parser = ShardParser()
    parser.build(write_tables=False)
    ast = parser.parse_code(content)

    return ast

def compile_file(path: str) -> None:
    check_path(path)
    
    ast = parse_file(path)
    cg = CodeGenerator(x86_64())
    for node in ast:
        if node is not None:
            cg.generate(node)

    filename = path.replace(".sd", ".asm")
    with open(filename, 'w', encoding="utf-8") as f:
        f.write('\n'.join(cg.output))