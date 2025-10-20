from shardc.frontend.symbols.symbol import Symbol
from shardc.utils.types.datatype import ShardType

class ShardVariable(Symbol):
    def __init__(self, prefix: str, name: str, t: ShardType, length: int=0):
        self.prefix = prefix
        self.name = name
        self.t = t
        self.length = length