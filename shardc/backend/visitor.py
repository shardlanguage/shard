from shardc.backend.codegen.architecure import Architecture
from shardc.frontend.nodes.declaration import NodeVariableDecl
from shardc.frontend.nodes.expression import NodeAssignOp, NodeBinaryOp, NodeGroup, NodeID, NodeUnaryOp, NodeValue
from shardc.utils.const.types import INT

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
        table = {
            '+': self.arch.add,
            '-': self.arch.sub,
            '*': self.arch.mul,
            '/': self.arch.div,
            '%': self.arch.modulo,
            '&': self.arch.bitwise_and,
            '|': self.arch.bitwise_or,
            '^': self.arch.bitwise_xor,
            '<<': self.arch.shift_left,
            '>>': self.arch.shift_right
        }
        table[node.op]()

    def visit_NodeAssignOp(self, node: NodeAssignOp) -> None:
        node.val.accept(self)
        self.arch.store_addr(node.name)

    def visit_NodeGroup(self, node: NodeGroup) -> None:
        node.group.accept(self)

    def visit_NodeVariableDecl(self, node: NodeVariableDecl) -> None:
        if isinstance(node.val, NodeValue):
            value = node.val.value
            self.arch.define_variable(node.name, node.datatype, value)
        else:
            node.val.accept(self)
            self.arch.move_addr(node.name)
            self.arch.define_variable(node.name, node.datatype, 0)