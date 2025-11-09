from shardc.frontend.symbols.symbol import ShardSymbol
from shardc.frontend.tree.node import Node
from shardc.frontend.types.shardtype import ShardType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shardc.frontend.tree.types import NodeT

class NodeExpression(Node):
    pass

class NodeAccess(NodeExpression):
    pass

class NodeNumber(NodeExpression):
    def __init__(self, value: str):
        self.value = float(value) if not isinstance(value, int) and '.' in value else int(value)

    def __repr__(self) -> str:
        return f"NodeNumber(value={self.value})"

class NodeString(NodeExpression):
    def __init__(self, value: str):
        self.value = value[1:-1]

    def __repr__(self) -> str:
        return f"NodeString(value={self.value})"

class NodeIDAccess(NodeAccess):
    def __init__(self, name: str):
        self.name = name
        self.symbol: ShardSymbol | None = None

    def __repr__(self) -> str:
        return f"NodeIDAccess(name={self.name}, symbol={self.symbol})"

class NodeArrayAccess(NodeAccess):
    def __init__(self, name: str, index: NodeExpression):
        self.name = name
        self.index = index
        self.symbol: ShardSymbol | None = None

    def __repr__(self) -> str:
        return f"NodeArrayAcess(name={self.name}, index={self.index})"

class NodeFieldAccess(NodeAccess):
    def __init__(self, instance: NodeAccess, field: NodeAccess):
        self.instance = instance
        self.field = field
        self.symbol: ShardSymbol | None = None

    def __repr__(self) -> str:
        return f"NodeFieldAccess(instance={self.instance}, field={self.field}, symbol={self.symbol})"

class NodeFunctionCall(NodeExpression):
    def __init__(self, name: str, parameters: list[NodeExpression]):
        self.name = name
        self.parameters = parameters
        self.symbol: ShardSymbol | None = None

    def __repr__(self) -> str:
        return f"NodeFunctionCall(name={self.name}, parameters={self.parameters}, symbol={self.symbol})"

class NodeUnaryOp(NodeExpression):
    def __init__(self, op: str, right: NodeExpression):
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"NodeUnaryOp(op={self.op}, right={self.right})"

class NodeBinaryOp(NodeExpression):
    def __init__(self, op: str, left: NodeExpression, right: NodeExpression):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"NodeBinaryOp(op={self.op}, left={self.left}, right={self.right})"

class NodeAssignmentOp(NodeExpression):
    def __init__(self, op: str, name: NodeIDAccess, value: NodeExpression):
        self.op = op
        self.name = name.name
        self.value = value
        self.symbol: ShardSymbol | None = None

    def __repr__(self) -> str:
        return f"NodeAssignmentOp(op={self.op}, name={self.name}, value={self.value}, symbol={self.symbol})"

class NodeArrayAssignmentOp(NodeExpression):
    def __init__(self, op: str, name: NodeArrayAccess, value: NodeExpression):
        self.op = op
        self.name = name.name
        self.index = name.index
        self.value = value
        self.symbol: ShardSymbol | None = None

    def __repr__(self) -> str:
        return f"NodeArrayAssignmentOp(op={self.op}, name={self.name}, index={self.index} value={self.value}, symbol={self.symbol})"

class NodeFieldAssignmentOp(NodeExpression):
    def __init__(self, op: str, name: NodeFieldAccess, value: NodeExpression):
        self.op = op
        self.instance = name.instance
        self.field = name.field
        self.value = value
        self.symbol: ShardSymbol | None = None

    def __repr__(self) -> str:
        return f"NodeFieldAssignmentOp(op={self.op}, instance={self.instance}, field={self.field}, value={self.value}, symbol={self.symbol})"

class NodeCast(NodeExpression):
    def __init__(self, value: NodeExpression, t: 'NodeT'):
        self.value = value
        self.t = t
        self.shardt: ShardType | None = None

    def __repr__(self) -> str:
        return f"NodeCast(value={self.value}, t={self.t}, shardt={self.shardt})"

class NodeGroupOp(NodeExpression):
    def __init__(self, group: NodeExpression):
        self.group = group

    def __repr__(self) -> str:
        return f"NodeGroupOp(group={self.group})"