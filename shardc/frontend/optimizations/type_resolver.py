from typing import Any

from shardc.backend.visitor import Visitor
from shardc.frontend.tree.codeblocks import NodeCodeBlock, NodeNamespaceBody, NodeStructureBody
from shardc.frontend.tree.condition_struct import NodeCondition, NodeElif, NodeElse, NodeIf
from shardc.frontend.tree.declarations import NodeExternDeclaration, NodeVariableDeclaration
from shardc.frontend.tree.expressions import NodeArrayAccess, NodeArrayAssignmentOp, NodeAssignmentOp, NodeBinaryOp, NodeCast, NodeFieldAssignmentOp, NodeIDAccess, NodeNamespaceAccess, NodeUnaryOp
from shardc.frontend.tree.function_def import NodeFunctionDefinition
from shardc.frontend.tree.loop_struct import NodeLoopFor, NodeLoopForever, NodeLoopUntil, NodeLoopWhile
from shardc.frontend.tree.namespace_def import NodeNamespaceDefinition
from shardc.frontend.tree.node import Node
from shardc.frontend.tree.structure_def import NodeStructureDefinition
from shardc.frontend.tree.types import NodeArrayType, NodeDereferenceType, NodeNamespaceType, NodeNewType, NodeT, NodeType, NodeTypeAlias
from shardc.frontend.types.shardtype import ShardType
from shardc.frontend.types.table import TypeTable
from shardc.utils.constants.types import S_VOID
from shardc.utils.structures.stack import Stack

