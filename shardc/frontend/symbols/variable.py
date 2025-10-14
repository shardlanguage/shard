from shardc.frontend.symbols.symbol import Symbol

class ShardVariable(Symbol):
    def __init__(self, prefix: str, name: str, t: str):
        self.prefix = prefix
        self.name = name
        self.t = t