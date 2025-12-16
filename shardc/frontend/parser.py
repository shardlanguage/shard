from typing import Any, override
import ply.yacc as yacc
import codecs

from shardc.frontend.lexer import ShardLexer
from shardc.frontend.tree.codeblocks import NodeCodeBlock, NodeNamespaceBody, NodeStructureBody
from shardc.frontend.tree.condition_struct import NodeCondition, NodeElif, NodeElse, NodeIf
from shardc.frontend.tree.declarations import NodeExternDeclaration, NodeVariableDeclaration
from shardc.frontend.tree.expressions import NodeArrayAccess, NodeArrayAssignmentOp, NodeAssignmentOp, NodeBinaryOp, NodeCast, NodeFieldAccess, NodeFieldAssignmentOp, NodeFunctionCall, NodeGroupOp, NodeIDAccess, NodeNamespaceAccess, NodeNamespaceAssignmentOp, NodeNumber, NodeString, NodeUnaryOp
from shardc.frontend.tree.flow_control import NodeBreak, NodeContinue, NodeReturn
from shardc.frontend.tree.function_def import NodeFunctionDefinition
from shardc.frontend.tree.inline import NodeInlineC
from shardc.frontend.tree.loop_struct import NodeLoopFor, NodeLoopForever, NodeLoopUntil, NodeLoopWhile
from shardc.frontend.tree.namespace_def import NodeNamespaceDefinition
from shardc.frontend.tree.structure_def import NodeStructureDefinition
from shardc.frontend.tree.types import NodeArrayType, NodeDereferenceType, NodeNamespaceType, NodeNewType, NodeType, NodeTypeAlias
from shardc.utils.constants.keywords import KW_WHILE
from shardc.utils.constants.symbols import SYM_COLON_BLOCK, SYM_DOT
from shardc.utils.errors.syntax import ShardError_BadSyntax, ShardError_EOF

