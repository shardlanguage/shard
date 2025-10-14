from shardc.frontend.symbols.symbol import Symbol
from shardc.utils.errors.symbols import ShardError_SymbolRedefined, ShardError_UnknownSymbol

class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def add_symbol(self, symbol: Symbol) -> None:
        if symbol.name in self.symbols:
            ShardError_SymbolRedefined(symbol.name).display()

        self.symbols[symbol.name] = symbol

    def get_symbol(self, name: str) -> Symbol:
        if name not in self.symbols:
            ShardError_UnknownSymbol(name).display()

        return self.symbols[name]