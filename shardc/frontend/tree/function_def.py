from shardc.frontend.symbols.symbol import ShardSymbol
from shardc.frontend.tree.codeblocks import NodeCodeBlock
from shardc.frontend.tree.declarations import NodeDeclaration
from shardc.frontend.tree.types import NodeT
from shardc.frontend.tree.node import Node
from shardc.frontend.types.shardtype import ShardType

class NodeFunctionDefinition(Node):
    def __init__(self, name: str, parameters: list[NodeDeclaration], t: NodeT | None, body: NodeCodeBlock):
        self.name = name
        self.parameters = parameters
        self.t = t
        self.body = body
        self.shardt: ShardType | None = None
        self.symbol: ShardSymbol | None = None

    def __repr__(self) -> str:
        return f"NodeFunctionDefinition(name={self.name}, parameters={self.parameters}, t={self.t}, body={self.body}, shardt={self.shardt}, symbol={self.symbol})"