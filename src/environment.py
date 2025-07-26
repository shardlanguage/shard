# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains the shardc environment, where the code is executed
# and the temporary data is stored.
# =====================================================================

# Import modules
from tree import *
from utils.symbols import *
from utils.codegen import *

# Environment class
class Environment:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.generated_functions = []
        self.generated_main = []

    # Evaluate <node> node
    def evaluate(self, node):
        if isinstance(node, Value):
            return generate_value(node.value)

        elif isinstance(node, VariableAccess):
            if self.symbol_table.find_variable(node.name):
                return generate_id(node.name)
            else:
                raise NameError(f"Cannot access to undeclared variable \"{node.name}\"")

        elif isinstance(node, ArrayAccess):
            if self.symbol_table.find_variable(node.name):
                index = self.evaluate(node.index)
                size = self.symbol_table.get_size(node.name)
                if isinstance(index, int) and index >= int(size):
                    raise IndexError("Array index out of range")
                return generate_array_access(node.name, index)
            else:
                raise NameError(f"Cannot access to undeclared array \"{node.name}\"")

        elif isinstance(node, FunctionCall):
            if self.symbol_table.find_function(node.name):
                args = [self.evaluate(param) for param in node.parameters]
                return generate_function_call(node.name, args)
            else:
                raise NameError(f"Call to undeclared function \"{node.name}\"")

        elif isinstance(node, UnaryOp):
            right = self.evaluate(node.right)
            return generate_UnOp(node.operator, right)

        elif isinstance(node, BinaryOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            return generate_BinOp(left, node.operator, right)

        elif isinstance(node, VariableAssignment):
            if self.symbol_table.find_variable(node.name):
                value = self.evaluate(node.value)
                return generate_AssignOp(self.symbol_table, node.name, node.operator, value)
            else:
                raise NameError(f"Assignment operation on undeclared variable \"{node.name}\"")

        elif isinstance(node, ArrayAssignment):
            if self.symbol_table.find_variable(node.name):
                index = self.evaluate(node.index)
                value = self.evaluate(node.value)
                size = self.symbol_table.get_size(node.name)
                if isinstance(index, int) and index >= int(size):
                    raise IndexError("Array index out of range")
                return generate_ArrayAssignOp(self.symbol_table, node.name, index, node.operator, value)
            else:
                raise NameError(f"Assignment operation on undeclared array \"{node.name}\"")

        elif isinstance(node, Group):
            group = self.evaluate(node.group)
            return generate_group(group)

        elif isinstance(node, VariableDeclaration):
            if not self.symbol_table.find_variable(node.name):
                value = 0
                if node.value is not None:
                    value = self.evaluate(node.value)
                is_const = (node.type_modifier == "const") if node.type_modifier else False
                var = Variable(node.primary_type, node.name, value, is_const)
                self.symbol_table.add_variable(var)
                return generate_variable_declaration(self.symbol_table, node.type_modifier, node.primary_type, node.name, value)
            else:
                raise NameError(f"Redeclaration of variable \"{node.name}\"")

        elif isinstance(node, ArrayDeclaration):
            if not self.symbol_table.find_variable(node.name):
                size = self.evaluate(node.size)
                content = []
                if node.content is not None:
                    for value_node in node.content:
                        content.append(self.evaluate(value_node))
                if len(content) > int(size):
                    raise IndexError(f"Array content exceeds declared size")
                is_const = (node.type_modifier == "const") if node.type_modifier else False
                var = Variable(node.primary_type, node.name, size, is_const)
                self.symbol_table.add_variable(var)
                return generate_array_declaration(self.symbol_table, node.type_modifier, node.primary_type, node.name, size, content)
            else:
                raise NameError(f"Redeclaration of array \"{node.name}\"")

        elif isinstance(node, CodeBlock):
            local_env = Environment()
            local_env.symbol_table = SymbolTable(parent=self.symbol_table)
            block_stmts = [local_env.evaluate(stmt) for stmt in node.statement_list]
            return generate_codeblock(block_stmts)

        elif isinstance(node, Condition):
            condition = self.evaluate(node.condition)
            if_branch = [self.evaluate(stmt) for stmt in node.if_branch.statement_list]
            else_branch = [self.evaluate(stmt) for stmt in node.else_branch.statement_list] if node.else_branch else []
            return generate_condition(condition, if_branch, else_branch)

        elif isinstance(node, LoopUnconditionnal):
            stmts = [self.evaluate(stmt) for stmt in node.statement_list.statement_list]
            return generate_loop_unconditionnal(stmts)

        elif isinstance(node, LoopConditionnal):
            condition = self.evaluate(node.condition)
            branch = [self.evaluate(stmt) for stmt in node.branch.statement_list]
            return generate_LoopCondition(node.looptype, condition, branch)

        elif isinstance(node, FlowControl):
            value = self.evaluate(node.value) if node.value is not None else None
            return generate_flow_control(node.statement, value)

        elif isinstance(node, FunctionDefinition):
            if self.symbol_table.find_function(node.name):
                raise NameError(f"Function \"{node.name}\" defined twice")

            fn = Function(node.datatype, node.name, node.parameters, node.body)
            self.symbol_table.add_function(fn)

            local_env = Environment()
            local_env.symbol_table = SymbolTable(parent=self.symbol_table)

            type_map = {
                'byte': 'int8_t', 'ubyte': 'uint8_t',
                'word': 'int16_t', 'uword': 'uint16_t',
                'dword': 'int32_t', 'udword': 'uint32_t',
                'qword': 'int64_t', 'uqword': 'uint64_t',
                'float': 'float', 'double': 'double'
            }

            param_decls = []
            for type_, name in node.parameters:
                var = Variable(type_, name, None, False)
                local_env.symbol_table.add_variable(var)

                if type_ not in type_map:
                    raise ValueError(f"Unknown type {type_} for parameter {name}")

                param_decls.append(f"{type_map[type_]} {name}")

            body_stmts = [local_env.evaluate(stmt) for stmt in node.body.statement_list]

            fn_code = generate_function_definition(node.datatype, node.name, param_decls, body_stmts)
            self.generated_functions.append(fn_code)
            return ""

        else:
            raise RuntimeError(f"Unknown node type \"{type(node)}\"")

    # Compile an AST
    def compile_ast(self, ast):
        code = []

        code.append("""
/*
    ===============================================================
    This program has been generated by the shardc compiler.

    DO NOT EDIT except if you work on a shardc fork or if
    the generated source code below is not correct.

    -- shardc - released under MIT License
    https://github.com/shardlanguage/shard
    ===============================================================
*/
""")

        code.append("#include <stdint.h>\n")

        if ast is not None:
            for node in ast:
                if isinstance(node, FunctionDefinition):
                    self.evaluate(node)

        code.extend(self.generated_functions)

        if ast is not None:
            for node in ast:
                if not isinstance(node, FunctionDefinition):
                    code_snippet = self.evaluate(node)
                    if code_snippet:
                        code.append(f"{code_snippet};\n")

        self.generated_main = code

        return self.generated_main