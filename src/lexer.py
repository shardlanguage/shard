import ply.lex as lex

keywords = {
    'byte': 'BYTE_T',
    'word': 'WORD_T',
    'dword': 'DWORD_T',
    'qword': 'QWORD_T',
    'const': 'CONST_T',
    'if': 'IF',
    'else': 'ELSE',
    'forever': 'FOREVER',
    'while': 'WHILE',
    'until': 'UNTIL',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}

tokens = (
    'COMMENT',
    'NUMBER', 'ID',
    'PLUS', 'MINUS', 'STAR', 'SLASH', 'LSHIFT', 'RSHIFT',
    'LPAR', 'RPAR', 'SEMI', 'LBRACE', 'RBRACE',
    'EQUAL', 'PLUSEQ', 'MINUSEQ', 'STAREQ', 'SLASHEQ', 'ANDEQ', 'OREQ', 'XOREQ', 'NOTEQ', 'LSHIFTEQ', 'RSHIFTEQ',
    'BITAND', 'BITOR', 'XOR', 'BITNOT',
    'EQEQUAL', 'NOTEQUAL', 'LESS', 'GREAT', 'LESSEQ', 'GREATEQ'
)

tokens += tuple(keywords.values())

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

t_NUMBER = r'\d+(\.\d+)?'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    return t

t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'

t_LPAR = r'\('
t_RPAR = r'\)'
t_SEMI = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_EQUAL = r'='
t_PLUSEQ = r'\+='
t_MINUSEQ = r'-='
t_STAREQ = r'\*='
t_SLASHEQ = r'/='
t_ANDEQ = r'&='
t_OREQ = r'\|='
t_XOREQ = r'\^='
t_NOTEQ = r'~='
t_LSHIFTEQ = r'<<='
t_RSHIFTEQ = r'>>='

t_BITAND = r'&'
t_BITOR = r'\|'
t_XOR = r'\^'
t_BITNOT = r'~'

t_EQEQUAL = r'=='
t_NOTEQUAL = r'!='
t_LESS = r'<'
t_GREAT = r'>'
t_LESSEQ = r'<='
t_GREATEQ = r'>='

def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)

def t_error(t):
    print(f"ERROR: Illegal character '{t.value}' found at line {t.lineno} and position {t.value}")
    t.lexer.skip(1)

lexer = lex.lex()