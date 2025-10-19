from shardc.backend.visitor import CodeGenerator
from shardc.frontend.nodes.node import Node
from shardc.frontend.optimizations.constant_folder import ConstantFolder
from shardc.frontend.symbols.resolver import SymbolResolver

class Compiler:
    def __init__(self, constant_folder: ConstantFolder, symbol_resolver: SymbolResolver, cg: CodeGenerator):
        self.constant_folder = constant_folder
        self.symbol_resolver = symbol_resolver
        self.cg = cg

    def compile_node(self, node: Node) -> None:
        self.constant_folder.fold_constants(node)
        self.symbol_resolver.resolve_symbols(node)
        self.cg.generate(node)