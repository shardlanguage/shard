class SymbolTable:
    def __init__(self):
        self.content = {}

    def find_symbol(self, name) -> bool:
        return name in self.content

    def add_variable(self, variable: 'Variable'):
        if variable.name in self.content:
            raise ValueError(f"Variable '{variable.name}' already defined.")
        self.content[variable.name] = variable

    def get_variable(self, name) -> 'Variable':
        if name not in self.content:
            raise KeyError(f"Variable '{name}' not found.")
        return self.content[name]

    def __repr__(self):
        return "Symbol table:\n" + "\n".join(
            [str(v) for v in self.content.values()]
        )

class Variable:
    def __init__(self, datatype, name, value, is_const: bool):
        self.datatype = datatype
        self.name = name
        self.value = value
        self.is_const = is_const

    def __repr__(self):
        return f"Variable {self.name} of type {self.datatype} = {self.value} and is_const = {self.is_const}"