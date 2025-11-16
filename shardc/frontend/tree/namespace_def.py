from shardc.frontend.tree.codeblocks import NodeNamespaceBody
from shardc.frontend.tree.expressions import NodeIDAccess
from shardc.frontend.tree.node import Node
from shardc.frontend.symbols.symbol import ShardSymbol

class NodeNamespaceDefinition(Node):
    def __init__(self, name: NodeIDAccess, content: NodeNamespaceBody):
        self.name = name
        self.content = content
        self.symbol: ShardSymbol | None = None

    def __repr__(self) -> str:
        return f"NodeNamespaceDefinition(name={self.name}, content={self.content}, symbol={self.symbol})"