from shardc.frontend.nodes.node import Node
from shardc.utils.types.datatype import ShardType

class NodeVariableDecl(Node):
    def __init__(self, prefix, name, t, val):
        self.prefix = prefix
        self.name = name
        self.t = t
        self.val = val
        self.datatype: ShardType

    def __repr__(self):
        return f"NodeVariableDecl(prefix={self.prefix}, name={self.name}, t={self.t}, val={self.val}, type={self.datatype})"