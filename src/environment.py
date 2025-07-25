from tree import *
from utils.symbols import *
from utils.codegen import *

class Environment:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.generated_code = []

    def evaluate(self, node):
        if isinstance(node, Value):
            return generate_value(node.value)

        elif isinstance(node, VariableAccess):
            if (self.symbol_table.find_symbol(node.name)):
                return generate_id(node.name)
            else:
                raise NameError(f"Cannot access to undeclared variable \"{node.name}\"")

        elif isinstance(node, ArrayAccess):
            if (self.symbol_table.find_symbol(node.name)):
                index = self.evaluate(node.index)
                size = self.symbol_table.get_size(node.name)
                
                if index >= int(size):
                    raise IndexError("Array index out of range")

                return generate_array_access(node.name, index)
            else:
                raise NameError(f"Cannot access to undeclared array \"{node.name}\"")

        elif isinstance(node, UnaryOp):
            right = self.evaluate(node.right)

            return generate_UnOp(node.operator, right)

        elif isinstance(node, BinaryOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            return generate_BinOp(left, node.operator, right)

        elif isinstance(node, VariableAssignment):
            if (self.symbol_table.find_symbol(node.name)):
                value = self.evaluate(node.value)
                return generate_AssignOp(self.symbol_table, node.name, node.operator, value)
            else:
                raise NameError(f"Assignment operation on undeclared variable \"{node.name}\"")

        elif isinstance(node, ArrayAssignment):
            if (self.symbol_table.find_symbol(node.name)):
                index = self.evaluate(node.index)
                value = self.evaluate(node.value)
                size = self.symbol_table.get_size(node.name)

                if index >= int(size):
                    raise IndexError("Array index out of range")

                return generate_ArrayAssignOp(self.symbol_table, node.name, index, node.operator, value)
            else:
                raise NameError(f"Assignment operation on undeclared array \"{node.name}\"")

        elif isinstance(node, Group):
            group = self.evaluate(node.group)

            return generate_group(group)

        elif isinstance(node, VariableDeclaration):
            if (not self.symbol_table.find_symbol(node.name)):
                code = ""

                value = 0
                if node.value is not None:
                    value = self.evaluate(node.value)

                is_const = (node.type_modifier == "const") if node.type_modifier else False
                var = Variable(node.primary_type, node.name, value, is_const)
                self.symbol_table.add_variable(var)

                code += generate_variable_declaration(self.symbol_table, node.type_modifier, node.primary_type, node.name, value)
                return code
            else:
                raise NameError(f"Redeclaration of variable \"{node.name}\"")

        elif isinstance(node, ArrayDeclaration):
            if (not self.symbol_table.find_symbol(node.name)):
                code = ""

                size = self.evaluate(node.size)
                content = []
                if node.content is not None:
                    for value in node.content:
                        content.append(self.evaluate(value))

                if len(content) >= int(size):
                    raise IndexError(f"Array content exceeds size")

                is_const = (node.type_modifier == "const") if node.type_modifier else False
                var = Variable(node.primary_type, node.name, value, is_const)
                self.symbol_table.add_variable(var)

                code += generate_array_declaration(self.symbol_table, node.type_modifier, node.primary_type, node.name, size, content)
                return code
            else:
                raise NameError(f"Redeclaration of array \"{node.name}\"")

        elif isinstance(node, CodeBlock):
            statement_list = []
            for stmt in node.statement_list:
                statement_list.append(self.evaluate(stmt))

            return generate_codeblock(statement_list)

        elif isinstance(node, Condition):
            condition = self.evaluate(node.condition)
            stmt_if = []
            stmt_else = []

            for stmt in node.if_branch.statement_list:
                stmt_if.append(self.evaluate(stmt))
            for stmt in node.else_branch.statement_list:
                stmt_else.append(self.evaluate(stmt))

            return generate_condition(condition, stmt_if, stmt_else)

        elif isinstance(node, LoopUnconditionnal):
            stmt_list = []

            for stmt in node.statement_list.statement_list:
                stmt_list.append(self.evaluate(stmt))

            return generate_loop_unconditionnal(stmt_list)

        elif isinstance(node, LoopConditionnal):
            condition = self.evaluate(node.condition)
            branch = []

            for stmt in node.branch.statement_list:
                branch.append(self.evaluate(stmt))

            return generate_LoopCondition(node.looptype, condition, branch)

        else:
            raise RuntimeError(f"Unknown node \"{node}\"")

    def compile_ast(self, ast):
        code = []

        code.append("""
/*
    ===============================================================
    This program has been generated by the shardc compiler.

    DO NOT EDIT excepted if you are working on a shardc fork or if
    the generated source code below is not correct.

    -- shardc - released under MIT License
    https://github.com/shardlanguage/shard
    ===============================================================
*/
""")

        code.append("#include <stdint.h>\n")

        code.append("int main() {\n")

        if ast is not None:
            for node in ast:
                if node is not None:
                    code.append(f"{self.evaluate(node)};\n")

        code.append("return 0;\n")
        code.append("}")

        self.generated_code = code

        return self.generated_code