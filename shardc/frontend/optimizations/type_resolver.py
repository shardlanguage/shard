from typing import Any
from shardc.backend.visitor import Visitor
from shardc.frontend.tree.codeblocks import NodeCodeBlock, NodeStructureBody
from shardc.frontend.tree.condition_struct import NodeCondition, NodeElif, NodeElse, NodeIf
from shardc.frontend.tree.declarations import NodeExternDeclaration, NodeVariableDeclaration
from shardc.frontend.tree.expressions import NodeArrayAccess, NodeArrayAssignmentOp, NodeAssignmentOp, NodeBinaryOp, NodeCast, NodeFieldAccess, NodeFieldAssignmentOp, NodeIDAccess, NodeUnaryOp
from shardc.frontend.tree.function_def import NodeFunctionDefinition
from shardc.frontend.tree.loop_struct import NodeLoopForever, NodeLoopUntil, NodeLoopWhile
from shardc.frontend.tree.node import Node
from shardc.frontend.tree.structure_def import NodeStructureDefinition
from shardc.frontend.tree.types import NodeArrayType, NodeDereferenceType, NodeNewType, NodeT, NodeType, NodeTypeAlias
from shardc.frontend.types.shardtype import ShardType
from shardc.frontend.types.table import TypeTable
from shardc.utils.constants.types import S_VOID

class TypeResolver(Visitor):
    def __init__(self, type_table: TypeTable):
        self.type_table = type_table
        super().__init__("resolve")

    def resolve_type(self, node: Node) -> None:
        if node is not None:
            node.accept(self)

    def resolve_NodeType(self, node: NodeType) -> ShardType:
        return self.type_table.get_type(node.name)

    def resolve_NodeReferenceType(self, node: NodeDereferenceType) -> ShardType:
        return self.type_table.get_type(node.name)

    def resolve_NodeArrayType(self, node: NodeArrayType) -> ShardType:
        return self.type_table.get_type(node.name)

    def resolve_NodeDereferenceType(self, node: NodeDereferenceType) -> ShardType:
        return self.type_table.get_type(node.name)

    def resolve_NodeTypeAlias(self, node: NodeTypeAlias) -> None:
        self.resolve_type(node.base)
        t = self.type_table.get_type(node.base.name)
        t.name = node.name
        self.type_table.add_type(t)

    def resolve_NodeNewType(self, node: NodeNewType) -> None:
        t = ShardType(node.name, node.translation[1:-1])
        self.type_table.add_type(t)

    def resolve_NodeArrayAccess(self, node: NodeArrayAccess) -> None:
        self.resolve_type(node.index)

    def resolve_NodeUnaryOp(self, node: NodeUnaryOp) -> None:
        self.resolve_type(node.right)

    def resolve_NodeBinaryOp(self, node: NodeBinaryOp) -> None:
        self.resolve_type(node.left)
        self.resolve_type(node.right)

    def resolve_NodeAssignmentOp(self, node: NodeAssignmentOp) -> None:
        self.resolve_type(node.value)

    def resolve_NodeArrayAssignmentOp(self, node: NodeArrayAssignmentOp) -> None:
        self.resolve_type(node.index)
        self.resolve_type(node.value)

    def resolve_NodeFieldAssignmentOp(self, node: NodeFieldAssignmentOp) -> None:
        self.resolve_type(node.value)

    def resolve_NodeCast(self, node: NodeCast) -> None:
        t: Any = node.t.accept(self)
        base = self.type_table.get_type(t.name)
        shardt = base.clone()

        if isinstance(node.t, NodeArrayType):
            shardt.name = f"[{node.t.length}]{base.name}"
            shardt.c = f"{base.c}[{node.t.length}]"
            shardt.length = node.t.length
            if shardt.name not in self.type_table.table:
                self.type_table.add_array_type(shardt)

        elif isinstance(node.t, NodeDereferenceType):
            shardt.name = f"{base.name}{'*'*node.t.nderefs}"
            shardt.c = f"{base.c}{'*'*node.t.nderefs}"
            if shardt.name not in self.type_table.table:
                self.type_table.add_deref_type(shardt)

        node.shardt = shardt
        self.resolve_type(node.value)

    def resolve_NodeVariableDeclaration(self, node: NodeVariableDeclaration) -> None:
        t: Any = node.t.accept(self)
        shardt = self.type_table.get_type(t.name)
        if isinstance(node.t, NodeArrayType):
            shardt.name = f"[{node.t.length}]{node.t.name}"
            shardt.length = node.t.length
            if shardt.name not in self.type_table.table:
                self.type_table.add_array_type(shardt)
        if isinstance(node.t, NodeDereferenceType):
            shardt.name = f"{'*'*node.t.nderefs}{node.t.name}"
            if shardt.name not in self.type_table.table:
                self.type_table.add_deref_type(shardt)
        node.shardt = shardt

        if node.value is not None:
            self.resolve_type(node.value)

    def resolve_NodeExternDeclaration(self, node: NodeExternDeclaration) -> None:
        self.resolve_type(node.symbol)

    def resolve_NodeCodeBlock(self, node: NodeCodeBlock) -> None:
        local_table = TypeTable(parent=self.type_table)
        old_table = self.type_table
        self.type_table = local_table
        for stmt in node.content:
            self.resolve_type(stmt)
        self.type_table = old_table

    def resolve_NodeStructureBody(self, node: NodeStructureBody) -> None:
        for stmt in node.content:
            self.resolve_type(stmt)

    def resolve_NodeIf(self, node: NodeIf) -> None:
        self.resolve_type(node.branch)

    def resolve_NodeElif(self, node: NodeElif) -> None:
        self.resolve_type(node.branch)

    def resolve_NodeElse(self, node: NodeElse) -> None:
        self.resolve_type(node.branch)

    def resolve_NodeCondition(self, node: NodeCondition) -> None:
        self.resolve_type(node.if_)
        if node.elif_ is not None:
            for nd in node.elif_:
                self.resolve_type(nd)
        if node.else_ is not None:
            self.resolve_type(node.else_)

    def resolve_NodeLoopForever(self, node: NodeLoopForever) -> None:
        self.resolve_type(node.branch)

    def resolve_NodeLoopWhile(self, node: NodeLoopWhile) -> None:
        self.resolve_type(node.branch)

    def resolve_NodeLoopUntil(self, node: NodeLoopUntil) -> None:
        self.resolve_type(node.branch)

    def resolve_NodeFunctionDefinition(self, node: NodeFunctionDefinition) -> None:
        if node.t is not None:
            t: Any = node.t.accept(self)
            shardt = self.type_table.get_type(t.name)
            if isinstance(node.t, NodeArrayType):
                shardt.name = f"[{node.t.length}]{node.t.name}"
                shardt.length = node.t.length
                if shardt.name not in self.type_table.table:
                    self.type_table.add_array_type(shardt)
            if isinstance(node.t, NodeDereferenceType):
                shardt.name = f"{'*'*node.t.nderefs}{node.t.name}"
                if shardt.name not in self.type_table.table:
                    self.type_table.add_deref_type(shardt)
            node.shardt = shardt
        else:
            node.shardt = self.type_table.table[S_VOID]

        for param in node.parameters:
            self.resolve_type(param)

        self.resolve_type(node.body)

    def resolve_NodeStructureDefinition(self, node: NodeStructureDefinition) -> None:
        self.type_table.add_type(ShardType(node.name, f"struct {node.name}"))

        self.resolve_type(node.body)