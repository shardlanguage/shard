from abc import ABC, abstractmethod

class Architecture(ABC):
    name: str = "unknown"
    word_size: int = 0

    def __init__(self):
        self.section_text: list = []
        self.section_data: list = []
        self.section_bss: list = []
        self.section_rodata: list = []

    @abstractmethod
    def section(self, name: str) -> str: ...

    @abstractmethod
    def integer(self, value) -> None: ...

    @abstractmethod
    def signed_value(self) -> None: ...

    @abstractmethod
    def move_addr(self, addr) -> None: ...

    @abstractmethod
    def store_addr(self, addr) -> None: ...

    @abstractmethod
    def add(self) -> None: ...

    @abstractmethod
    def sub(self) -> None: ...

    @abstractmethod
    def mul(self) -> None: ...

    @abstractmethod
    def div(self) -> None: ...

    @abstractmethod
    def signed_div(self) -> None: ...

    @abstractmethod
    def modulo(self) -> None: ...

    @abstractmethod
    def signed_modulo(self) -> None: ...

    @abstractmethod
    def bitwise_and(self) -> None: ...

    @abstractmethod
    def bitwise_or(self) -> None: ...

    @abstractmethod
    def bitwise_xor(self) -> None: ...

    @abstractmethod
    def bitwise_not(self) -> None: ...

    @abstractmethod
    def shift_left(self) -> None: ...

    @abstractmethod
    def shift_right(self) -> None: ...

    @abstractmethod
    def signed_shift_right(self) -> None: ...

    @abstractmethod
    def push(self) -> None: ...

    @abstractmethod
    def pop(self) -> None: ...

    @abstractmethod
    def define_variable(self, name, t, value) -> None: ...

    @abstractmethod
    def define_buffer(self, name, t, size) -> None: ...

    @abstractmethod
    def define_const(self, name, t, value) -> None: ...

    @abstractmethod
    def access_value(self, address) -> None: ...

    @abstractmethod
    def compare(self, comparison: int) -> None: ...