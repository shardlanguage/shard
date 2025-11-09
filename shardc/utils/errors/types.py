from shardc.utils.errors.default import ShardError

class ShardError_TypeRedefined(ShardError):
    def __init__(self, t: str):
        super().__init__(f"type redefined: {t}")

class ShardError_UnknownType(ShardError):
    def __init__(self, t: str):
        super().__init__(f"unknown type: {t}")