class TypeResolver(Visitor):
    def __init__(self, type_table: TypeTable):
        self.type_table = type_table
        self.namespace_stack = Stack()
        super().__init__("resolve")

    def _resolve_scoped_name(self, node: NodeNamespaceAccess) -> str:
        if isinstance(node.namespace, NodeIDAccess):
            ns_part = node.namespace.name
        elif isinstance(node.namespace, NodeNamespaceAccess):
            ns_part = self._resolve_scoped_name(node.namespace)
        else:
            ns_part = node.namespace.accept(self)

        if isinstance(node.sym, NodeIDAccess):
            sym_part = node.sym.name
        elif isinstance(node.sym, NodeNamespaceAccess):
            sym_part = self._resolve_scoped_name(node.sym)
        else:
            sym_part = str(node.sym)

        return f"{ns_part}::{sym_part}"

    def resolve_type(self, node: Node) -> Any:
        if node is not None:
            return node.accept(self)

    def resolve_NodeType(self, node: NodeType) -> ShardType:
        if isinstance(node.name, NodeIDAccess):
            tname = node.name.name
        elif isinstance(node.name, NodeNamespaceAccess):
            tname = self._resolve_scoped_name(node.name)
        else:
            tname = str(node.name)

        return self.type_table.get_type(tname)

    def resolve_NodeArrayType(self, node: NodeArrayType) -> ShardType:
        base = self.resolve_type(node.name)
        shardt = base.clone()
        shardt.name = f"{base.name}[{node.length}]"
        shardt.length = node.length
        if shardt.name not in self.type_table.table:
            self.type_table.add_array_type(shardt)
        return shardt

    def resolve_NodeDereferenceType(self, node: NodeDereferenceType) -> ShardType:
        if isinstance(node.name, NodeNamespaceAccess):
            base = self.resolve_NodeNamespaceAccess(node.name)
        elif isinstance(node.name, NodeType):
            base = self.resolve_NodeType(node.name)
        else:
            type_name = node.name.name if hasattr(node.name, "name") else str(node.name)
            base = self.type_table.get_type(type_name)

        shardt = base.clone()
        n_stars = node.nderefs
        if base.c.endswith('*'):
            n_stars -= base.name.count('*')
        shardt.name = f"{base.name}{'*'*max(n_stars, 1)}"
        shardt.c = f"{base.c}{'*'*max(n_stars, 1)}"

        if shardt.name not in self.type_table.table:
            self.type_table.add_deref_type(shardt)

        return shardt

    def resolve_NodeNamespaceType(self, node: NodeNamespaceType):
        ns_name = node.namespace.accept(self)
        t_name = node.t.accept(self) if isinstance(node.t, NodeType) else str(node.t)
        scoped_name = f"{ns_name}::{t_name}"

        t = self.type_table.get_type(scoped_name)
        return t

    def resolve_NodeTypeAlias(self, node: NodeTypeAlias) -> ShardType:
        base_type = self.resolve_type(node.base)

        alias_type = base_type.clone()
        alias_type.name = f"{'::'.join(self.namespace_stack.items())}::{node.name}"
        alias_type.c = base_type.c
        alias_type.alias_of = base_type.name

        self.type_table.add_type(alias_type)
        return alias_type

    def resolve_NodeNewType(self, node: NodeNewType) -> ShardType:
        t = ShardType(node.name.name, node.translation[1:-1])
        self.type_table.add_type(t)
        return t

    def resolve_NodeArrayAccess(self, node: NodeArrayAccess) -> None:
        self.resolve_type(node.index)

    def resolve_NodeNamespaceAccess(self, node: NodeNamespaceAccess):
        scoped_name = self._resolve_scoped_name(node)
        return self.type_table.get_type(scoped_name)

    def resolve_NodeIDAccess(self, node: NodeIDAccess) -> ShardType | None:
        if isinstance(node.name, NodeT):
            type_name = node.name if isinstance(node.name, str) else getattr(node.name, 'name', str(node.name))
            return self.type_table.get_type(type_name)

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

    def resolve_NodeCast(self, node: NodeCast) -> ShardType:
        if isinstance(node.t, NodeNamespaceType):
            shardt = node.t.accept(self)
        elif isinstance(node.t, NodeTypeAlias):
            shardt = node.t.accept(self)
        elif isinstance(node.t, NodeArrayType):
            shardt = self.resolve_NodeArrayType(node.t)
        elif isinstance(node.t, NodeDereferenceType):
            shardt = self.resolve_NodeDereferenceType(node.t)
        else:
            shardt = self.resolve_type(node.t)

        node.shardt = shardt
        self.resolve_type(node.value)

        return shardt

    def resolve_NodeVariableDeclaration(self, node: NodeVariableDeclaration) -> None:
        node.shardt = self.resolve_type(node.t)

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

    def resolve_NodeNamespaceBody(self, node: NodeNamespaceBody) -> None:
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

    def resolve_NodeLoopFor(self, node: NodeLoopFor) -> None:
        self.resolve_type(node.declaration)
        self.resolve_type(node.condition)
        self.resolve_type(node.update)
        self.resolve_type(node.branch)

    def resolve_NodeFunctionDefinition(self, node: NodeFunctionDefinition) -> None:
        if node.t is not None:
            if isinstance(node.t.name, NodeNamespaceAccess):
                t: Any = node.t.name.accept(self)
            else:
                t: Any = node.t.accept(self)
        else:
            t: Any = self.type_table.table[S_VOID]
        node.shardt = t

        for param in node.parameters:
            self.resolve_type(param)

        self.resolve_type(node.body)

    def resolve_NodeStructureDefinition(self, node: NodeStructureDefinition) -> None:
        if self.namespace_stack.isempty():
            full_name = node.name
            c_name = f"struct {node.name}"
        else:
            full_name = "::".join(self.namespace_stack.items()) + f"::{node.name}"
            c_name = f"struct {'_'.join(self.namespace_stack.items())}_{node.name}"

        struct_type = ShardType(full_name, c_name)
        self.type_table.add_type(struct_type)

        self.resolve_type(node.body)

    def resolve_NodeNamespaceDefinition(self, node: NodeNamespaceDefinition) -> None:
        ns_name = node.name.name if hasattr(node.name, "name") else node.name

        if self.namespace_stack.isempty():
            full_name = ns_name
            c_name = f"__shardc_namespace_{ns_name}"
        else:
            full_name = "::".join(self.namespace_stack.items()) + f"::{ns_name}"
            c_name = "_".join(self.namespace_stack.items()) + f"_{ns_name}"

        namespace_type = ShardType(full_name, c_name)
        self.type_table.add_type(namespace_type, check=False)

        self.namespace_stack.push(ns_name)
        self.resolve_type(node.content)
        self.namespace_stack.pop()