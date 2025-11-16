from __future__ import annotations

from shardc.frontend.symbols.symbol import ShardSymbol
from shardc.frontend.symbols.table import SymbolTable

class ShardNamespace(ShardSymbol):
    def __init__(self, name: str, symbol_table: SymbolTable, parent: ShardNamespace | None = None):
        self.name = name
        self.symbol_table = symbol_table
        self.parent = parent

    def __repr__(self) -> str:
        return f"ShardNamespace(name={self.name}, symbol_table={self.symbol_table}, parent={self.parent})"