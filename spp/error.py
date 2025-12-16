import sys

from spp.colors import ANSIColors
from spp.colors import colorize

class SPPError:
    def __init__(self, message: str):
        self.message = message

    def display(self):
        print(f"[spp] {colorize(ANSIColors.BOLD_RED, "error")}: {self.message}")
        sys.exit(1)

class SPPError_FileNotFound(SPPError):
    def __init__(self, filename: str):
        super().__init__(f"unable to find file: {filename}")