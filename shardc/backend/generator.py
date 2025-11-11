from typing import Any
from shardc.backend.codegen.lang import ProgrammingLanguage
from shardc.backend.visitor import Visitor
from shardc.frontend.tree.codeblocks import NodeCodeBlock, NodeStructureBody
from shardc.frontend.tree.condition_struct import NodeCondition, NodeElif, NodeElse, NodeIf
from shardc.frontend.tree.declarations import NodeExternDeclaration, NodeVariableDeclaration
from shardc.frontend.tree.flow_control import NodeBreak, NodeContinue, NodeReturn
from shardc.frontend.tree.function_def import NodeFunctionDefinition
from shardc.frontend.tree.inline import NodeInlineC
from shardc.frontend.tree.loop_struct import NodeLoopForever, NodeLoopUntil, NodeLoopWhile
from shardc.frontend.tree.node import Node
from shardc.frontend.tree.expressions import NodeArrayAccess, NodeArrayAssignmentOp, NodeAssignmentOp, NodeBinaryOp, NodeCast, NodeFieldAccess, NodeFieldAssignmentOp, NodeFunctionCall, NodeGroupOp, NodeIDAccess, NodeNumber, NodeString, NodeUnaryOp
from shardc.frontend.tree.structure_def import NodeStructureDefinition
from shardc.frontend.tree.types import Node, NodeDereferenceType, NodeNewType, NodeTypeAlias
from shardc.utils.constants.operators import OP_BITWISE_AND, OP_BITWISE_NOT, OP_BITWISE_OR, OP_BITWISE_XOR, OP_DIVIDE, OP_GREATER_THAN, OP_GREATER_THAN_OR_EQUAL, OP_ISEQUAL, OP_ISNOTEQUAL, OP_LESSER_THAN, OP_LESSER_THAN_OR_EQUAL, OP_LOGICAL_AND, OP_LOGICAL_NOT, OP_LOGICAL_OR, OP_MINUS, OP_MODULO, OP_PLUS, OP_REFERENCE, OP_SET, OP_SET_ADD, OP_SET_AND, OP_SET_DIV, OP_SET_MOD, OP_SET_MUL, OP_SET_NOT, OP_SET_OR, OP_SET_SHL, OP_SET_SHR, OP_SET_SUB, OP_SET_XOR, OP_SHIFT_LEFT, OP_SHIFT_RIGHT, OP_SIZEOF, OP_TIMES
from shardc.utils.constants.prefixes import C_CONST, C_VAR, S_CONST, S_VAR

