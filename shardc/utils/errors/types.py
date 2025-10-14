from shardc.utils.errors.classes import ErrorClass
from shardc.utils.errors.default import ShardError

class ShardError_TypeUnknown(ShardError):
    def __init__(self, name: str):
        super().__init__(ErrorClass.ERROR, f"unknown data type: {name}")