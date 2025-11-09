from shardc.frontend.tree.node import Node

class NodeCodeBlock(Node):
    def __init__(self, content: list[Node]):
        self.content = content

    def __repr__(self) -> str:
        return f"NodeCodeBlock(content={self.content})"