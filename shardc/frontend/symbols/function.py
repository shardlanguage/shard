from shardc.frontend.symbols.symbol import ShardSymbol

class ShardFunction(ShardSymbol):
    def __init__(self, name: str, t: str, nparams: int):
        self.name = name
        self.t = t
        self.nparams = nparams

    def __repr__(self) -> str:
        return f"ShardFunction(name={self.name}, t={self.t}, nparams={self.nparams})"