from shardc.utils.errors.default import ShardError

class ShardError_FileNotFound(ShardError):
    def __init__(self, file: str):
        super().__init__(f"file not found: {file}")

class ShardError_IsADirectory(ShardError):
    def __init__(self, directory: str):
        super().__init__(f"is a directory: {directory}")