from shardc.backend.visitor import CodeGenerator
from shardc.frontend.nodes.node import Node
from shardc.frontend.symbols.resolver import SymbolResolver

class Compiler:
    def __init__(self, symbol_resolver: SymbolResolver, cg: CodeGenerator):
        self.symbol_resolver = symbol_resolver
        self.cg = cg

    def compile_node(self, node: Node) -> None:
        self.symbol_resolver.resolve_symbols(node)
        self.cg.generate(node)