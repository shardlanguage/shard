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