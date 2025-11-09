from shardc.frontend.symbols.symbol import ShardSymbol

class ShardVariable(ShardSymbol):
    def __init__(self, name: str, prefix: str, t: str):
        self.name = name
        self.prefix = prefix
        self.t = t

    def __repr__(self) -> str:
        return f"ShardVariable(name={self.name}, prefix={self.prefix}, type={self.t})"