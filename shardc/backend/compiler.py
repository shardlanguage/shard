from shardc.backend.generator import CodeGenerator
from shardc.frontend.optimizations.content_verifier import ContentVerifier
from shardc.frontend.optimizations.context_checker import ContextChecker
from shardc.frontend.optimizations.symbol_resolver import SymbolResolver
from shardc.frontend.tree.node import Node
from shardc.frontend.optimizations.type_resolver import TypeResolver

class Compiler:
    def __init__(self, code_generator: CodeGenerator,
                type_resolver: TypeResolver,
                symbol_resolver: SymbolResolver,
                context_checker: ContextChecker,
                content_verifier: ContentVerifier,
                std: bool=True
        ):
        self.content_verifier = content_verifier
        self.context_checker = context_checker
        self.type_resolver = type_resolver
        self.symbol_resolver = symbol_resolver
        self.code_generator = code_generator
        self.std = std
        self.code = []

    def add_preamble(self) -> None:
        preamble = self.code_generator.lang.preamble(extra_includes=self.std)
        self.code.append(preamble)

    def compile_node(self, node: Node) -> None:
        self.content_verifier.verify_content(node)
        self.context_checker.check_context(node)
        self.type_resolver.resolve_type(node)
        self.symbol_resolver.resolve_symbol(node)
        code = self.code_generator.generate(node, statement=True)

        self.code.append(code)