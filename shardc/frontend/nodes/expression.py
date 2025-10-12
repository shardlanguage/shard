from shardc.frontend.nodes.node import Node

class NodeValue(Node):
    def __init__(self, value, t):
        self.value = value
        self.t = t

    def __repr__(self):
        return f"NodeValue(value={self.value}, type={self.t})"

class NodeUnaryOp(Node):
    def __init__(self, op, right):
        self.op = op
        self.right = right

    def __repr__(self):
        return f"NodeUnaryOp(op={self.op}, right={self.right})"

class NodeBinaryOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f"NodeBinaryOp(op={self.op}, left={self.left}, right={self.right})"

class NodeGroup(Node):
    def __init__(self, group):
        self.group = group

    def __repr__(self):
        return f"NodeGroup(group={self.group})"