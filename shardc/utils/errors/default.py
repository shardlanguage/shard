import sys

from shardc.utils.errors.classes import error_types

class ShardError:
    def __init__(self, errclass: int, msg: str):
        self.errclass = errclass
        self.msg = msg

        self.display()

    def display(self) -> None:
        errt = error_types[self.errclass]
        print(f"{errt}: {self.msg}")
        sys.exit(1)