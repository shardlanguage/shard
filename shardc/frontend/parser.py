from typing import Any
import ply.yacc as yacc

from shardc.frontend.lexer import ShardLexer
from shardc.frontend.nodes.expression import NodeBinaryOp, NodeGroup, NodeUnaryOp, NodeValue
from shardc.utils.const.types import INT
from shardc.utils.errors.syntax import ShardError_BadSyntax

class ShardParser:
    def __init__(self):
        self.parser: Any = None
        self.lexer = ShardLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens

    precedence = (
        ("left", "PLUS", "MINUS"),
        ("left", "STAR", "SLASH"),
        ("right", "POS", "NEG")
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
        """
        p[0] = p[1]

    def p_expression_value(self, p) -> None:
        """
        expression : NUMBER
        """
        p[0] = NodeValue(p[1], INT)

    def p_expression_unary(self, p) -> None:
        """
        expression : PLUS expression %prec POS
                   | MINUS expression %prec NEG
        """
        p[0] = NodeUnaryOp(p[1], p[2])

    def p_expression_binary(self, p) -> None:
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression STAR expression
                   | expression SLASH expression
        """
        p[0] = NodeBinaryOp(p[2], p[1], p[3])

    def p_expression_group(self, p) -> None:
        """
        expression : LPAR expression RPAR
        """
        p[0] = NodeGroup(p[2])

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