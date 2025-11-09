from shardc.backend.visitor import Visitor
from shardc.frontend.symbols.function import ShardFunction
from shardc.frontend.symbols.structure import ShardStructure
from shardc.frontend.symbols.table import SymbolTable
from shardc.frontend.symbols.variable import ShardVariable
from shardc.frontend.tree.codeblocks import NodeCodeBlock
from shardc.frontend.tree.declarations import NodeExternDeclaration, NodeVariableDeclaration
from shardc.frontend.tree.expressions import NodeArrayAccess, NodeArrayAssignmentOp, NodeAssignmentOp, NodeBinaryOp, NodeCast, NodeFieldAccess, NodeFieldAssignmentOp, NodeFunctionCall, NodeGroupOp, NodeIDAccess, NodeUnaryOp
from shardc.frontend.tree.condition_struct import NodeIf, NodeElif, NodeElse, NodeCondition
from shardc.frontend.tree.flow_control import NodeReturn
from shardc.frontend.tree.function_def import NodeFunctionDefinition
from shardc.frontend.tree.loop_struct import NodeLoopForever, NodeLoopWhile, NodeLoopUntil
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

    def resolve_NodeIDAccess(self, node: NodeIDAccess) -> None:
        symbol = self.symbol_table.get_symbol(node.name)
        node.symbol = symbol

    def resolve_NodeArrayAccess(self, node: NodeArrayAccess) -> None:
        symbol = self.symbol_table.get_symbol(node.name)
        node.symbol = symbol

        self.resolve_symbol(node.index)

    def resolve_NodeFunctionCall(self, node: NodeFunctionCall) -> None:
        symbol = self.symbol_table.get_symbol(node.name)
        node.symbol = symbol

        for param in node.parameters:
            self.resolve_symbol(param)

    def resolve_NodeUnaryOp(self, node: NodeUnaryOp) -> None:
        self.resolve_symbol(node.right)

    def resolve_NodeBinaryOp(self, node: NodeBinaryOp) -> None:
        self.resolve_symbol(node.left)
        self.resolve_symbol(node.right)

    def resolve_NodeAssignmentOp(self, node: NodeAssignmentOp) -> None:
        symbol = self.symbol_table.get_symbol(node.name)
        node.symbol = symbol

        self.resolve_symbol(node.value)

    def resolve_NodeFieldAccess(self, node: NodeFieldAccess) -> None:
        symbol = self.symbol_table.get_symbol(node.instance)
        node.symbol = symbol

        if isinstance(node.symbol, ShardStructure):
            old_table = self.symbol_table
            self.symbol_table = node.symbol.symbol_table
            self.resolve_symbol(node.field)
            self.symbol_table = old_table

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

        structure = ShardStructure(node.name, local_table)
        self.symbol_table.add_symbol(structure)
        node.symbol = structure

        self.resolve_symbol(node.body)

        self.symbol_table = old_table