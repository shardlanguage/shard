from shardc.backend.visitor import Visitor
from shardc.frontend.symbols.function import ShardFunction
from shardc.frontend.symbols.namespace import ShardNamespace
from shardc.frontend.symbols.structure import ShardStructure
from shardc.frontend.symbols.table import SymbolTable
from shardc.frontend.symbols.variable import ShardVariable
from shardc.frontend.tree.codeblocks import NodeCodeBlock, NodeNamespaceBody, NodeStructureBody
from shardc.frontend.tree.declarations import NodeExternDeclaration, NodeVariableDeclaration
from shardc.frontend.tree.expressions import NodeArrayAccess, NodeArrayAssignmentOp, NodeAssignmentOp, NodeBinaryOp, NodeCast, NodeFieldAccess, NodeFieldAssignmentOp, NodeFunctionCall, NodeGroupOp, NodeIDAccess, NodeNamespaceAccess, NodeNamespaceAssignmentOp, NodeUnaryOp
from shardc.frontend.tree.condition_struct import NodeIf, NodeElif, NodeElse, NodeCondition
from shardc.frontend.tree.flow_control import NodeReturn
from shardc.frontend.tree.function_def import NodeFunctionDefinition
from shardc.frontend.tree.loop_struct import NodeLoopFor, NodeLoopForever, NodeLoopWhile, NodeLoopUntil
from shardc.frontend.tree.namespace_def import NodeNamespaceDefinition
from shardc.frontend.tree.node import Node
from shardc.frontend.tree.structure_def import NodeStructureDefinition

