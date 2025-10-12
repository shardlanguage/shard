from abc import ABC, abstractmethod

class Architecture(ABC):
    name: str = "unknown"
    word_size: int = 0

    @abstractmethod
    def integer(self, value) -> str: ...

    @abstractmethod
    def signed_value(self) -> str: ...

    @abstractmethod
    def add(self) -> str: ...

    @abstractmethod
    def sub(self) -> str: ...

    @abstractmethod
    def mul(self) -> str: ...

    @abstractmethod
    def div(self) -> str: ...

    @abstractmethod
    def modulo(self) -> str: ...

    @abstractmethod
    def bitwise_and(self) -> str: ...

    @abstractmethod
    def bitwise_or(self) -> str: ...

    @abstractmethod
    def bitwise_xor(self) -> str: ...

    @abstractmethod
    def bitwise_not(self) -> str: ...

    @abstractmethod
    def shift_left(self) -> str: ...

    @abstractmethod
    def shift_right(self) -> str: ...

    @abstractmethod
    def push(self) -> str: ...

    @abstractmethod
    def pop(self) -> str: ...