from shardc.utils.errors.default import ShardError

class ShardError_BreakOutsideOfLoop(ShardError):
    def __init__(self):
        super().__init__("break used outisde of a loop")

class ShardError_ContinueOutsideOfLoop(ShardError):
    def __init__(self):
        super().__init__("continue used outside of a loop")

class ShardError_ReturnOutsideOfFunction(ShardError):
    def __init__(self):
        super().__init__("return used outside of a function")