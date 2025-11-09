from shardc.utils.errors.default import ShardError

class ShardError_IllegalCharacter(ShardError):
    def __init__(self, line: int, pos: int, c: int):
        super().__init__(f"illegal character: {c}\n- line: {line}\n- position: {pos}")

class ShardError_BadSyntax(ShardError):
    def __init__(self, code: str, line: int):
        super().__init__(f"syntax error: {code}\n- line: {line}")

class ShardError_EOF(ShardError):
    def __init__(self):
        super().__init__("syntax error at EOF")