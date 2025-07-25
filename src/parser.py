import ply.yacc as yacc

from lexer import tokens
from tree import *

precedence = (
    ('right', 'EQUAL', 'PLUSEQ', 'MINUSEQ', 'STAREQ', 'SLASHEQ', 'ANDEQ', 'OREQ', 'XOREQ', 'NOTEQ', 'LSHIFTEQ', 'RSHIFTEQ'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'BITOR'),
    ('left', 'XOR'),
    ('left', 'BITAND'),
    ('nonassoc', 'LESS', 'GREAT', 'LESSEQ', 'GREATEQ', 'EQEQUAL', 'NOTEQUAL'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'SLASH'),
    ('right', 'BITNOT'),
    ('right', 'POSITIVE', 'NEGATIVE')
)

def p_program(p):
    """
    program : statement_list
    """
    p[0] = p[1]

def p_statement_list(p):
    """
    statement_list : statement
                   | statement_list separator statement
    """
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = p[1] if p[1] is not None else []
        if p[3] is not None:
            p[0] += [p[3]]

def p_statement(p):
    """
    statement : empty
              | expression
              | declaration
              | codeblock
              | condition
              | loop
    """
    p[0] = p[1]

def p_empty(p):
    """
    empty :
          | COMMENT
    """
    pass

def p_expression_value(p):
    """
    expression : NUMBER
    """
    p[0] = Value(p[1])

def p_expression_variable_access(p):
    """
    expression : ID
    """
    p[0] = VariableAccess(p[1])

def p_expression_array_access(p):
    """
    expression : ID LSQB expression RSQB
    """
    p[0] = ArrayAccess(p[1], p[3])

def p_expression_unary_op(p):
    """
    expression : PLUS expression %prec POSITIVE
               | MINUS expression %prec NEGATIVE
               | NOT expression
               | BITNOT expression
    """
    p[0] = UnaryOp(p[1], p[2])

def p_expression_binary_op(p):
    """
    expression : expression PLUS expression
               | expression MINUS expression
               | expression STAR expression
               | expression SLASH expression
               | expression AND expression
               | expression OR expression
               | expression BITAND expression
               | expression BITOR expression
               | expression XOR expression
               | expression EQEQUAL expression
               | expression NOTEQUAL expression
               | expression LESS expression
               | expression GREAT expression
               | expression LESSEQ expression
               | expression GREATEQ expression
               | expression LSHIFT expression
               | expression RSHIFT expression
    """
    p[0] = BinaryOp(p[1], p[2], p[3])

def p_expression_variable_assignment(p):
    """
    expression : ID EQUAL expression
               | ID PLUSEQ expression
               | ID MINUSEQ expression
               | ID STAREQ expression
               | ID SLASHEQ expression
               | ID ANDEQ expression
               | ID OREQ expression
               | ID XOREQ expression
               | ID NOTEQ expression
               | ID LSHIFTEQ expression
               | ID RSHIFTEQ expression
    """
    p[0] = VariableAssignment(p[1], p[2], p[3])

def p_expression_array_assignment(p):
    """
    expression : ID LSQB expression RSQB EQUAL expression
               | ID LSQB expression RSQB PLUSEQ expression
               | ID LSQB expression RSQB MINUSEQ expression
               | ID LSQB expression RSQB STAREQ expression
               | ID LSQB expression RSQB SLASHEQ expression
               | ID LSQB expression RSQB ANDEQ expression
               | ID LSQB expression RSQB OREQ expression
               | ID LSQB expression RSQB XOREQ expression
               | ID LSQB expression RSQB NOTEQ expression
               | ID LSQB expression RSQB LSHIFTEQ expression
               | ID LSQB expression RSQB RSHIFTEQ expression
    """
    p[0] = ArrayAssignment(p[1], p[3], p[5], p[6])

def p_expression_group(p):
    """
    expression : LPAR expression RPAR
    """
    p[0] = Group(p[2])

def p_declaration_variable(p):
    """
    declaration : datatype ID
                | datatype ID EQUAL expression
    """
    if len(p) == 3:
        p[0] = VariableDeclaration(p[1][0], p[1][1], p[2], None)
    else:
        p[0] = VariableDeclaration(p[1][0], p[1][1], p[2], p[4])

def p_declaration_array(p):
    """
    declaration : datatype ID LSQB expression RSQB
                | datatype ID LSQB expression RSQB EQUAL LSQB expression_list RSQB
    """
    if len(p) == 6:
        p[0] = ArrayDeclaration(p[1][0], p[1][1], p[2], p[4], None)
    else:
        p[0] = ArrayDeclaration(p[1][0], p[1][1], p[2], p[4], p[8])

def p_codeblock(p):
    """
    codeblock : LBRACE statement_list RBRACE
    """
    p[0] = CodeBlock(p[2])

def p_condition(p):
    """
    condition : IF expression codeblock
              | IF expression codeblock ELSE codeblock
    """
    if len(p) == 4:
        p[0] = Condition(p[2], p[3], [])
    else:
        p[0] = Condition(p[2], p[3], p[5])

def p_loop_unconditionnal(p):
    """
    loop : FOREVER codeblock
    """
    p[0] = LoopUnconditionnal(p[2])

def p_loop_conditionnal(p):
    """
    loop : WHILE expression codeblock
         | UNTIL expression codeblock
    """
    p[0] = LoopConditionnal(p[1], p[2], p[3])

def p_separator(p):
    """
    separator : SEMI
    """
    p[0] = p[1]

def p_datatype(p):
    """
    datatype : primary_type
             | type_modifier primary_type
    """
    p[0] = [None, p[1]] if len(p) == 2 else [p[1], p[2]]

def p_primary_type(p):
    """
    primary_type : BYTE_T
                 | WORD_T
                 | DWORD_T
                 | QWORD_T
                 | FLOAT_T
                 | DOUBLE_T
                 | UBYTE_T
                 | UWORD_T
                 | UDWORD_T
                 | UQWORD_T
    """
    p[0] = p[1]

def p_type_modifier(p):
    """
    type_modifier : CONST_T
    """
    p[0] = p[1]

def p_expression_list(p):
    """
    expression_list : expression
                    | expression COMMA expression_list
    """
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_error(p):
    if p:
        print(f"ERROR: syntax error at \"{p.value}\" at line {p.lineno}")
    else:
        print("ERROR: unexpected end of statement")

parser = yacc.yacc(outputdir="parser_out")