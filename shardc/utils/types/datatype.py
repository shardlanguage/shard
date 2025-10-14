class ShardType:
    def __init__(self, name: str, size: int, signed: bool=True):
        self.name = name
        self.size = size
        self.signed = signed