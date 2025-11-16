from __future__ import annotations

from shardc.frontend.symbols.symbol import ShardSymbol
from shardc.utils.errors.symbols import ShardError_SymbolRedeclared, ShardError_UnknownSymbol

class SymbolTable:
    def __init__(self, parent: SymbolTable | None = None):
        self.parent = parent
        self.table = {}

    def add_symbol(self, symbol: ShardSymbol, check: bool=True) -> None:
        if check:
            if symbol.name in self.table:
                ShardError_SymbolRedeclared(symbol.name).display()
        
        self.table[symbol.name] = symbol

    def remove_symbol(self, name: str) -> None:
        if name not in self.table:
            ShardError_UnknownSymbol(name).display()

        self.table.pop(name)

    def get_symbol(self, name: str, error: bool=True) -> ShardSymbol | None:
        if name in self.table:
            return self.table[name]
        elif self.parent is not None:
            return self.parent.get_symbol(name)
        else:
            if error:
                ShardError_UnknownSymbol(name).display()
            else:
                return None

    def get_root(self) -> SymbolTable:
        t = self
        while t.parent is not None:
            t = t.parent
        return t