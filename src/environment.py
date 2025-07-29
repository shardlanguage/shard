# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains the shardc environment, where the code is executed
# and the temporary data is stored.
# =====================================================================

# Import modules
import os

from parser import parser
from tree import *
from utils.symbols import *
from utils.codegen import *
from utils.conversion import type_map

# Environment class
class Environment:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.generated_functions = []
        self.generated_main = []

    # Evaluate <node> node
    def evaluate(self, node):
        global type_map

        if isinstance(node, Value):
            return generate_value(node.value)

        elif isinstance(node, String):
            return generate_string(node.string)

        elif isinstance(node, VariableAccess):
            if self.symbol_table.find_variable(node.name):
                return generate_id(node.name)
            else:
                raise NameError(f"Cannot access to undeclarated variable \"{node.name}\"")

        elif isinstance(node, ArrayAccess):
            if self.symbol_table.find_variable(node.name):
                index = self.evaluate(node.index)
                size = self.symbol_table.get_size(node.name)
                if isinstance(index, int) and index >= int(size):
                    raise IndexError("Array index out of range")
                return generate_array_access(node.name, index)
            else:
                raise NameError(f"Cannot access to undeclarated array \"{node.name}\"")

        elif isinstance(node, StructInstanceFieldAccess):
            if self.symbol_table.find_variable(node.instance):
                return generate_struct_instance_field_access(node.instance, node.field)
            else:
                raise NameError(f"Cannot access to undeclarated variable \"{node.instance}\"")

        elif isinstance(node, FunctionCall):
            if self.symbol_table.find_function(node.name):
                args = [self.evaluate(param) for param in node.parameters]
                return generate_function_call(node.name, args)
            else:
                raise NameError(f"Call to undeclarated function \"{node.name}\"")

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
                raise NameError(f"Assignment operation on undeclarated variable \"{node.name}\"")

        elif isinstance(node, ArrayAssignment):
            if self.symbol_table.find_variable(node.name):
                index = self.evaluate(node.index)
                value = self.evaluate(node.value)
                size = self.symbol_table.get_size(node.name)
                if isinstance(index, int) and index >= int(size):
                    raise IndexError("Array index out of range")
                return generate_ArrayAssignOp(self.symbol_table, node.name, index, node.operator, value)
            else:
                raise NameError(f"Assignment operation on undeclarated array \"{node.name}\"")

        elif isinstance(node, StructInstanceFieldAssignment):
            if self.symbol_table.find_variable(node.instance):
                value = self.evaluate(node.value)
                return generate_StructInstanceFieldAssignOp(self.symbol_table, node.instance, node.field, node.operator, value)

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
                return generate_variable_declaration(node.type_modifier, node.primary_type, node.name, value)
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
                    raise IndexError(f"Array content exceeds declarated size")
                is_const = (node.type_modifier == "const") if node.type_modifier else False
                var = Variable(node.primary_type, node.name, size, is_const)
                self.symbol_table.add_variable(var)
                return generate_array_declaration(node.type_modifier, node.primary_type, node.name, size, content)
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

            param_decls = []
            for param in node.parameters:
                if len(param) == 2:
                    datatype, name = param
                    size = None
                elif len(param) == 3:
                    datatype, name, size = param
                else:
                    raise ValueError(f"Invalid parameter declaration: {param}")

                if isinstance(datatype, (list, tuple)) and len(datatype) == 2:
                    modifier, primary_type = datatype
                else:
                    modifier = None
                    primary_type = datatype

                if primary_type not in type_map:
                    raise ValueError(f"Unknown type {primary_type} for parameter {name}")

                type_str = ''
                if modifier == 'const':
                    type_str += 'const '

                type_str += type_map[primary_type]

                evaluated_size = None
                if size is not None:
                    evaluated_size = self.evaluate(size)
                if evaluated_size is not None:
                    param_decls.append(f"{type_str} {name}[{evaluated_size}]")
                else:
                    param_decls.append(f"{type_str} {name}")

                var = Variable(datatype, name, None, False)
                local_env.symbol_table.add_variable(var)

            body_stmts = [local_env.evaluate(stmt) for stmt in node.body.statement_list]

            fn_code = generate_function_definition(node.datatype, node.name, param_decls, body_stmts)
            self.generated_functions.append(fn_code)
            return ""

        elif isinstance(node, StructureDefinition):
            if self.symbol_table.find_structure(node.name):
                raise NameError(f"Structure \"{node.name}\" already defined")

            processed_fields = []
            for field in node.fields:
                if len(field) == 2:
                    datatype, var_name = field
                    size = None
                elif len(field) == 3:
                    datatype, var_name, size = field
                else:
                    raise ValueError(f"Invalid field declaration: {field}")

                if isinstance(datatype, (list, tuple)) and len(datatype) == 2:
                    modifier, primary_type = datatype
                else:
                    modifier = None
                    primary_type = datatype

                if primary_type not in type_map:
                    raise ValueError(f"Unknown type: {primary_type}")

                type_str = ''
                if modifier == 'const':
                    type_str += 'const '
                type_str += type_map[primary_type]

                evaluated_size = self.evaluate(size)

                processed_fields.append((type_str, var_name) if size is None else (type_str, var_name, evaluated_size))

            type_map[node.name] = f"struct {node.name}"

            struct = Structure(node.name, processed_fields)
            self.symbol_table.add_structure(struct)

            return generate_struct_definition(node.name, processed_fields)

        elif isinstance(node, InlineC):
            return generate_inline_c(node.code)

        elif node is None:
            return ""

        else:
            raise ValueError(f"Unknow node: {node}")

    # Compile an AST
    def compile_ast(self, ast):
        code = []

        code.append("""/*
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
        code.append("#include <stdio.h>\n")

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

        if "main" not in self.symbol_table.functions:
            raise NameError("main() not defined")

        self.generated_main = code

        return self.generated_main