class ShardParser:
    def __init__(self):
        self.parser: Any = None
        self.lexer = ShardLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.precedence = (
            ("left", "AND"),
            ("left", "OR"),
            ("left", "PIPE"),
            ("left", "CARET"),
            ("left", "AMPERSAND"),
            ("left", "EQEQ", "NOTEQ"),
            ("left", "LT", "GT", "LTEQ", "GTEQ"),
            ("left", "SHIFTL", "SHIFTR"),
            ("left", "PLUS", "MINUS"),
            ("left", "STAR", "SLASH", "PERCENT"),
            ("right", "UPLUS", "UMINUS", "TILDE", "NOT", "REF", "SIZEOF"),
            ("right", "AS", "EQUAL", "PLUSEQ", "MINUSEQ", "STAREQ", "SLASHEQ", "PERCENTEQ", "SHIFTLEQ", "SHIFTREQ", "AMPERSANDEQ", "PIPEEQ", "CARETEQ", "TILDEEQ")
        )

    def p_program(self, p):
        """
        program : statement_list_opt
        """
        p[0] = p[1]

    def p_statement_opt(self, p):
        """
        statement_list_opt : statement_list
                           |
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = []

    def p_statement_list(self, p):
        """
        statement_list : statement
                       | statement statement_list
        """
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    def p_statement(self, p):
        """
        statement : special
                  | expression SEMI
                  | declaration SEMI
                  | codeblock
                  | conditional_structure
                  | loop_structure
                  | flow_control SEMI
                  | function_definition
                  | structure_definition
                  | namespace_definition
                  | inline SEMI
                  | extern_declaration SEMI
                  | type_definition SEMI
        """
        p[0] = p[1]

    def p_special_reset_line(self, p):
        """
        special : RESET_LINE
        """
        p.lexer.lineno = 0
        p[0] = None

    def p_expression_number(self, p):
        """
        expression : NUMBER
        """
        p[0] = NodeNumber(p[1])

    def p_expression_character(self, p):
        """
        expression : CHAR
        """
        s = p[1][1:-1]
        char = codecs.decode(s, "unicode_escape")
        p[0] = NodeNumber(ord(char))

    def p_expression_string(self, p):
        """
        expression : STRING
        """
        p[0] = NodeString(p[1])

    def p_expression_id(self, p):
        """
        expression : id_access
        """
        p[0] = p[1]

    def p_expression_function_call(self, p):
        """
        expression : id_access LPAR expression_list RPAR
        """
        p[0] = NodeFunctionCall(p[1], p[3])

    def p_expression_unary(self, p):
        """
        expression : PLUS expression %prec UPLUS
                   | MINUS expression %prec UMINUS
                   | TILDE expression
                   | NOT expression
                   | AMPERSAND expression %prec REF
        """
        p[0] = NodeUnaryOp(p[1], p[2])

    def p_expression_unary_special(self, p):
        """
        expression : SIZEOF LPAR expression RPAR
        """
        p[0] = NodeUnaryOp(p[1], p[3])

    def p_expression_binary(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression STAR expression
                   | expression SLASH expression
                   | expression PERCENT expression
                   | expression SHIFTL expression
                   | expression SHIFTR expression
                   | expression AMPERSAND expression
                   | expression PIPE expression
                   | expression CARET expression
                   | expression EQEQ expression
                   | expression NOTEQ expression
                   | expression LT expression
                   | expression GT expression
                   | expression LTEQ expression
                   | expression GTEQ expression
                   | expression AND expression
                   | expression OR expression
        """
        p[0] = NodeBinaryOp(p[2], p[1], p[3])

    def p_expression_assignment(self, p):
        """
        expression : id_access EQUAL expression
                   | id_access PLUSEQ expression
                   | id_access MINUSEQ expression
                   | id_access STAREQ expression
                   | id_access SLASHEQ expression
                   | id_access PERCENTEQ expression
                   | id_access SHIFTLEQ expression
                   | id_access SHIFTREQ expression
                   | id_access AMPERSANDEQ expression
                   | id_access PIPEEQ expression
                   | id_access CARETEQ expression
                   | id_access TILDEEQ expression
        """
        if isinstance(p[1], NodeIDAccess):
            p[0] = NodeAssignmentOp(p[2], p[1], p[3])
        elif isinstance(p[1], NodeArrayAccess):
            p[0] = NodeArrayAssignmentOp(p[2], p[1], p[3])
        elif isinstance(p[1], NodeFieldAccess):
            p[0] = NodeFieldAssignmentOp(p[2], p[1], p[3])
        elif isinstance(p[1], NodeNamespaceAccess):
            p[0] = NodeNamespaceAssignmentOp(p[2], p[1], p[3])

    def p_expression_cast(self, p):
        """
        expression : expression AS type
        """
        p[0] = NodeCast(p[1], p[3])

    def p_expression_group(self, p):
        """
        expression : LPAR expression RPAR
        """
        p[0] = NodeGroupOp(p[2])

    def p_declaration_variable(self, p):
        """
        declaration : prefix ID COLON type
                    | prefix ID COLON type EQUAL initializer
        """
        if len(p) == 5:
            p[0] = NodeVariableDeclaration(p[1], p[2], p[4], None)
        else:
            p[0] = NodeVariableDeclaration(p[1], p[2], p[4], p[6])

    def p_codeblock(self, p):
        """
        codeblock : LBRACE statement_list_opt RBRACE
        """
        p[0] = NodeCodeBlock(p[2])

    def p_conditional_structure(self, p):
        """
        conditional_structure : if
                              | if elif_list
                              | if else
                              | if elif_list else
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            if isinstance(p[2], NodeElse):
                p[0] = NodeCondition(p[1], None, p[2])
            else:
                p[0] = NodeCondition(p[1], p[2], None)
        else:
            p[0] = NodeCondition(p[1], p[2], p[3])

    def p_loop_structure(self, p):
        """
        loop_structure : FOREVER codeblock
                       | WHILE expression codeblock
                       | UNTIL expression codeblock
        """
        if len(p) == 3:
            p[0] = NodeLoopForever(p[2])
        else:
            if p[1] == KW_WHILE:
                p[0] = NodeLoopWhile(p[2], p[3])
            else:
                p[0] = NodeLoopUntil(p[2], p[3])

    def p_loop_structure_for(self, p):
        """
        loop_structure : FOR declaration SEMI expression SEMI expression codeblock
        """
        p[0] = NodeLoopFor(p[2], p[4], p[6], p[7])

    def p_flow_control_break(self, p):
        """
        flow_control : BREAK
        """
        p[0] = NodeBreak()

    def p_flow_control_continue(self, p):
        """
        flow_control : CONTINUE
        """
        p[0] = NodeContinue()

    def p_flow_control_return(self, p):
        """
        flow_control : RETURN
                     | RETURN expression
        """
        p[0] = NodeReturn(p[2] if len(p) == 3 else None)

    def p_function_definition_notype(self, p):
        """
        function_definition : FUNC ID LPAR RPAR codeblock
                            | FUNC ID LPAR declaration_list RPAR codeblock
        """
        if len(p) == 6:
            p[0] = NodeFunctionDefinition(p[2], [], None, p[5])
        else:
            p[0] = NodeFunctionDefinition(p[2], p[4], None, p[6])

    def p_function_definition_type(self, p):
        """
        function_definition : FUNC ID LPAR RPAR ARROW type codeblock
                            | FUNC ID LPAR declaration_list RPAR ARROW type codeblock
        """
        if len(p) == 8:
            p[0] = NodeFunctionDefinition(p[2], [], p[6], p[7])
        else:
            p[0] = NodeFunctionDefinition(p[2], p[4], p[7], p[8])

    def p_structure_definition(self, p):
        """
        structure_definition : STRUCT ID structure_body
        """
        p[0] = NodeStructureDefinition(p[2], p[3])

    def p_namespace_definition(self, p):
        """
        namespace_definition : NAMESPACE ID namespace_body
        """
        p[0] = NodeNamespaceDefinition(p[2], p[3])

    def p_inline_c(self, p):
        """
        inline : C expression
        """
        p[0] = NodeInlineC(p[2])

    def p_declaration_extern(self, p):
        """
        extern_declaration : EXTERN declaration
        """
        p[0] = NodeExternDeclaration(p[2])

    def p_declaration_extern_function(self, p):
        """
        extern_declaration : EXTERN function_definition
        """
        p[0] = NodeExternDeclaration(p[2])

    def p_type_definition_alias(self, p):
        """
        type_definition : TYPE ID EQUAL type
        """
        p[0] = NodeTypeAlias(p[2], p[4])

    def p_type_definition_new(self, p):
        """
        type_definition : NEWTYPE ID EQUAL STRING
        """
        p[0] = NodeNewType(p[2], p[4])

    def p_id_access(self, p):
        """
        id_access : ID
                  | id_access DOT id_access
                  | id_access COLONS id_access
                  | ID LSQB expression RSQB
        """
        if len(p) == 2:
            p[0] = NodeIDAccess(p[1])
        elif len(p) == 4:
            if p[2] == SYM_DOT:
                p[0] = NodeFieldAccess(p[1], p[3])
            elif p[2] == SYM_COLON_BLOCK:
                p[0] = NodeNamespaceAccess(p[1], p[3])
        else:
            p[0] = NodeArrayAccess(p[1], p[3])

    def p_prefix(self, p):
        """
        prefix : VAR
               | CONST
        """
        p[0] = p[1]

    def p_type(self, p):
        """
        type : id_access
             | dereferences id_access
             | id_access COLONS id_access
             | LSQB expression RSQB id_access
        """
        if len(p) == 2:
            p[0] = NodeType(p[1])
        elif len(p) == 3:
            p[0] = NodeDereferenceType(p[2], len(p[1]))
        elif len(p) == 4:
            p[0] = NodeNamespaceType(p[1], p[3])
        elif len(p) == 5:
            p[0] = NodeArrayType(p[4], p[2])

    def p_initializer(self, p):
        """
        initializer : expression
                    | expression_list
        """
        p[0] = p[1]

    def p_expression_list(self, p):
        """
        expression_list : expression
                        | expression COMMA expression_list
        """
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_declaration_list(self, p):
        """
        declaration_list : declaration
                         | declaration COMMA declaration_list
        """
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_dereferences(self, p):
        """
        dereferences : STAR
                     | STAR dereferences
        """
        p[0] = p[1] if len(p) == 2 else p[1] + p[2]

    def p_if(self, p):
        """
        if : IF expression codeblock
        """
        p[0] = NodeIf(p[2], p[3])

    def p_elif_list(self, p):
        """
        elif_list : elif
                  | elif elif_list
        """
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    def p_elif(self, p):
        """
        elif : ELIF expression codeblock
        """
        p[0] = NodeElif(p[2], p[3])

    def p_else(self, p):
        """
        else : ELSE codeblock
        """
        p[0] = NodeElse(p[2])

    def p_structure_body(self, p):
        """
        structure_body : LBRACE statement_list_opt RBRACE
        """
        p[0] = NodeStructureBody(p[2])

    def p_namespace_body(self, p):
        """
        namespace_body : LBRACE statement_list_opt RBRACE
        """
        p[0] = NodeNamespaceBody(p[2])

    def p_error(self, p) -> None:
        if not p:
            ShardError_EOF().display()
            return

        source = p.lexer.lexdata
        pos = p.lexpos  

        lineno = p.lexer.lineno
        start = source.rfind("\n", 0, pos) + 1
        end = source.find("\n", pos)
        if end == -1:
            end = len(source)

        line_text = source[start:end]
        col = pos - start

        caret = " " * col + "^"

        text = (
            f"\n{line_text}\n"
            f"{caret}"
        )

        ShardError_BadSyntax(text, p.lexer.lineno).display()

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, debug=False, write_tables=False, **kwargs)

    def parse_code(self, code: str):
        ast = self.parser.parse(code)
        return ast