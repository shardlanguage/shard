import sys

from shardc.utils.style.colorize import colorize
from shardc.utils.style.colors import ANSIColors

class ShardError:
    def __init__(self, message: str):
        self.message = message

    def display(self):
        print(f"[shardc] {colorize(ANSIColors.BOLD_RED, "error")}: {self.message}")
        sys.exit(1)