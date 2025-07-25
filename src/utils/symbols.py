# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains the symbol-related classes.
# =====================================================================

# Symbol table class
# Can store variables/arrays and functions
class SymbolTable:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent

    # Find a variable in the variables table
    def find_variable(self, name) -> bool:
        return name in self.variables or (self.parent and self.parent.find_variable(name))

    # Add a variable to the variables table
    def add_variable(self, variable: 'Variable'):
        if variable.name in self.variables:
            raise ValueError(f"Variable '{variable.name}' already defined in this scope.")
        self.variables[variable.name] = variable

    # Get a variable from the variables table
    def get_variable(self, name) -> 'Variable':
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get_variable(name)
        else:
            raise KeyError(f"Variable '{name}' not found.")

    # Get the size of an array from the variables table
    def get_size(self, name) -> int:
        var = self.get_variable(name)
        if var.size is None:
            raise AttributeError(f"Variable '{name}' has no size (not an array?)")
        return var.size

    # Find a function in the functions table
    def find_function(self, name) -> bool:
        return name in self.functions or (self.parent and self.parent.find_function(name))

    # Add a function to the functions table
    def add_function(self, function: 'Function'):
        if function.name in self.functions:
            raise ValueError(f"Function '{function.name}' already defined.")
        self.functions[function.name] = function

    # Get a function from the functions table
    def get_function(self, name) -> 'Function':
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            raise KeyError(f"Function '{name}' not found.")

    def __repr__(self):
        lines = ["Symbol Table:"]
        lines += [f"  Variable {v}" for v in self.variables.values()]
        lines += [f"  Function {f}" for f in self.functions.values()]
        return "\n".join(lines)

# A variable
class Variable:
    def __init__(self, datatype, name, value, is_const: bool, size=None):
        self.datatype = datatype
        self.name = name
        self.value = value
        self.is_const = is_const
        self.size = size

    def __repr__(self):
        return f"Variable {self.name} of type {self.datatype} and size (if array) {self.size} = {self.value} and is_const = {self.is_const}"

# A function
class Function:
    def __init__(self, return_type, name, parameters, body):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"Function {self.name} of type {self.return_type} with parameters {self.parameters} and body {self.body}"