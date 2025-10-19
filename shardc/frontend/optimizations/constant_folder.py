from shardc.frontend.nodes.declaration import NodeVariableDecl
from shardc.frontend.nodes.expression import NodeAssignOp, NodeBinaryOp, NodeGroup, NodeUnaryOp, NodeValue
from shardc.frontend.nodes.node import Node

class ConstantFolder:
    def __init__(self):
        pass

    def fold_constants(self, node: Node):
        function_name = f"fold_{type(node).__name__}"
        function = getattr(self, function_name, self.generic_fold)
        return function(node)

    def generic_fold(self, node: Node) -> None:
        pass

    def fold_NodeValue(self, node: NodeValue):
        return node.value

    def fold_NodeUnaryOp(self, node: NodeUnaryOp):
        _right = self.fold_constants(node.right)

        if _right is None:
            return None

        right = int(_right)

        table = {
            '+': +right,
            '-': -right,
            '~': ~right
        }

        node.val = table[node.op]
        return node.val

    def fold_NodeBinaryOp(self, node: NodeBinaryOp):
        _left = self.fold_constants(node.left)
        _right = self.fold_constants(node.right)

        if _left is None or _right is None:
            return None

        left = int(_left)
        right = int(_right)

        table = {
            '+': left + right,
            '-': left - right,
            '*': left * right,
            '/': left // right,
            '%': left % right,
            '<<': left << right,
            '>>': left >> right,
            '&': left & right,
            '|': left | right,
            '^': left ^ right,
            '==': int(left == right),
            '!=': int(left != right),
            '<': int(left < right),
            '>': int(left > right),
            '<=': int(left <= right),
            '>=': int(left >= right)
        }

        node.val = table[node.op]
        return node.val

    def fold_NodeAssignOp(self, node: NodeAssignOp):
        val = self.fold_constants(node.val)
        return val

    def fold_NodeGroup(self, node: NodeGroup):
        group = self.fold_constants(node.group)
        return group

    def fold_NodeVariableDecl(self, node: NodeVariableDecl):
        val = self.fold_constants(node.val)
        return val