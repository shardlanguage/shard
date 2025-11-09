from shardc.utils.errors.default import ShardError

class ShardError_InvalidStructContent(ShardError):
    def __init__(self, node: str):
        super().__init__(f"node not allowed in structure definitions: {node}")

class ShardError_NestedFunctions(ShardError):
    def __init__(self, base: str, nested: str):
        super().__init__(f"nested function in {base}: {nested}")