from shardc.backend.visitor import Visitor
from shardc.frontend.tree.codeblocks import NodeCodeBlock
from shardc.frontend.tree.condition_struct import NodeIf, NodeElif, NodeElse, NodeCondition
from shardc.frontend.tree.flow_control import NodeBreak, NodeContinue, NodeReturn
from shardc.frontend.tree.loop_struct import NodeLoopStructure
from shardc.frontend.tree.function_def import NodeFunctionDefinition
from shardc.frontend.tree.namespace_def import NodeNamespaceDefinition
from shardc.frontend.tree.node import Node
from shardc.utils.errors.context import ShardError_BreakOutsideOfLoop, ShardError_ContinueOutsideOfLoop, ShardError_ReturnOutsideOfFunction
from shardc.utils.structures.stack import Stack

class ContextChecker(Visitor):
    def __init__(self):
        self.loop_stack = Stack()
        self.function_stack = Stack()
        super().__init__("check")

    def check_context(self, node: Node) -> None:
        if node is not None:
            node.accept(self)

    def check_NodeCodeBlock(self, node: NodeCodeBlock) -> None:
        for statement in node.content:
            self.check_context(statement)

    def check_NodeIf(self, node: NodeIf) -> None:
        self.check_context(node.branch)

    def check_NodeElif(self, node: NodeElif) -> None:
        self.check_context(node.branch)

    def check_NodeElse(self, node: NodeElse) -> None:
        self.check_context(node.branch)

    def check_NodeCondition(self, node: NodeCondition) -> None:
        self.check_context(node.if_)
        if node.elif_ is not None:
            for nd in node.elif_:
                self.check_context(nd)
        if node.else_ is not None:
            self.check_context(node.else_)

    def check_NodeLoopStructure(self, node: NodeLoopStructure) -> None:
        self.loop_stack.push(True)
        self.check_context(node.branch)
        self.loop_stack.pop()

    def check_NodeNamespaceDefinition(self, node: NodeNamespaceDefinition) -> None:
        self.check_context(node.content)

    def check_NodeFunctionDefinition(self, node: NodeFunctionDefinition) -> None:
        self.function_stack.push(True)
        self.check_context(node.body)
        self.function_stack.pop()

    def check_NodeBreak(self, node: NodeBreak) -> None:
        if self.loop_stack.isempty():
            ShardError_BreakOutsideOfLoop().display()

    def check_NodeContinue(self, node: NodeContinue) -> None:
        if self.loop_stack.isempty():
            ShardError_ContinueOutsideOfLoop().display()

    def check_NodeReturn(self, node: NodeReturn) -> None:
        if self.function_stack.isempty():
            ShardError_ReturnOutsideOfFunction().display()