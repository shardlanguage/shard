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
        code = ""
        if node.op == '-':
            code = self.arch.signed_value()
        self.emit(code)

    def visit_NodeBinaryOp(self, node: NodeBinaryOp) -> None:
        node.left.accept(self)
        self.emit(self.arch.push())
        node.right.accept(self)
        self.emit(self.arch.pop())
        if node.op == '+': self.emit(self.arch.add())
        if node.op == '-': self.emit(self.arch.sub())
        if node.op == '*': self.emit(self.arch.mul())
        if node.op == '/': self.emit(self.arch.div())

    def visit_NodeGroup(self, node: NodeGroup) -> None:
        node.group.accept(self)