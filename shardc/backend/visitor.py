from shardc.backend.codegen.architecure import Architecture
from shardc.frontend.nodes.expression import NodeBinaryOp, NodeGroup, NodeUnaryOp, NodeValue
from shardc.utils.const.types import INT

class CodeGenerator:
    def __init__(self, arch: Architecture):
        self.output = []
        self.arch = arch

    def emit(self, line: str) -> None:
        self.output.append(line)

    def generate(self, node) -> str:
        node.accept(self)
        return "\n".join(self.output)

    def generic_visit(self, node) -> None:
        raise NotImplementedError(f"No visitor for {type(node).__name__}")

    def visit_NodeValue(self, node: NodeValue) -> None:
        code = ""
        if node.t == INT:
            code = self.arch.integer(node.value)

        self.emit(code)

    def visit_NodeUnaryOp(self, node: NodeUnaryOp) -> None:
        node.right.accept(self)
        table = {
            '-': self.arch.signed_value,
            '~': self.arch.bitwise_not
        }
        self.emit(table[node.op]())

    def visit_NodeBinaryOp(self, node: NodeBinaryOp) -> None:
        node.left.accept(self)
        self.emit(self.arch.push())
        node.right.accept(self)
        self.emit(self.arch.pop())
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
        self.emit(table[node.op]())

    def visit_NodeGroup(self, node: NodeGroup) -> None:
        node.group.accept(self)