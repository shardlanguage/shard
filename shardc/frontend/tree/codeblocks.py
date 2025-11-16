from shardc.frontend.tree.node import Node

class NodeCodeBlock(Node):
    def __init__(self, content: list[Node]):
        self.content = content

    def __repr__(self) -> str:
        return f"NodeCodeBlock(content={self.content})"

class NodeStructureBody(Node):
    def __init__(self, contnent: list[Node]):
        self.content = contnent

    def __repr__(self) -> str:
        return f"NodeStructureBody(content={self.content})"

class NodeNamespaceBody(Node):
    def __init__(self, content: list[Node]):
        self.content = content

    def __repr__(self) -> str:
        return f"NodeNamespaceBody(content={self.content})"