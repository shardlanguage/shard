# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains functions used to convert Shard code to C code.
# =====================================================================

type_map = {
    'byte': 'int8_t', 'ubyte': 'uint8_t',
    'word': 'int16_t', 'uword': 'uint16_t',
    'dword': 'int32_t', 'udword': 'uint32_t',
    'qword': 'int64_t', 'uqword': 'uint64_t',
    'float': 'float', 'double': 'double',
    'void': 'void', 'string': 'char*'
}

# Convert a Shard type to a C type
def shard_type_to_c(shard_type):
    global type_map
    if shard_type not in type_map:
        raise ValueError(f"Invalid data type: {shard_type}")

    return type_map[shard_type]