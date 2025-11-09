from shardc.utils.errors.default import ShardError

class ShardError_SymbolRedeclared(ShardError):
    def __init__(self, symbol: str):
        super().__init__(f"symbol redeclared: {symbol}")

class ShardError_UnknownSymbol(ShardError):
    def __init__(self, symbol: str):
        super().__init__(f"unknown symbol: {symbol}")