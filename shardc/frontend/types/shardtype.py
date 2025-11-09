class ShardType:
    def __init__(self, name: str, c: str, length: int=0, nderefs: int=0):
        self.name = name
        self.c = c
        self.length = length
        self.nderefs = nderefs