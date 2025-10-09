from shardc.utils.errors.default import ShardError
from shardc.utils.errors.classes import ErrorClass

class ShardError_IllegalCharacter(ShardError):
    def __init__(self, char: str, line: int, position: int):
        super().__init__(ErrorClass.ERROR, f"illegal character: {char}\n- line: {line}\n- position: {position}")