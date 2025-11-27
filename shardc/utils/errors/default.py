import sys

class ShardError:
    def __init__(self, message: str):
        self.message = message

    def display(self):
        print(f"error: {self.message}")
        sys.exit(1)