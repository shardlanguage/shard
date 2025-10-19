import functools
from shardc.backend.codegen.architecure import Architecture
from shardc.frontend.nodes.declaration import NodeVariableDecl
from shardc.frontend.nodes.expression import NodeAssignOp, NodeBinaryOp, NodeGroup, NodeID, NodeUnaryOp, NodeValue
from shardc.frontend.symbols.variable import ShardVariable
from shardc.utils.const.comparisons import EQUAL, GT_SIGNED, GT_UNSIGNED, GTQ_SIGNED, GTQ_UNSIGNED, LT_SIGNED, LT_UNSIGNED, LTQ_SIGNED, LTQ_UNSIGNED, NOT_EQUAL
from shardc.utils.const.types import INT
from shardc.utils.errors.symbols import ShardError_UninitializedConstant

class CodeGenerator:
    def __init__(self, arch: Architecture):
        self.output = ""
        self.arch = arch

    def generate(self, node) -> str:
        node.accept(self)
        text = '\n'.join(self.arch.section_text)
        rodata = '\n'.join(self.arch.section_rodata)
        data = '\n'.join(self.arch.section_data)
        bss = '\n'.join(self.arch.section_bss)
        program = (
            self.arch.section("text") + text +
            self.arch.section("rodata") + rodata +
            self.arch.section("data") + data +
            self.arch.section("bss") + bss
        )
        self.output = program
        return program

    def generic_visit(self, node) -> None:
        pass

    def visit_NodeValue(self, node: NodeValue) -> None:
        if node.t == INT: self.arch.integer(node.value)

    def visit_NodeID(self, node: NodeID) -> None:
        self.arch.access_value(node.name)

    def visit_NodeUnaryOp(self, node: NodeUnaryOp) -> None:
        node.right.accept(self)
        table = {
            '-': self.arch.signed_value,
            '~': self.arch.bitwise_not
        }
        table[node.op]()

    def visit_NodeBinaryOp(self, node: NodeBinaryOp) -> None:
        node.right.accept(self)
        self.arch.push()
        node.left.accept(self)
        self.arch.pop()

        signed = (isinstance(node.left, NodeID) and isinstance(node.left.symbol, ShardVariable) and node.left.symbol.t.signed) or (isinstance(node.right, NodeID) and isinstance(node.right.symbol, ShardVariable) and node.right.symbol.t.signed)

        table = {
            '+': self.arch.add,
            '-': self.arch.sub,
            '*': self.arch.mul,
            '/': self.arch.div if not signed else self.arch.signed_div,
            '%': self.arch.modulo if not signed else self.arch.signed_modulo,
            '&': self.arch.bitwise_and,
            '|': self.arch.bitwise_or,
            '^': self.arch.bitwise_xor,
            '<<': self.arch.shift_left,
            '>>': self.arch.shift_right if not signed else self.arch.signed_shift_right,
            '==': functools.partial(self.arch.compare, comparison=EQUAL),
            '!=': functools.partial(self.arch.compare, comparison=NOT_EQUAL),
            '<': functools.partial(self.arch.compare, comparison=LT_UNSIGNED if not signed else LT_SIGNED),
            '>': functools.partial(self.arch.compare, comparison=GT_UNSIGNED if not signed else GT_SIGNED),
            '<=': functools.partial(self.arch.compare, comparison=LTQ_UNSIGNED if not signed else LTQ_SIGNED),
            '>=': functools.partial(self.arch.compare, comparison=GTQ_UNSIGNED if not signed else GTQ_SIGNED)
        }

        func = table[node.op]
        func()

    def visit_NodeAssignOp(self, node: NodeAssignOp) -> None:
        self.arch.move_addr(node.name)
        self.arch.push()
        node.val.accept(self)
        self.arch.pop()

        signed = isinstance(node.symbol, ShardVariable) and node.symbol.t.signed

        table = {
            '=': None,
            '+=': self.arch.add,
            '-=': self.arch.sub,
            '*=': self.arch.mul,
            '/=': self.arch.div if not signed else self.arch.signed_div,
            '%=': self.arch.modulo if not signed else self.arch.signed_modulo,
            '<<=': self.arch.shift_left,
            '>>=': self.arch.shift_right if not signed else self.arch.signed_shift_right,
            '&=': self.arch.bitwise_and,
            '|=': self.arch.bitwise_or,
            '^=': self.arch.bitwise_xor,
            '~=': self.arch.bitwise_not
        }

        func = table[node.op]
        if func is not None:
            func()
        self.arch.store_addr(node.name)

    def visit_NodeGroup(self, node: NodeGroup) -> None:
        node.group.accept(self)

    def visit_NodeVariableDecl(self, node: NodeVariableDecl) -> None:
        value = None

        if node.val is not None:
            if isinstance(node.val, NodeValue):
                value = node.val.value
            else:
                value = getattr(node.val, "val", None)

        if node.prefix == "var":
            if value is None:
                self.arch.define_buffer(node.name, node.datatype, 1)
            else:
                self.arch.define_variable(node.name, node.datatype, value)

        elif node.prefix == "const":
            if value is None:
                ShardError_UninitializedConstant(node.name).display()
            else:
                self.arch.define_const(node.name, node.datatype, value)