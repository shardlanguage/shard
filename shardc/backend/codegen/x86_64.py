from shardc.backend.codegen.architecure import Architecture

class x86_64(Architecture):
    name = "x86_64"
    word_size = 64

    def integer(self, value) -> str:
        return f"mov rax, {value}"

    def signed_value(self) -> str:
        return "neg rax"

    def add(self) -> str:
        return "add rax, rbx"

    def sub(self) -> str:
        return '\n'.join([
            "sub rbx, rax",
            "mov rax, rbx"
        ])

    def mul(self) -> str:
        return "imul rax, rbx"

    def div(self) -> str:
        return '\n'.join([
            "xor rdx, rdx",
            "idiv rbx"
        ])

    def modulo(self) -> str:
        return '\n'.join([
            "xor rdx, rdx",
            "idiv rbx",
            "mov rax, rdx"
        ])

    def bitwise_and(self) -> str:
        return "and rax, rbx"

    def bitwise_or(self) -> str:
        return "or rax, rbx"

    def bitwise_xor(self) -> str:
        return "xor rax, rbx"

    def bitwise_not(self) -> str:
        return "not rax"

    def shift_left(self) -> str:
        return '\n'.join([
            "mov rcx, rbx",
            "shl rax, cl"
        ])

    def shift_right(self) -> str:
        return '\n'.join([
            "mov rcx, rbx",
            "sar rax, cl"
        ])

    def push(self) -> str:
        return "push rax"

    def pop(self) -> str:
        return "pop rbx"