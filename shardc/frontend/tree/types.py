from shardc.frontend.tree.expressions import NodeExpression
from shardc.frontend.tree.node import Node

class NodeT(Node):
    pass

class NodeType(NodeT):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"NodeType(name={self.name})"

class NodeDereferenceType(NodeT):
    def __init__(self, name: str, nderefs: int):
        self.name = name
        self.nderefs = nderefs

    def __repr__(self) -> str:
        return f"NodeReferenceType(name={self.name}, nderefs={self.nderefs})"

class NodeArrayType(NodeT):
    def __init__(self, name: str, length: NodeExpression):
        self.name = name
        self.length = length

    def __repr__(self) -> str:
        return f"NodeArrayType(name={self.name}, length={self.length})"

class NodeTypeAlias(Node):
    def __init__(self, name: str, base: NodeT):
        self.name = name
        self.base = base

    def __repr__(self) -> str:
        return f"NodeTypeAlias(name={self.name}, base={self.base})"

class NodeNewType(Node):
    def __init__(self, name: str, translation: str):
        self.name = name
        self.translation = translation

    def __repr__(self) -> str:
        return f"NodeNewType(name={self.name}, translation={self.translation})"