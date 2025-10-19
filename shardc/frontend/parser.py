from typing import Any
import ply.yacc as yacc

from shardc.frontend.lexer import ShardLexer
from shardc.frontend.nodes.declaration import NodeVariableDecl
from shardc.frontend.nodes.expression import NodeAssignOp, NodeBinaryOp, NodeGroup, NodeID, NodeUnaryOp, NodeValue
from shardc.utils.const.types import INT
from shardc.utils.errors.syntax import ShardError_BadSyntax

class ShardParser:
    def __init__(self):
        self.parser: Any = None
        self.lexer = ShardLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens

    precedence = (
        ("right", "EQUAL", "PLUSEQ", "MINUSEQ", "STAREQ", "SLASHEQ", "PERCENTEQ", "LSHIFTEQ", "RSHIFTEQ", "AMPERSANDEQ", "PIPEEQ", "CARETEQ", "TILDEEQ"),
        ("left", "PLUS", "MINUS"),
        ("left", "STAR", "SLASH", "PERCENT"),
        ("left", "LSHIFT", "RSHIFT"),
        ("left", "LT", "GT", "LTEQ", "GTEQ"),
        ("left", "EQEQ", "NOTEQ"),
        ("left", "AMPERSAND"),
        ("left", "CARET"),
        ("left", "PIPE"),
        ("right", "POS", "NEG", "TILDE"),
    )

    def p_program(self, p) -> None:
        """
        program : statement_list_opt
        """
        p[0] = p[1]

    def p_statement_list_opt(self, p) -> None:
        """
        statement_list_opt : statement_list
                           |
        """
        p[0] = p[1] if p[1] else None

    def p_statement_list(self, p) -> None:
        """
        statement_list : statement
                       | statement statement_list
        """
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    def p_statement(self, p) -> None:
        """
        statement : expression SEMI
                  | declaration SEMI
        """
        p[0] = p[1]

    def p_expression_number(self, p) -> None:
        """
        expression : NUMBER
        """
        p[0] = NodeValue(p[1], INT)

    def p_expression_id(self, p) -> None:
        """
        expression : id_access
        """
        p[0] = NodeID(p[1])

    def p_expression_unary(self, p) -> None:
        """
        expression : PLUS expression %prec POS
                   | MINUS expression %prec NEG
                   | TILDE expression
        """
        p[0] = NodeUnaryOp(p[1], p[2])

    def p_expression_binary(self, p) -> None:
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression STAR expression
                   | expression SLASH expression
                   | expression PERCENT expression
                   | expression AMPERSAND expression
                   | expression CARET expression
                   | expression PIPE expression
                   | expression LSHIFT expression
                   | expression RSHIFT expression
                   | expression EQEQ expression
                   | expression NOTEQ expression
                   | expression LT expression
                   | expression GT expression
                   | expression LTEQ expression
                   | expression GTEQ expression
        """
        p[0] = NodeBinaryOp(p[2], p[1], p[3])

    def p_expression_assignment(self, p) -> None:
        """
        expression : id_access EQUAL expression
                   | id_access PLUSEQ expression
                   | id_access MINUSEQ expression
                   | id_access STAREQ expression
                   | id_access SLASHEQ expression
                   | id_access PERCENTEQ expression
                   | id_access LSHIFTEQ expression
                   | id_access RSHIFTEQ expression
                   | id_access AMPERSANDEQ expression
                   | id_access PIPEEQ expression
                   | id_access CARETEQ expression
                   | id_access TILDEEQ expression
        """
        p[0] = NodeAssignOp(p[1], p[2], p[3])

    def p_expression_group(self, p) -> None:
        """
        expression : LPAR expression RPAR
        """
        p[0] = NodeGroup(p[2])

    def p_declaration_variable(self, p) -> None:
        """
        declaration : prefix ID COLON type EQUAL expression
                    | prefix ID COLON type
        """
        if len(p) == 7:
            p[0] = NodeVariableDecl(p[1], p[2], p[4], p[6])
        else:
            p[0] = NodeVariableDecl(p[1], p[2], p[4], None)

    def p_id_access(self, p) -> None:
        """
        id_access : ID
        """
        p[0] = p[1]

    def p_prefix(self, p) -> None:
        """
        prefix : VAR
               | CONST
        """
        p[0] = p[1]

    def p_type(self, p) -> None:
        """
        type : ID
        """
        p[0] = p[1]

    def p_error(self, p) -> None:
        ShardError_BadSyntax(p.value if p else "EOF", p.lexer.lineno).display()

    def build(self, **kwargs) -> None:
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse_code(self, code: str) -> list:
        ast = self.parser.parse(code)
        for i in ast:
            if i is None:
                ast.remove(i)
        return ast