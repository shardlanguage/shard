import shlex

from spp.constants import CONST, INCLUDE, LIB_PATH, LIB_PREFIX, MACRO, MESSAGE, ROOTFILE, STATEMENT_START, UNDEF
from spp.error import SPPError_FileNotFound
from spp.macro import SPPMacro
from pathlib import Path

class ShardPreProcessor:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.symbol_table = {}
        self.macros = []
        self.included_files = []
        self.root = ROOTFILE
        self.output = []

    def find_root(self) -> Path:
        path = Path(self.input_file).resolve()
        for parent in [path.parent] + list(path.parents):
            if (parent / self.root).exists():
                return parent
        SPPError_FileNotFound(ROOTFILE).display()

    def process(self) -> None:
        with open(self.input_file, 'r') as file:
            content = file.read()

        lines = content.splitlines()
        output_lines = []

        for line in lines:
            if line.startswith(STATEMENT_START):
                parts = shlex.split(line)
                stmt_name = parts[0]
                stmt_args = parts[1:]
                self.execute_statement(stmt_name, *stmt_args)
            else:
                for name, value in self.symbol_table.items():
                    line = line.replace(name, value)

                for macro in self.macros:
                    line = macro.expand(line)

                output_lines.append(line)

        self.output.extend(output_lines)

    def execute_statement(self, statement: str, *args) -> None:
        statement_table = {
            CONST: self.execute_const,
            UNDEF: self.execute_undef,
            INCLUDE: self.execute_include,
            MESSAGE: self.execute_message,
            MACRO: self.execute_macro
        }

        statement_table[statement](*args)

    def execute_const(self, name: str, value: str) -> None:
        self.symbol_table[name] = value

    def execute_undef(self, name: str) -> None:
        self.symbol_table.pop(name)

    def execute_include(self, file: str) -> None:
        file = file.strip('"').strip("'") + ".sd"
        if file.startswith(LIB_PREFIX):
            file = LIB_PATH + file.split('/')[0] + '/' + file

        if file in self.included_files:
            return

        if not file.startswith(LIB_PATH):
            project_root = self.find_root()
            toinc = f"{project_root}/{file}"
        else:
            toinc = file.replace(LIB_PREFIX, '')
        self.included_files.append(file)

        local_spp = ShardPreProcessor(toinc)
        local_spp.included_files = self.included_files
        local_spp.process()

        self.symbol_table.update(local_spp.symbol_table)
        self.macros.extend(local_spp.macros)

        self.output.extend(local_spp.output)

    def execute_message(self, text: str) -> None:
        print(f"{text}")

    def execute_macro(self, name: str, pattern: str, replacement: str) -> None:
        pattern = pattern.strip('"').strip("'")
        replacement = replacement.strip('"').strip("'")
        macro = SPPMacro(name, pattern, replacement)
        self.macros.append(macro)