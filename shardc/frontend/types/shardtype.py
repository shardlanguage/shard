from __future__ import annotations

class ShardType:
    def __init__(self, name: str, c: str, length: int=0, nderefs: int=0):
        self.name = name
        self.c = c
        self.length = length
        self.nderefs = nderefs

    def clone(self) -> ShardType:
        t = ShardType(self.name, self.c, self.length, self.nderefs)
        return t