class SymbolResolver(Visitor):
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        super().__init__("resolve")

    def resolve_symbol(self, node: Node) -> None:
        if isinstance(node, list):
            for n in node:
                n.accept(self)
        else:
            if node is not None:
                node.accept(self)

    def _resolve_scoped_name(self, node: NodeNamespaceAccess) -> list[str]:
        parts = []

        if isinstance(node.namespace, NodeIDAccess):
            parts.append(node.namespace.name)
        elif isinstance(node.namespace, NodeNamespaceAccess):
            parts.extend(self._resolve_scoped_name(node.namespace))
        else:
            parts.append(str(node.namespace))

        if isinstance(node.sym, NodeIDAccess):
            parts.append(node.sym.name)
        elif isinstance(node.sym, NodeNamespaceAccess):
            parts.extend(self._resolve_scoped_name(node.sym))
        else:
            parts.append(str(node.sym))

        return parts

    def _get_scoped_symbol(self, full_name: str):
        parts = full_name.split("::")
        table = self.symbol_table.get_root()
        symbol = None

        for part in parts:
            symbol = table.get_symbol(part, error=False)
            if symbol is None:
                return None
            if isinstance(symbol, ShardNamespace):
                table = symbol.symbol_table

        return symbol

    def resolve_NodeIDAccess(self, node: NodeIDAccess) -> None:
        symbol = self.symbol_table.get_symbol(node.name)
        node.symbol = symbol

    def resolve_NodeArrayAccess(self, node: NodeArrayAccess) -> None:
        symbol = self.symbol_table.get_symbol(node.name)
        node.symbol = symbol

        self.resolve_symbol(node.index)

    def resolve_NodeFieldAccess(self, node: NodeFieldAccess) -> None:
        def _extract_base_type(t: str) -> str:
            while t.endswith("*"):
                t = t[:-1]

            while t.endswith("]"):
                i = t.rfind("[")
                if i == -1:
                    break
                t = t[:i]

            return t

        self.resolve_symbol(node.instance)
        instance_symbol = getattr(node.instance, "symbol", None)

        if instance_symbol is None:
            node.symbol = None
            return

        typename = instance_symbol.t
        base_type = _extract_base_type(typename)

        if "::" in base_type:
            struct_symbol = self._get_scoped_symbol(base_type)
        else:
            table = self.symbol_table
            struct_symbol = None
            while table is not None:
                sym = table.get_symbol(base_type, error=False)
                if isinstance(sym, ShardStructure):
                    struct_symbol = sym
                    break
                table = getattr(table, "parent", None)

        if not isinstance(struct_symbol, ShardStructure):
            node.symbol = None
            return

        field_name = node.field.name
        field_symbol = struct_symbol.symbol_table.get_symbol(field_name, error=False)

        node.field.symbol = field_symbol
        node.symbol = field_symbol

    def resolve_NodeNamespaceAccess(self, node: NodeNamespaceAccess) -> None:
        path = self._resolve_scoped_name(node)
        table = self.symbol_table
        symbol = None
        for part in path:
            symbol = table.get_symbol(part, error=False)
            if symbol is None:
                break
            if hasattr(symbol, "symbol_table"):
                table = symbol.symbol_table
        node.symbol = symbol
        if isinstance(node.sym, NodeIDAccess):
            node.sym.symbol = symbol

    def resolve_NodeFunctionCall(self, node: NodeFunctionCall):
        node.name.accept(self)
        target = node.name.symbol

        node.symbol = target

        for p in node.parameters:
            self.resolve_symbol(p)

    def resolve_NodeUnaryOp(self, node: NodeUnaryOp) -> None:
        self.resolve_symbol(node.right)

    def resolve_NodeBinaryOp(self, node: NodeBinaryOp) -> None:
        self.resolve_symbol(node.left)
        self.resolve_symbol(node.right)

    def resolve_NodeAssignmentOp(self, node: NodeAssignmentOp) -> None:
        symbol = self.symbol_table.get_symbol(node.name)
        node.symbol = symbol

        self.resolve_symbol(node.value)

    def resolve_NodeArrayAssignmentOp(self, node: NodeArrayAssignmentOp) -> None:
        symbol = self.symbol_table.get_symbol(node.name)
        node.symbol = symbol

        self.resolve_symbol(node.index)
        self.resolve_symbol(node.value)

    def resolve_NodeFieldAssignmentOp(self, node: NodeFieldAssignmentOp) -> None:
        self.resolve_symbol(node.instance)

        symbol = self.symbol_table.get_symbol(node.instance.name)
        node.symbol = symbol

        if isinstance(node.symbol, ShardStructure):
            old_table = self.symbol_table
            self.symbol_table = node.symbol.symbol_table
            self.resolve_symbol(node.field)
            self.symbol_table = old_table

        self.resolve_symbol(node.value)

    def resolve_NodeNamespaceAssignmentOp(self, node: NodeNamespaceAssignmentOp) -> None:
        self.resolve_symbol(node.value)

        path = self._resolve_scoped_name(node.namespace)
        table = self.symbol_table
        target = None

        for part in path:
            target = table.get_symbol(part, error=False)
            if hasattr(target, "symbol_table"):
                table = target.symbol_table

        node.symbol = target

    def resolve_NodeCast(self, node: NodeCast) -> None:
        self.resolve_symbol(node.value)

    def resolve_NodeGroupOp(self, node: NodeGroupOp) -> None:
        node.group.accept(self)

    def resolve_NodeVariableDeclaration(self, node: NodeVariableDeclaration) -> None:
        variable = ShardVariable(node.name, node.prefix, node.shardt.name if node.shardt is not None else "_shardc_unknown_type")
        self.symbol_table.add_symbol(variable)
        node.symbol = variable

        if node.value is not None:
            self.resolve_symbol(node.value)

    def resolve_NodeExternDeclaration(self, node: NodeExternDeclaration) -> None:
        self.resolve_symbol(node.symbol)

    def resolve_NodeCodeBlock(self, node: NodeCodeBlock) -> None:
        local_table = SymbolTable(parent=self.symbol_table)
        old_table = self.symbol_table
        self.symbol_table = local_table
        for stmt in node.content:
            self.resolve_symbol(stmt)
        self.symbol_table = old_table

    def resolve_NodeStructureBody(self, node: NodeStructureBody) -> None:
        for stmt in node.content:
            self.resolve_symbol(stmt)

    def resolve_NodeNamespaceBody(self, node: NodeNamespaceBody) -> None:
        for stmt in node.content:
            if not isinstance(stmt, NodeNamespaceDefinition):
                self.resolve_symbol(stmt)

    def resolve_NodeIf(self, node: NodeIf) -> None:
        self.resolve_symbol(node.branch)

    def resolve_NodeElif(self, node: NodeElif) -> None:
        self.resolve_symbol(node.branch)

    def resolve_NodeElse(self, node: NodeElse) -> None:
        self.resolve_symbol(node.branch)

    def resolve_NodeCondition(self, node: NodeCondition) -> None:
        self.resolve_symbol(node.if_)
        if node.elif_ is not None:
            for nd in node.elif_:
                self.resolve_symbol(nd)
        if node.else_ is not None:
            self.resolve_symbol(node.else_)

    def resolve_NodeLoopForever(self, node: NodeLoopForever) -> None:
        self.resolve_symbol(node.branch)

    def resolve_NodeLoopWhile(self, node: NodeLoopWhile) -> None:
        self.resolve_symbol(node.branch)

    def resolve_NodeLoopUntil(self, node: NodeLoopUntil) -> None:
        self.resolve_symbol(node.branch)

    def resolve_NodeLoopFor(self, node: NodeLoopFor) -> None:
        self.resolve_symbol(node.declaration)
        self.resolve_symbol(node.condition)
        self.resolve_symbol(node.update)
        self.resolve_symbol(node.branch)

    def resolve_NodeReturn(self, node: NodeReturn) -> None:
        if node.value is not None:
            self.resolve_symbol(node.value)

    def resolve_NodeFunctionDefinition(self, node: NodeFunctionDefinition) -> None:
        function = ShardFunction(node.name, node.shardt.name if node.shardt is not None else "_shardc_unknown_type", len(node.parameters))
        self.symbol_table.add_symbol(function)
        node.symbol = function

        local_table = SymbolTable(parent=self.symbol_table)
        old_table = self.symbol_table
        self.symbol_table = local_table
        
        if len(node.parameters) != 0:
            for param in node.parameters:
                self.resolve_symbol(param)

        self.resolve_symbol(node.body)

        self.symbol_table = old_table

    def resolve_NodeStructureDefinition(self, node: NodeStructureDefinition) -> None:
        local_table = SymbolTable(parent=self.symbol_table)
        old_table = self.symbol_table

        self.symbol_table = local_table
        self.resolve_symbol(node.body)
        self.symbol_table = old_table

        structure = ShardStructure(node.name, local_table)
        self.symbol_table.add_symbol(structure)
        node.symbol = structure

    def resolve_NodeNamespaceDefinition(self, node: NodeNamespaceDefinition) -> None:
        existing = self.symbol_table.get_symbol(node.name, error=False)
        
        if isinstance(existing, ShardNamespace):
            namespace = existing
            local_table = namespace.symbol_table
        else:
            local_table = SymbolTable(parent=self.symbol_table)
            namespace = ShardNamespace(node.name, local_table)
            self.symbol_table.add_symbol(namespace, check=False)

        old_table = self.symbol_table
        self.symbol_table = local_table
        self.resolve_symbol(node.content)
        self.symbol_table = old_table

        namespace.symbol_table = old_table
        node.symbol = namespace