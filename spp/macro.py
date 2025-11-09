import re

class SPPMacro:
    def __init__(self, name: str, pattern: str, replacement: str):
        self.name = name
        self.pattern = pattern
        self.replacement = replacement
        self.regex = self.compile_pattern(pattern)

    def compile_pattern(self, pattern: str) -> re.Pattern:
        regex = re.escape(pattern)
        regex = re.sub(r'\\\$([a-zA-Z_][a-zA-Z0-9_]*)', r'(?P<\1>.+?)', regex)
        regex = regex.replace(r'\ ', r'\s+')
        return re.compile(regex)

    def expand(self, text: str) -> str:
        def repl(match):
            result = self.replacement
            for name, value in match.groupdict().items():
                result = result.replace(f"${name}", value)
            return result
        return self.regex.sub(repl, text)