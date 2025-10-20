from shardc.frontend.nodes.declaration import NodeVariableDecl
from shardc.frontend.nodes.expression import NodeAssignOp, NodeBinaryOp, NodeGroup, NodeID, NodeUnaryOp
from shardc.frontend.symbols.variable import ShardVariable
from shardc.frontend.symbols.table import SymbolTable
from shardc.frontend.nodes.node import Node
from shardc.utils.types.table import TypeTable

class SymbolResolver:
    def __init__(self, symbol_table: SymbolTable, type_table: TypeTable):
        self.symbol_table = symbol_table
        self.type_table = type_table

    def resolve_symbols(self, node: Node) -> None:
        function_name = f"resolve_{type(node).__name__}"
        function = getattr(self, function_name, self.generic_resolve)
        function(node)

    def generic_resolve(self, node: Node) -> None:
        pass

    def resolve_NodeID(self, node: NodeID) -> None:
        symbol = self.symbol_table.get_symbol(node.name)
        if node.idx:
            self.resolve_symbols(node.idx)
        node.symbol = symbol

    def resolve_NodeUnaryOp(self, node: NodeUnaryOp) -> None:
        self.resolve_symbols(node.right)

    def resolve_NodeBinaryOp(self, node: NodeBinaryOp) -> None:
        self.resolve_symbols(node.left)
        self.resolve_symbols(node.right)

    def resolve_NodeAssignOp(self, node: NodeAssignOp) -> None:
        if not isinstance(node.name, NodeID):
            symbol = self.symbol_table.get_symbol(node.name)
        else:
            symbol = self.symbol_table.get_symbol(node.name.name)
        node.symbol = symbol

        self.resolve_symbols(node.val)

    def resolve_NodeGroup(self, node: NodeGroup) -> None:
        self.resolve_symbols(node.group)

    def resolve_NodeVariableDecl(self, node: NodeVariableDecl) -> None:
        if node.val is not None:
            self.resolve_symbols(node.val)

        if not isinstance(node.t, list):
            t = self.type_table.get_type(node.t)
            node.datatype = t
            var = ShardVariable(node.prefix, node.name, t)
        else:
            base_type = self.type_table.get_type(node.t[0])
            size = node.t[1]
            node.datatype = (base_type, size)
            var = ShardVariable(node.prefix, node.name, base_type, size)
            
        self.symbol_table.add_symbol(var)