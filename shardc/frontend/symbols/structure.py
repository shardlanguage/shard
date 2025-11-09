from shardc.frontend.symbols.symbol import ShardSymbol
from shardc.frontend.symbols.table import SymbolTable

class ShardStructure(ShardSymbol):
    def __init__(self, name: str, symbol_table: SymbolTable):
        self.name = name
        self.symbol_table = symbol_table

    def __repr__(self) -> str:
        return f"ShardStructure(name={self.name}, symbol_table={self.symbol_table})"