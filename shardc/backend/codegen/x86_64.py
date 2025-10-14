from shardc.backend.codegen.architecure import Architecture

class x86_64(Architecture):
    name = "x86_64"
    word_size = 64

    section_text = []
    section_data = []
    section_bss = []
    section_rodata = []

    def section(self, name: str) -> str:
        return f"\nsection .{name}\n"

    def integer(self, value) -> None:
        self.section_text.append(f"mov rax, {value}")

    def signed_value(self) -> None:
        self.section_text.append("neg rax")

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
        self.section_text.append("idiv rbx")

    def modulo(self) -> None:
        self.section_text.append("xor rdx, rdx")
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
        self.section_text.append("sar rax, cl")

    def push(self) -> None:
        self.section_text.append("push rax")

    def pop(self) -> None:
        self.section_text.append("pop rbx")

    def define_variable(self, name, size, value) -> None:
        sizes = {
            8: "db",
            16: "dw",
            32: "dd",
            64: "dq"
        }
        self.section_data.append(f"{name}: {sizes[size.size]} {value}")

    def access_value(self, address) -> None:
        self.section_text.append(f"mov rax, [{address}]")