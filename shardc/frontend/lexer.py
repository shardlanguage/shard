from typing import Any
import ply.lex as lex

from shardc.utils.errors.syntax import ShardError_IllegalCharacter

class ShardLexer:
    def __init__(self):
        self.lexer: Any = None

    tokens = (
        "NUMBER",
        "PLUS", "MINUS", "STAR", "SLASH",
        "LPAR", "RPAR", "SEMI"
    )

    t_NUMBER = r'\d+'

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_STAR = r'\*'
    t_SLASH = r'/'

    t_LPAR = r'\('
    t_RPAR = r'\)'
    t_SEMI = r';'

    @lex.Token(r'\n+')
    def t_newline(self, t) -> None:
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(self, t) -> None:
        ShardError_IllegalCharacter(t.value[0], t.lexer.lineno, t.lexer.lexpos).display()

    def build(self, **kwargs) -> None:
        self.lexer = lex.lex(module=self, **kwargs)

    def lex_code(self, code: str) -> list:
        self.lexer.input(code)
        tokens = []
        
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)

        return tokens