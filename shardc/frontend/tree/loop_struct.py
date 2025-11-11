from shardc.frontend.tree.codeblocks import NodeCodeBlock
from shardc.frontend.tree.declarations import NodeDeclaration
from shardc.frontend.tree.expressions import NodeExpression
from shardc.frontend.tree.node import Node

class NodeLoopStructure(Node):
    pass

class NodeLoopForever(NodeLoopStructure):
    def __init__(self, branch: NodeCodeBlock):
        self.branch = branch

    def __repr__(self) -> str:
        return f"NodeLoopForever(branch={self.branch})"

class NodeLoopWhile(NodeLoopStructure):
    def __init__(self, condition: NodeExpression, branch: NodeCodeBlock):
        self.condition = condition
        self.branch = branch

    def __repr__(self) -> str:
        return f"NodeLoopWhile(condition={self.condition}, branch={self.branch})"

class NodeLoopUntil(NodeLoopStructure):
    def __init__(self, condition: NodeExpression, branch: NodeCodeBlock):
        self.condition = condition
        self.branch = branch

    def __repr__(self) -> str:
        return f"NodeLoopUntil(condition={self.condition}, branch={self.branch})"

class NodeLoopFor(NodeLoopStructure):
    def __init__(self, declaration: NodeDeclaration, condition: NodeExpression, update: NodeExpression, branch: NodeCodeBlock):
        self.declaration = declaration
        self.condition = condition
        self.update = update
        self.branch = branch

    def __repr__(self) -> str:
        return f"NodeLoopFor(declaration={self.declaration}, condition={self.condition}, update={self.update}, branch={self.branch})"