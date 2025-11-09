from __future__ import annotations

from shardc.frontend.types.shardtype import ShardType
from shardc.utils.constants.types import C_BOOL, C_CHAR, C_F32, C_F64, C_I16, C_I32, C_I64, C_I8, C_INT, C_LONG, C_SHORT, C_SIZE, C_U16, C_U32, C_U64, C_U8, C_UCHAR, C_UINT, C_ULONG, C_USHORT, C_USIZE, C_VOID, C_VOIDPTR, S_BOOL, S_CHAR, S_F32, S_F64, S_I16, S_I32, S_I64, S_I8, S_INT, S_LONG, S_SHORT, S_SIZE, S_U16, S_U32, S_U64, S_U8, S_UCHAR, S_UINT, S_ULONG, S_USHORT, S_USIZE, S_VOID, S_VOIDPTR
from shardc.utils.errors.types import ShardError_TypeRedefined, ShardError_UnknownType

class TypeTable:
    def __init__(self, parent: TypeTable | None = None):
        self.parent = parent
        self.table = {
            S_I8:  ShardType(S_I8,  C_I8),
            S_U8:  ShardType(S_U8,  C_U8),
            S_I16: ShardType(S_I16, C_I16),
            S_U16: ShardType(S_U16, C_U16),
            S_I32: ShardType(S_I32, C_I32),
            S_U32: ShardType(S_U32, C_U32),
            S_I64: ShardType(S_I64, C_I64),
            S_U64: ShardType(S_U64, C_U64),
            S_F32: ShardType(S_F32, C_F32),
            S_F64: ShardType(S_F64, C_F64),
            S_VOIDPTR: ShardType(S_VOIDPTR, C_VOIDPTR),
            S_BOOL: ShardType(S_BOOL, C_BOOL),

            S_CHAR: ShardType(S_CHAR, C_CHAR),
            S_SHORT: ShardType(S_SHORT, C_SHORT),
            S_INT: ShardType(S_INT, C_INT),
            S_LONG: ShardType(S_LONG, C_LONG),
            S_UCHAR: ShardType(S_UCHAR, C_UCHAR),
            S_USHORT: ShardType(S_USHORT, C_USHORT),
            S_UINT: ShardType(S_UINT, C_UINT),
            S_ULONG: ShardType(S_ULONG, C_ULONG),
            S_VOID: ShardType(S_VOID, C_VOID),
            S_SIZE: ShardType(S_SIZE, C_SIZE),
            S_USIZE: ShardType(S_USIZE, C_USIZE)
        }

    def add_type(self, t: ShardType) -> None:
        if t.name in self.table:
            ShardError_TypeRedefined(t.name).display()

        self.table[t.name] = t

    def add_array_type(self, t: ShardType) -> None:
        tname = f"[{t.length}]{t.name}"
        if tname in self.table:
            ShardError_TypeRedefined(t.name).display()

        self.table[tname] = t

    def add_deref_type(self, t: ShardType) -> None:
        tname = f"{'*'*t.nderefs}{t.name}"
        if tname in self.table:
            ShardError_TypeRedefined(t.name).display()

        self.table[tname] = t

    def remove_type(self, name: str) -> None:
        if name not in self.table:
            ShardError_UnknownType(name).display()

        self.table.pop(name)

    def get_type(self, name: str) -> ShardType:
        if name in self.table:
            return self.table[name]
        elif self.parent is not None:
            return self.parent.get_type(name)
        else:
            ShardError_UnknownType(name).display()