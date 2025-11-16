from shardc.backend.visitor import Visitor
from shardc.frontend.tree.codeblocks import NodeCodeBlock
from shardc.frontend.tree.namespace_def import NodeNamespaceDefinition
from shardc.frontend.tree.node import Node
from shardc.frontend.tree.structure_def import NodeStructureDefinition
from shardc.frontend.tree.declarations import NodeVariableDeclaration
from shardc.frontend.tree.function_def import NodeFunctionDefinition
from shardc.frontend.tree.condition_struct import NodeIf, NodeElif, NodeElse, NodeCondition
from shardc.frontend.tree.loop_struct import NodeLoopStructure
from shardc.frontend.tree.types import NodeNewType, NodeTypeAlias
from shardc.utils.errors.content import ShardError_InvalidNamespaceContent, ShardError_InvalidStructContent, ShardError_NestedFunctions

class ContentVerifier(Visitor):
    def __init__(self):
        super().__init__("verify")

    def verify_content(self, node: Node) -> None:
        node.accept(self)

    def verify_NodeCodeBlock(self, node: NodeCodeBlock) -> None:
        for nd in node.content:
            self.verify_content(nd)

    def verify_NodeIf(self, node: NodeIf) -> None:
        self.verify_content(node.branch)

    def verify_NodeElif(self, node: NodeElif) -> None:
        self.verify_content(node.branch)

    def verify_NodeElse(self, node: NodeElse) -> None:
        self.verify_content(node.branch)

    def verify_NodeCondition(self, node: NodeCondition) -> None:
        self.verify_content(node.if_)
        if node.elif_ is not None:
            for nd in node.elif_:
                self.verify_content(nd)
        if node.else_ is not None:
            self.verify_content(node.else_)

    def check_NodeLoopStructure(self, node: NodeLoopStructure) -> None:
        self.verify_content(node.branch)

    def verify_NodeStructureDefinition(self, node: NodeStructureDefinition) -> None:
        allowed_nodes = [
            NodeStructureDefinition,
            NodeVariableDeclaration
        ]

        for nd in node.body.content:
            if type(nd) not in allowed_nodes:
                ShardError_InvalidStructContent(nd.__class__.__name__).display()

    def verify_NodeNamespaceDefinition(self, node: NodeNamespaceDefinition) -> None:
        allowed_nodes = [
            NodeNamespaceDefinition,
            NodeStructureDefinition,
            NodeFunctionDefinition,
            NodeVariableDeclaration,
            NodeTypeAlias,
            NodeNewType
        ]

        for nd in node.content.content:
            if type(nd) not in allowed_nodes:
                ShardError_InvalidNamespaceContent(nd.__class__.__name__).display()

    def verify_NodeFunctionDefinition(self, node: NodeFunctionDefinition):
        for nd in node.body.content:
            if isinstance(nd, NodeFunctionDefinition):
                ShardError_NestedFunctions(node.name, nd.name).display()