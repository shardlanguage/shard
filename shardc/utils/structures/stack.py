from typing import Any

class Stack:
    def __init__(self):
        self.content = []

    def __len__(self):
        return len(self.content)

    def isempty(self) -> bool:
        return len(self.content) == 0

    def push(self, value: Any) -> None:
        self.content.append(value)

    def pop(self) -> Any:
        if not self.isempty():
            return self.content.pop()