class CodeGenerator(Visitor):
    def __init__(self, lang: ProgrammingLanguage):
        self.lang = lang
        self.main_function = "__main__"
        self.main_function_params = []
        super().__init__("generate")

    def generate(self, node: Node, statement: bool=False) -> Any:
        code = node.accept(self) if node is not None else ""
        if statement:
            return f"{code}{self.lang.end_marker}"
        return code

    def generate_NodeNumber(self, node: NodeNumber) -> str:
        return str(node.value)

    def generate_NodeString(self, node: NodeString) -> str:
        return self.lang.string(node.value)

    def generate_NodeIDAccess(self, node: NodeIDAccess) -> str:
        return node.name

    def generate_NodeArrayAccess(self, node: NodeArrayAccess) -> str:
        index = node.index.accept(self)

        return self.lang.access_array(node.name, index)

    def generate_NodeFieldAccess(self, node: NodeFieldAccess) -> str:
        instance = node.instance.accept(self)
        field = node.field.accept(self)

        return self.lang.access_structure_field(instance, field)
        
    def generate_NodeFunctionCall(self, node: NodeFunctionCall) -> str:
        parameters = []
        if len(node.parameters) != 0:
            for param in node.parameters:
                parameters.append(param.accept(self))

        return self.lang.call_function(node.name, parameters)

    def generate_NodeUnaryOp(self, node: NodeUnaryOp) -> str:
        right = node.right.accept(self)

        table = {
            OP_PLUS: self.lang.positive,
            OP_MINUS: self.lang.negative,
            OP_BITWISE_NOT: self.lang.bitwise_not,
            OP_LOGICAL_NOT: self.lang.logical_not,
            OP_REFERENCE: self.lang.reference,
            OP_SIZEOF: self.lang.sizeof
        }

        return table[node.op](right)

    def generate_NodeBinaryOp(self, node: NodeBinaryOp) -> str:
        left = node.left.accept(self)
        right = node.right.accept(self)

        table = {
            OP_PLUS: self.lang.add,
            OP_MINUS: self.lang.substract,
            OP_TIMES: self.lang.multiply,
            OP_DIVIDE: self.lang.divide,
            OP_MODULO: self.lang.modulo,
            OP_SHIFT_LEFT: self.lang.shift_left,
            OP_SHIFT_RIGHT: self.lang.shift_right,
            OP_BITWISE_AND: self.lang.bitwise_and,
            OP_BITWISE_OR: self.lang.bitwise_or,
            OP_BITWISE_XOR: self.lang.bitwise_xor,
            OP_ISEQUAL: self.lang.is_equal,
            OP_ISNOTEQUAL: self.lang.is_not_equal,
            OP_LESSER_THAN: self.lang.is_lesser_than,
            OP_GREATER_THAN: self.lang.is_greater_than,
            OP_LESSER_THAN_OR_EQUAL: self.lang.is_lesser_than_or_equal,
            OP_GREATER_THAN_OR_EQUAL: self.lang.is_greater_than_or_equal,
            OP_LOGICAL_AND: self.lang.logical_and,
            OP_LOGICAL_OR: self.lang.logical_or
        }

        return table[node.op](left, right)

    def generate_NodeAssignmentOp(self, node: NodeAssignmentOp) -> str:
        value = node.value.accept(self)
        
        table = {
            OP_SET: self.lang.assign_equal,
            OP_SET_ADD: self.lang.assign_add,
            OP_SET_SUB: self.lang.assign_substract,
            OP_SET_MUL: self.lang.assign_times,
            OP_SET_DIV: self.lang.assign_divide,
            OP_SET_MOD: self.lang.assign_modulo,
            OP_SET_SHL: self.lang.assign_shift_left,
            OP_SET_SHR: self.lang.assign_shift_right,
            OP_SET_AND: self.lang.assign_and,
            OP_SET_OR: self.lang.assign_or,
            OP_SET_XOR: self.lang.assign_xor,
            OP_SET_NOT: self.lang.assign_not
        }

        return table[node.op](node.name, value)

    def generate_NodeArrayAssignmentOp(self, node: NodeArrayAssignmentOp) -> str:
        value = node.value.accept(self)
        index = node.index.accept(self)
        
        table = {
            OP_SET: self.lang.assign_equal_array,
            OP_SET_ADD: self.lang.assign_add_array,
            OP_SET_SUB: self.lang.assign_substract_array,
            OP_SET_MUL: self.lang.assign_times_array,
            OP_SET_DIV: self.lang.assign_divide_array,
            OP_SET_MOD: self.lang.assign_modulo_array,
            OP_SET_SHL: self.lang.assign_shift_left_array,
            OP_SET_SHR: self.lang.assign_shift_right_array,
            OP_SET_AND: self.lang.assign_and_array,
            OP_SET_OR: self.lang.assign_or_array,
            OP_SET_XOR: self.lang.assign_xor_array,
            OP_SET_NOT: self.lang.assign_not_array
        }

        return table[node.op](node.name, index, value)

    def generate_NodeFieldAssignmentOp(self, node: NodeFieldAssignmentOp) -> str:
        value = node.value.accept(self)
        field = node.field.accept(self)
        
        table = {
            OP_SET: self.lang.assign_equal_field,
            OP_SET_ADD: self.lang.assign_add_field,
            OP_SET_SUB: self.lang.assign_substract_field,
            OP_SET_MUL: self.lang.assign_times_field,
            OP_SET_DIV: self.lang.assign_divide_field,
            OP_SET_MOD: self.lang.assign_modulo_field,
            OP_SET_SHL: self.lang.assign_shift_left_field,
            OP_SET_SHR: self.lang.assign_shift_right_field,
            OP_SET_AND: self.lang.assign_and_field,
            OP_SET_OR: self.lang.assign_or_field,
            OP_SET_XOR: self.lang.assign_xor_field,
            OP_SET_NOT: self.lang.assign_not_field
        }

        name = ""
        if isinstance(node.instance, NodeArrayAccess):
            instance_name = node.instance.accept(self)
        else:
            instance_name = node.symbol.name if node.symbol is not None else node.instance
        name = instance_name

        return table[node.op](name, field, value)

    def generate_NodeCast(self, node: NodeCast) -> str:
        value = node.value.accept(self)

        if node.shardt is not None:
            t = node.shardt.c
        else:
            t = node.t

        return self.lang.cast(value, t)

    def generate_NodeGroupOp(self, node: NodeGroupOp) -> str:
        group = node.group.accept(self)
        return self.lang.group(group)

    def generate_NodeVariableDeclaration(self, node: NodeVariableDeclaration) -> str:
        values = []
        value = None
        if isinstance(node.value, list):
            for v in node.value:
                values.append(v.accept(self))
        else:
            value = node.value.accept(self) if node.value is not None else None

        prefixes = {
            S_VAR: C_VAR,
            S_CONST: C_CONST
        }

        prefix = prefixes[node.prefix]
        name = node.symbol.name if node.symbol is not None else node.name
        t = node.shardt.c if node.shardt is not None else node.t

        if len(values) == 0:
            if isinstance(node.t, NodeDereferenceType):
                if value is None:
                    return self.lang.declare_empty_pointer(prefix, node.t.nderefs, name, t)
                return self.lang.declare_pointer(prefix, node.t.nderefs, name, t, value)
            if value is None:
                return self.lang.declare_empty_variable(prefix, name, t)
            return self.lang.declare_variable(prefix, name, t, value)
        else:
            length = 0
            if node.shardt is not None:
                if isinstance(node.shardt.length, Node):
                    length = node.shardt.length.accept(self)
            if value is None:
                return self.lang.declare_empty_array(prefix, name, t, length)
            return self.lang.declare_array(prefix, name, t, length, values)

    def generate_NodeCodeBlock(self, node: NodeCodeBlock) -> str:
        content = []
        for stmt in node.content:
            if stmt is not None:
                content.append(stmt.accept(self))

        return self.lang.codeblock(content)

    def generate_NodeStructureBody(self, node: NodeStructureBody) -> str:
        content = []
        for stmt in node.content:
            if stmt is not None:
                content.append(stmt.accept(self))

        return self.lang.codeblock(content)

    def generate_NodeExternDeclaration(self, node: NodeExternDeclaration) -> str:
        symbol = node.symbol.accept(self)

        return self.lang.declare_extern_symbol(symbol)

    def generate_NodeIf(self, node: NodeIf) -> str:
        condition = node.condition.accept(self)
        branch = node.branch.accept(self)
        return self.lang.conditional_if(condition, branch)

    def generate_NodeElif(self, node: NodeElif) -> str:
        condition = node.condition.accept(self)
        branch = node.branch.accept(self)
        return self.lang.conditional_else_if(condition, branch)

    def generate_NodeElse(self, node: NodeElse) -> str:
        branch = node.branch.accept(self)
        return self.lang.conditional_else(branch)

    def generate_NodeCondition(self, node: NodeCondition) -> str:
        elifs = []
        else_ = ""
        code = ""

        if_ = node.if_.accept(self)
        if node.elif_ is not None:
            for elseif in node.elif_:
                elifs.append(elseif.accept(self))
        if node.else_ is not None:
            else_ = node.else_.accept(self)

        if if_ is not None:
            code = if_ + ''.join([' ' + elseif for elseif in elifs]) + ' ' + else_
        return code

    def generate_NodeLoopForever(self, node: NodeLoopForever) -> str:
        branch = node.branch.accept(self)
        return self.lang.infinite_loop(branch)

    def generate_NodeLoopWhile(self, node: NodeLoopWhile) -> str:
        condition = node.condition.accept(self)
        branch = node.branch.accept(self)
        return self.lang.while_loop(condition, branch)

    def generate_NodeLoopUntil(self, node: NodeLoopUntil) -> str:
        condition = node.condition.accept(self)
        branch = node.branch.accept(self)
        return self.lang.until_loop(condition, branch)

    def generate_NodeBreak(self, node: NodeBreak) -> str:
        return self.lang.break_loop()

    def generate_NodeContinue(self, node: NodeContinue) -> str:
        return self.lang.continue_loop()

    def generate_NodeReturn(self, node: NodeReturn) -> str:
        value = None
        if node.value is not None:
            value = node.value.accept(self)

        if value is not None:
            return self.lang.return_function(value)
        else:
            return self.lang.return_function_empty()

    def generate_NodeFunctionDefinition(self, node: NodeFunctionDefinition) -> str:
        parameters = []
        if len(node.parameters) != 0:
            for param in node.parameters:
                parameters.append(param.accept(self))

        name = node.symbol.name if node.symbol is not None else node.name
        t = node.shardt.c if node.shardt is not None else node.t

        if node.name == "main":
            name = "__main__"
            self.main_function = "__main__"
            self.main_function_params = parameters

        body = node.body.accept(self)

        return self.lang.define_function(t, name, parameters, body)

    def generate_NodeStructureDefinition(self, node: NodeStructureDefinition) -> str:
        body = node.body.accept(self)
        
        name = node.symbol.name if node.symbol is not None else node.name

        return self.lang.define_structure(name, body)

    def generate_NodeInlineC(self, node: NodeInlineC) -> str:
        code = node.code.value.replace('\\"', '"')

        return self.lang.inline(code)

    def generate_NodeTypeAlias(self, node: NodeTypeAlias) -> str:
        return ""

    def generate_NodeNewType(self, node: NodeNewType) -> str:
        return ""