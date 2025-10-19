from ast import keyword
from typing import Any
import ply.lex as lex

from shardc.utils.errors.syntax import ShardError_IllegalCharacter

class ShardLexer:
    def __init__(self):
        self.lexer: Any = None

    keywords = {
        "var": "VAR",
        "const": "CONST"
    }

    tokens = tuple(keywords.values()) + (
        "NUMBER", "ID",
        "PLUS", "MINUS", "STAR", "SLASH", "PERCENT",
        "LSHIFT", "RSHIFT", "AMPERSAND", "PIPE", "CARET", "TILDE",
        "EQUAL", "PLUSEQ", "MINUSEQ", "STAREQ", "SLASHEQ", "PERCENTEQ",
        "LSHIFTEQ", "RSHIFTEQ", "AMPERSANDEQ", "PIPEEQ", "CARETEQ", "TILDEEQ",
        "EQEQ", "NOTEQ", "LT", "GT", "LTEQ", "GTEQ",
        "LPAR", "RPAR", "SEMI", "COLON"
    )

    t_NUMBER = r'\d+'

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_STAR = r'\*'
    t_SLASH = r'/'
    t_PERCENT = r'%'

    t_LSHIFT = r'<<'
    t_RSHIFT = r'>>'
    t_AMPERSAND = r'&'
    t_PIPE = r'\|'
    t_CARET = r'\^'
    t_TILDE = r'~'

    t_EQUAL = r'='
    t_PLUSEQ = r'\+='
    t_MINUSEQ = r'-='
    t_STAREQ = r'\*='
    t_SLASHEQ = r'/='
    t_PERCENTEQ = r'%='
    t_LSHIFTEQ = r'<<='
    t_RSHIFTEQ = r'>>='
    t_AMPERSANDEQ = r'&='
    t_PIPEEQ = r'\|='
    t_CARETEQ = r'\^='
    t_TILDEEQ = r'~='

    t_EQEQ = r'=='
    t_NOTEQ = r'!='
    t_LT = r'<'
    t_GT = r'>'
    t_LTEQ = r'<='
    t_GTEQ = r'>='

    t_LPAR = r'\('
    t_RPAR = r'\)'
    t_SEMI = r';'
    t_COLON = ':'

    @lex.Token(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def t_ID(self, t):
        t.type = self.keywords.get(t.value, "ID")
        return t

    @lex.Token(r'\n+')
    def t_newline(self, t) -> None:
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'
    t_ignore_COMMENT = r'//.*'
    t_ignore_MULTILINE_COMMENT = r'/\*[\s\S]*?\*/'

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