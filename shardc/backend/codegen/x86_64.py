from shardc.backend.codegen.architecure import Architecture
from shardc.utils.const.comparisons import EQUAL, GT_SIGNED, GT_UNSIGNED, GTQ_SIGNED, GTQ_UNSIGNED, LT_SIGNED, LT_UNSIGNED, LTQ_SIGNED, LTQ_UNSIGNED, NOT_EQUAL

class x86_64(Architecture):
    name = "x86_64"
    word_size = 64
    accumulator = "rax"
    register_b = "rbx"

    def __init__(self):
        self.section_text = []
        self.section_data = []
        self.section_bss = []
        self.section_rodata = []

    def section(self, name: str) -> str:
        return f"\nsection .{name}\n"

    def integer(self, value) -> None:
        self.section_text.append(f"mov rax, {value}")

    def signed_value(self) -> None:
        self.section_text.append("neg rax")

    def addr_offset(self, addr, offset) -> str:
        return f"{addr} + {offset}"

    def move_addr(self, addr) -> None:
        self.section_text.append(f"mov rax, [{addr}]")

    def store_addr(self, addr) -> None:
        self.section_text.append(f"mov [{addr}], rax")

    def add(self) -> None:
        self.section_text.append("add rax, rbx")

    def sub(self) -> None:
        self.section_text.append("sub rax, rbx")

    def mul(self) -> None:
        self.section_text.append("imul rax, rbx")

    def div(self) -> None:
        self.section_text.append("xor rdx, rdx")
        self.section_text.append("div rbx")

    def signed_div(self) -> None:
        self.section_text.append("cqo")
        self.section_text.append("idiv rbx")

    def modulo(self) -> None:
        self.section_text.append("xor rdx, rdx")
        self.section_text.append("div rbx")
        self.section_text.append("mov rax, rdx")

    def signed_modulo(self) -> None:
        self.section_text.append("cqo")
        self.section_text.append("idiv rbx")
        self.section_text.append("mov rax, rdx")

    def bitwise_and(self) -> None:
        self.section_text.append("and rax, rbx")

    def bitwise_or(self) -> None:
        self.section_text.append("or rax, rbx")

    def bitwise_xor(self) -> None:
        self.section_text.append("xor rax, rbx")

    def bitwise_not(self) -> None:
        self.section_text.append("not rax")

    def shift_left(self) -> None:
        self.section_text.append("mov rcx, rbx")
        self.section_text.append("shl rax, cl")

    def shift_right(self) -> None:
        self.section_text.append("mov rcx, rbx")
        self.section_text.append("shr rax, cl")

    def signed_shift_right(self) -> None:
        self.section_text.append("mov rcx, rbx")
        self.section_text.append("sar rax, cl")

    def push(self) -> None:
        self.section_text.append("push rax")

    def pop(self) -> None:
        self.section_text.append("pop rbx")

    def define_variable(self, name, t, value) -> None:
        sizes = {
            8: "db",
            16: "dw",
            32: "dd",
            64: "dq"
        }
        self.section_data.append(f"{name}: {sizes[t.size]} {value}")

    def define_buffer(self, name, t, size) -> None:
        sizes = {
            8: "resb",
            16: "resw",
            32: "resd",
            64: "resq"
        }
        self.section_bss.append(f"{name}: {sizes[t.size]} {size}")

    def define_const(self, name, t, value) -> None:
        sizes = {
            8: "db",
            16: "dw",
            32: "dd",
            64: "dq"
        }
        self.section_rodata.append(f"{name}: {sizes[t.size]} {value}")

    def access_value(self, address) -> None:
        self.section_text.append(f"mov rax, [{address}]")

    def compare(self, comparison: int) -> None:
        table = {
            EQUAL: "sete al",
            NOT_EQUAL: "setne al",
            LT_SIGNED: "setl al",
            LT_UNSIGNED: "setb al",
            GT_SIGNED: "setg al",
            GT_UNSIGNED: "seta al",
            LTQ_SIGNED: "setle al",
            LTQ_UNSIGNED: "setbe al",
            GTQ_SIGNED: "setge al",
            GTQ_UNSIGNED: "setae al"
        }

        self.section_text.append("cmp rax, rbx")
        self.section_text.append(table.get(comparison))
        self.section_text.append("movzx rax, al")