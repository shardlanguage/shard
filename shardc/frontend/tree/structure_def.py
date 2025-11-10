from shardc.frontend.tree.codeblocks import NodeStructureBody
from shardc.frontend.tree.node import Node
from shardc.frontend.symbols.symbol import ShardSymbol

class NodeStructureDefinition(Node):
    def __init__(self, name: str, body: NodeStructureBody):
        self.name = name
        self.body = body
        self.symbol: ShardSymbol | None = None

    def __repr__(self) -> str:
        return f"NodeStructureDefinition(name={self.name}, body={self.body}, symbol={self.symbol})"