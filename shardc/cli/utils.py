from shardc.frontend.lexer import ShardLexer
from shardc.utils.checks import check_path

def lex_file(path: str) -> list:
    check_path(path)

    with open(path, 'r', encoding="utf-8") as f:
        content = f.read()

    lexer = ShardLexer()
    lexer.build()
    tokens = lexer.lex_code(content)

    return tokens