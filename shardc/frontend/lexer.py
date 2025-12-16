from typing import Any
import ply.lex as lex

from shardc.utils.errors.syntax import ShardError_IllegalCharacter

class ShardLexer:
    def __init__(self):
        self.lexer: Any = None
        self.keywords = {
            "var": "VAR",
            "const": "CONST",
            "and": "AND",
            "or": "OR",
            "not": "NOT",
            "if": "IF",
            "elif": "ELIF",
            "else": "ELSE",
            "forever": "FOREVER",
            "while": "WHILE",
            "until": "UNTIL",
            "break": "BREAK",
            "continue": "CONTINUE",
            "func": "FUNC",
            "return": "RETURN",
            "as": "AS",
            "struct": "STRUCT",
            "sizeof": "SIZEOF",
            "_c_": "C",
            "extern": "EXTERN",
            "type": "TYPE",
            "newtype": "NEWTYPE",
            "for": "FOR",
            "namespace": "NAMESPACE"
        }
        self.tokens = (
            "RESET_LINE",
            "NUMBER", "ID", "CHAR", "STRING",
            "PLUS", "MINUS", "STAR", "SLASH", "PERCENT",
            "SHIFTL", "SHIFTR", "AMPERSAND", "PIPE", "CARET", "TILDE",
            "EQEQ", "NOTEQ", "LT", "GT", "LTEQ", "GTEQ",
            "EQUAL", "PLUSEQ", "MINUSEQ", "STAREQ", "SLASHEQ", "PERCENTEQ", "SHIFTLEQ", "SHIFTREQ",
            "AMPERSANDEQ", "PIPEEQ", "CARETEQ", "TILDEEQ",
            "LPAR", "RPAR", "SEMI", "COLON", "LSQB", "RSQB", "COMMA", "LBRACE", "RBRACE", "ARROW", "DOT", "COLONS"
        )
        self.tokens += tuple(self.keywords.values())
        
    def t_RESET_LINE(self, t):
        r'\#\#'
        t.lexer.lineno = 0
        return t

    def t_NUMBER(self, t):
        r'(0b[01]+|0o[0-7]+|0x[0-9A-Fa-f]+|\d+(\.\d+)?([eE][+-]?\d+)?)'
        s = t.value
        if s.startswith('0b'):
            t.value = int(s, 2)
        elif s.startswith('0o'):
            t.value = int(s, 8)
        elif s.startswith('0x'):
            t.value = int(s, 16)
        elif '.' in s or 'e' in s or 'E' in s:
            t.value = float(s)
        else:
            t.value = int(s)
        return t

    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        t.type = self.keywords.get(t.value, "ID")
        return t

    t_CHAR = r"'([^'\\]|\\.)'"
    t_STRING = r'"([^"\\]|\\.)*"'
    
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_STAR = r'\*'
    t_SLASH = r'/'
    t_PERCENT = r'%'

    t_SHIFTL = r'<<'
    t_SHIFTR = r'>>'
    t_AMPERSAND = r'&'
    t_PIPE = r'\|'
    t_CARET = r'\^'
    t_TILDE = r'~'

    t_EQEQ = r'=='
    t_NOTEQ = r'!='
    t_LT = r'<'
    t_GT = r'>'
    t_LTEQ = r'<='
    t_GTEQ = r'>='

    t_EQUAL = r'='
    t_PLUSEQ = r'\+='
    t_MINUSEQ = r'-='
    t_STAREQ = r'\*='
    t_SLASHEQ = r'/='
    t_PERCENTEQ = r'%='
    t_SHIFTLEQ = r'<<='
    t_SHIFTREQ = r'>>='
    t_AMPERSANDEQ = r'&='
    t_PIPEEQ = r'\|='
    t_CARETEQ = r'\^='
    t_TILDEEQ = r'~='
    
    t_LPAR = r'\('
    t_RPAR = r'\)'
    t_SEMI = r';'
    t_COLON = r':'
    t_LSQB = r'\['
    t_RSQB = r'\]'
    t_COMMA = r','
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_ARROW = r'->'
    t_DOT = r'\.'
    t_COLONS = r'::'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'
    t_ignore_COMMENT = r'//.*'
    t_ignore_COMMENT_MULTILINE = r'/\*[\s\S]*?\*/'

    def t_error(self, t):
        ShardError_IllegalCharacter(t.lineno, t.lexpos, t.value[0]).display()

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def lex_code(self, code: str):
        self.lexer.input(code)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens