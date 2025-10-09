from shardc.utils.errors.classes import ErrorClass
from shardc.utils.errors.default import ShardError

class ShardError_FileNotFound(ShardError):
    def __init__(self, path: str):
        super().__init__(ErrorClass.ERROR, f"file not found: {path}")

class ShardError_IsADirectory(ShardError):
    def __init__(self, path: str):
        super().__init__(ErrorClass.ERROR, f"{path} is a directory")