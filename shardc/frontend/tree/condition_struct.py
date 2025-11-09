from shardc.frontend.tree.codeblocks import NodeCodeBlock
from shardc.frontend.tree.expressions import NodeExpression
from shardc.frontend.tree.node import Node

class NodeConditionalStruct(Node):
    pass

class NodeIf(NodeConditionalStruct):
    def __init__(self, condition: NodeExpression, branch: NodeCodeBlock):
        self.condition = condition
        self.branch = branch

    def __repr__(self) -> str:
        return f"NodeIf(condition={self.condition}, branch={self.branch})"

class NodeElif(NodeConditionalStruct):
    def __init__(self, condition: NodeExpression, branch: NodeCodeBlock):
        self.condition = condition
        self.branch = branch

    def __repr__(self) -> str:
        return f"NodeElif(condition={self.condition}, branch={self.branch})"

class NodeElse(NodeConditionalStruct):
    def __init__(self, branch: NodeCodeBlock):
        self.branch = branch

    def __repr__(self) -> str:
        return f"NodeElse(branch={self.branch})"

class NodeCondition(NodeConditionalStruct):
    def __init__(self, if_: NodeIf, elif_: list[NodeElif] | None, else_: NodeElse | None):
        self.if_ = if_
        self.elif_ = elif_
        self.else_ = else_

    def __repr__(self) -> str:
        return f"NodeCondition(if={self.if_}, elif={self.elif_}, else={self.else_})"