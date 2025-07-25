class Value:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"<Value: {self.value}>"

class VariableAccess:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<VariableAccess: {self.name}>"

class ArrayAccess:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        return f"ArrayAccess: {self.name}, {self.index}"

class UnaryOp:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"<UnaryOp: {self.operator}, {self.right}>"

class BinaryOp:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"<BinaryOp: {self.left}, {self.operator}, {self.right}>"

class VariableAssignment:
    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator
        self.value = value

    def __repr__(self):
        return f"<VariableAssignment: {self.name}, {self.operator}, {self.value}>"

class ArrayAssignment:
    def __init__(self, name, index, operator, value):
        self.name = name
        self.index = index
        self.operator = operator
        self.value = value

    def __repr__(self):
        return f"<ArrayAssignment: {self.name}, {self.operator}, {self.value}>"

class Group:
    def __init__(self, group):
        self.group = group

    def __repr__(self):
        return f"<Group: {self.group}>"

class VariableDeclaration:
    def __init__(self, type_modifier, primary_type, name, value):
        self.type_modifier = type_modifier
        self.primary_type = primary_type
        self.name = name
        self.value = value

    def __repr__(self):
        return f"<VariableDeclaration: {self.type_modifier}, {self.primary_type}, {self.name}, {self.value}>"

class ArrayDeclaration:
    def __init__(self, type_modifier, primary_type, name, size, content):
        self.type_modifier = type_modifier
        self.primary_type = primary_type
        self.name = name
        self.size = size
        self.content = content

    def __repr__(self):
        return f"<ArrayDeclaration: {self.type_modifier}, {self.primary_type}, {self.name}, {self.size}, {self.content}>"

class CodeBlock:
    def __init__(self, statement_list):
        self.statement_list = statement_list

    def __repr__(self):
        return f"<CodeBlock: {self.statement_list}>"

class Condition:
    def __init__(self, condition, if_branch, else_branch):
        self.condition = condition
        self.if_branch = if_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"<Condition: {self.condition}, {self.if_branch}, {self.else_branch}>"

class LoopUnconditionnal:
    def __init__(self, statement_list):
        self.statement_list = statement_list

    def __repr__(self):
        return f"<LoopUnconditionnal: {self.statement_list}>"

class LoopConditionnal:
    def __init__(self, looptype, condition, branch):
        self.looptype = looptype
        self.condition = condition
        self.branch = branch

    def __repr__(self):
        return f"<LoopConditionnal: {self.looptype}, {self.condition}, {self.branch}>"