from shardc.frontend.tree.expressions import NodeString
from shardc.frontend.tree.node import Node

class NodeInline(Node):
    pass

class NodeInlineC(NodeInline):
    def __init__(self, code: NodeString):
        self.code = code

    def __repr__(self) -> str:
        return f"NodeInlineC(code={self.code})"