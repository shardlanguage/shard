from shardc.utils.errors.classes import ErrorClass
from shardc.utils.errors.default import ShardError

class ShardError_SymbolRedefined(ShardError):
    def __init__(self, name: str):
        super().__init__(ErrorClass.ERROR, f"symbol already defined: {name}")

class ShardError_UnknownSymbol(ShardError):
    def __init__(self, name: str):
        super().__init__(ErrorClass.ERROR, f"symbol used but not defined: {name}")