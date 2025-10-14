from shardc.utils.errors.types import ShardError_TypeUnknown
from shardc.utils.types.datatype import ShardType

class TypeTable:
    def __init__(self):
        self.types = {
            "i8": ShardType("i8", 8),
            "i16": ShardType("i16", 16),
            "i32": ShardType("i32", 32),
            "i64": ShardType("i64", 64),
            "u8": ShardType("u8", 8, signed=False),
            "u16": ShardType("u16", 16, signed=False),
            "u32": ShardType("u32", 32, signed=False),
            "u64": ShardType("u64", 64, signed=False)
        }

    def get_type(self, name: str) -> ShardType:
        if name not in self.types:
            ShardError_TypeUnknown(name).display()

        return self.types[name]