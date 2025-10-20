import functools
from shardc.backend.codegen.architecure import Architecture
from shardc.frontend.nodes.declaration import NodeVariableDecl
from shardc.frontend.nodes.expression import NodeAssignOp, NodeBinaryOp, NodeGroup, NodeID, NodeUnaryOp, NodeValue, NodeExpressionList
from shardc.frontend.symbols.variable import ShardVariable
from shardc.utils.const.comparisons import EQUAL, GT_SIGNED, GT_UNSIGNED, GTQ_SIGNED, GTQ_UNSIGNED, LT_SIGNED, LT_UNSIGNED, LTQ_SIGNED, LTQ_UNSIGNED, NOT_EQUAL
from shardc.utils.const.operators import BITWISE_AND, BITWISE_NOT, BITWISE_OR, BITWISE_XOR, DIVIDE, EQUALS, GREATER_THAN, GT_EQUAL, LESSER_THAN, LSHIFT, LT_EQUAL, MINUS, MODULO, NOTEQUALS, PLUS, RSHIFT, SET, SET_BITWISE_AND, SET_BITWISE_NOT, SET_BITWISE_OR, SET_BITWISE_XOR, SET_DIVIDE, SET_LSHIFT, SET_MINUS, SET_MODULO, SET_PLUS, SET_RSHIFT, SET_TIMES, TIMES
from shardc.utils.const.prefix import CONST, VAR
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

    def visit_NodeID(self, node: NodeID):
        if node.idx is None:
            self.arch.access_value(node.name)
            return

        if isinstance(node.idx, NodeValue):
            idx_val = node.idx.value
            if node.symbol is not None:
                if isinstance(node.symbol.t, tuple):
                    base_type, _ = node.symbol.t
                else:
                    base_type = node.symbol.t
                element_size = base_type.size // 8
            else:
                element_size = 1
            offset = int(idx_val) * element_size
            addr = self.arch.addr_offset(node.name, offset)
            self.arch.access_value(addr)

        elif isinstance(node.idx, NodeID):
            node.idx.accept(self)
            self.arch.push()
            element_size = 1
            if node.symbol is not None:
                if isinstance(node.symbol.t, tuple):
                    base_type, _ = node.symbol.t
                else:
                    base_type = node.symbol.t
                element_size = base_type.size // 8
            self.arch.integer(element_size)
            self.arch.mul()
            self.arch.add_base_address(node.name)
            addr = self.arch.accumulator

    def visit_NodeUnaryOp(self, node: NodeUnaryOp) -> None:
        node.right.accept(self)
        table = {
            PLUS: self.arch.integer,
            MINUS: self.arch.signed_value,
            BITWISE_NOT: self.arch.bitwise_not
        }
        table[node.op]()

    def visit_NodeBinaryOp(self, node: NodeBinaryOp) -> None:
        node.right.accept(self)
        self.arch.push()
        node.left.accept(self)
        self.arch.pop()

        signed = (isinstance(node.left, NodeID) and isinstance(node.left.symbol, ShardVariable) and node.left.symbol.t.signed) or (isinstance(node.right, NodeID) and isinstance(node.right.symbol, ShardVariable) and node.right.symbol.t.signed)

        table = {
            PLUS: self.arch.add,
            MINUS: self.arch.sub,
            TIMES: self.arch.mul,
            DIVIDE: self.arch.div if not signed else self.arch.signed_div,
            MODULO: self.arch.modulo if not signed else self.arch.signed_modulo,
            BITWISE_AND: self.arch.bitwise_and,
            BITWISE_OR: self.arch.bitwise_or,
            BITWISE_XOR: self.arch.bitwise_xor,
            LSHIFT: self.arch.shift_left,
            RSHIFT: self.arch.shift_right if not signed else self.arch.signed_shift_right,
            EQUALS: functools.partial(self.arch.compare, comparison=EQUAL),
            NOTEQUALS: functools.partial(self.arch.compare, comparison=NOT_EQUAL),
            LESSER_THAN: functools.partial(self.arch.compare, comparison=LT_UNSIGNED if not signed else LT_SIGNED),
            GREATER_THAN: functools.partial(self.arch.compare, comparison=GT_UNSIGNED if not signed else GT_SIGNED),
            LT_EQUAL: functools.partial(self.arch.compare, comparison=LTQ_UNSIGNED if not signed else LTQ_SIGNED),
            GT_EQUAL: functools.partial(self.arch.compare, comparison=GTQ_UNSIGNED if not signed else GTQ_SIGNED)
        }

        func = table[node.op]
        func()

    def visit_NodeAssignOp(self, node: NodeAssignOp) -> None:
        signed = isinstance(node.symbol, ShardVariable) and node.symbol.t.signed

        if node.name.idx is None:
            node.val.accept(self)
            op = node.op
            if op != SET:
                self.arch.access_value(node.name.name)
                self.arch.push()
                node.val.accept(self)
                self.arch.pop()
                table = {
                    SET_PLUS: self.arch.add,
                    SET_MINUS: self.arch.sub,
                    SET_TIMES: self.arch.mul,
                    SET_DIVIDE: self.arch.div if not signed else self.arch.signed_div,
                    SET_MODULO: self.arch.modulo if not signed else self.arch.signed_modulo,
                    SET_LSHIFT: self.arch.shift_left,
                    SET_RSHIFT: self.arch.shift_right if not signed else self.arch.signed_shift_right,
                    SET_BITWISE_AND: self.arch.bitwise_and,
                    SET_BITWISE_OR: self.arch.bitwise_or,
                    SET_BITWISE_XOR: self.arch.bitwise_xor,
                    SET_BITWISE_NOT: self.arch.bitwise_not
                }
                func = table.get(op)
                if func:
                    func()
            self.arch.store_addr(node.name.name)

        if isinstance(node.name.idx, NodeValue):
            idx_val = node.name.idx.value
            if node.symbol is not None:
                if isinstance(node.symbol.t, tuple):
                    base_type, _ = node.symbol.t
                else:
                    base_type = node.symbol.t
                element_size = base_type.size // 8
            else:
                element_size = 1

            offset = int(idx_val) * element_size
            addr = self.arch.addr_offset(node.name.name, offset)

            node.val.accept(self)
            self.arch.store_addr(addr)

        if isinstance(node.name.idx, NodeID):
            node.name.idx.accept(self)
            self.arch.push()

            element_size = 1
            if node.symbol is not None:
                if isinstance(node.symbol.t, tuple):
                    base_type, _ = node.symbol.t
                else:
                    base_type = node.symbol.t
                element_size = base_type.size // 8

            self.arch.integer(element_size)
            self.arch.pop()
            self.arch.mul()
            self.arch.push()

            self.arch.integer(node.name.name)
            self.arch.pop()
            self.arch.add()
            self.arch.push()

            node.val.accept(self)

            self.arch.pop()
            self.arch.store_addr(self.arch.register_b)

    def visit_NodeGroup(self, node: NodeGroup) -> None:
            node.group.accept(self)

    def visit_NodeVariableDecl(self, node: NodeVariableDecl) -> None:
        value = None

        if node.val is not None:
            if isinstance(node.val, NodeValue):
                value = node.val.value
            elif isinstance(node.val, NodeExpressionList):
                value = [expr.value if isinstance(expr, NodeValue) else None for expr in node.val.expressions]
            else:
                value = getattr(node.val, "val", None)

        if isinstance(node.datatype, tuple):
            base_type, array_size = node.datatype
        else:
            base_type, array_size = node.datatype, 1

        if node.prefix == VAR:
            if value is None:
                self.arch.define_buffer(node.name, base_type, array_size.value if not hasattr(array_size, "val") else array_size.val)
            else:
                if isinstance(value, list):
                    self.arch.define_variable(f"{node.name}", base_type, ', '.join([val for val in value]))
                else:
                    self.arch.define_variable(node.name, base_type, value)

        elif node.prefix == CONST:
            if value is None:
                ShardError_UninitializedConstant(node.name).display()
            else:
                if isinstance(value, list):
                    self.arch.define_const(f"{node.name}", base_type, ', '.join([val for val in value]))
                else:
                    self.arch.define_const(node.name, base_type, value)