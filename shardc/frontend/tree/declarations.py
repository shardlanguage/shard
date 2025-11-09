from shardc.frontend.symbols.symbol import ShardSymbol
from shardc.frontend.tree.expressions import NodeExpression
from shardc.frontend.tree.node import Node
from shardc.frontend.tree.types import  NodeT
from shardc.frontend.types.shardtype import ShardType

class NodeDeclaration(Node):
    pass

class NodeVariableDeclaration(NodeDeclaration):
    def __init__(self, prefix: str, name: str, t: NodeT, value: NodeExpression | None):
        self.prefix = prefix
        self.name = name
        self.t = t
        self.value = value
        self.symbol: ShardSymbol | None = None
        self.shardt: ShardType | None = None

    def __repr__(self) -> str:
        return f"NodeVariableDeclaration(prefix={self.prefix}, name={self.name}, type={self.t}, value={self.value}, symbol={self.symbol}, shardtype={self.shardt})"

class NodeExternDeclaration(NodeDeclaration):
    def __init__(self, declaration: NodeVariableDeclaration):
        self.symbol = declaration

    def __repr__(self) -> str:
        return f"NodeVariableDeclaration(symbol={self.symbol})"