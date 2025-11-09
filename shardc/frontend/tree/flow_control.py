from shardc.frontend.tree.expressions import NodeExpression
from shardc.frontend.tree.node import Node

class NodeFlowControl(Node):
    pass

class NodeBreak(NodeFlowControl):
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return f"NodeBreak()"

class NodeContinue(NodeFlowControl):
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return f"NodeContinue()"

class NodeReturn(NodeFlowControl):
    def __init__(self, value: NodeExpression | None):
        self.value = value

    def __repr__(self) -> str:
        return f"NodeReturn(value={self.value})"