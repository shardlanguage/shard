# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains the Shard PreProcessor (SPP) source code. The pre
# processor is used to edit source code before it is analyzed.
#
# The source code is modified in memory.
# =====================================================================

# Import modules
import os

# Shard PreProcessor parser class
class SPP_Parser:
    def __init__(self, code: str, base_dir: str):
        self.code = code
        self.base_dir = base_dir
        self.included_files = []
        self.instructions = ["@include"]

    # Parse a file
    def parse_file(self, filename):
        full_path = os.path.abspath(os.path.join(self.base_dir, filename))

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Include file not found: {full_path}")
        if full_path in self.included_files:
            return ""

        self.included_files.append(full_path)

        with open(full_path, "r") as f:
            content = f.read()

        sub_parser = SPP_Parser(content, os.path.dirname(full_path))
        return sub_parser.process()

    # Process instructions
    # Only instructions starting with @ are evaluated
    def process(self):
        lines = self.code.splitlines()
        output = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("@include"):
                parts = stripped.split(maxsplit=1)
                if len(parts) != 2:
                    raise SyntaxError("Missing filename in @include directive")
                include_path = parts[1].strip('"')
                included_code = self.parse_file(include_path)
                output.append(included_code)

            else:
                output.append(line)

        return "\n".join(output)