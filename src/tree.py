# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains the Shard AST node types, represented by classes.
# =====================================================================

# Value <value>
class Value:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"<Value: {self.value}>"

# String <string>
class String:
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return f"<String: {self.string}>"

# Access to variable <name>
class VariableAccess:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<VariableAccess: {self.name}>"

# Access to index <index> of array <name>
class ArrayAccess:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        return f"ArrayAccess: {self.name}, {self.index}"

# Access to field <field> of structure instance <instance>
class StructInstanceFieldAccess:
    def __init__(self, instance, field):
        self.instance = instance
        self.field = field

    def __repr__(self):
        return f"<StructInstanceFieldAccess: {self.instance}, {self.field}>"

# Call function <name> with parameters <parameters>
class FunctionCall:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    def __repr__(self):
        return f"<FunctionCall: {self.name}, {self.parameters}>"

# Unary operation on <right> with <operator> operator
class UnaryOp:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"<UnaryOp: {self.operator}, {self.right}>"

# Binary operation on <left> and <right> with <operator> operator
class BinaryOp:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"<BinaryOp: {self.left}, {self.operator}, {self.right}>"

# Assign <value> to variable <name> with <operator> assignment operator
class VariableAssignment:
    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator
        self.value = value

    def __repr__(self):
        return f"<VariableAssignment: {self.name}, {self.operator}, {self.value}>"

# Assign <value> to index <index> of array <name> with <operator> assignment operator
class ArrayAssignment:
    def __init__(self, name, index, operator, value):
        self.name = name
        self.index = index
        self.operator = operator
        self.value = value

    def __repr__(self):
        return f"<ArrayAssignment: {self.name}, {self.operator}, {self.value}>"

# Assign <value> to field <field> of structure instance <instance> using assignment operator
# <operator>
class StructInstanceFieldAssignment:
    def __init__(self, instance, field, operator, value):
        self.instance = instance
        self.field = field
        self.operator = operator
        self.value = value

    def __repr__(self):
        return f"<StructInstanceFieldAssignment: {self.instance}, {self.operator}, {self.value}>"

# (group)
class Group:
    def __init__(self, group):
        self.group = group

    def __repr__(self):
        return f"<Group: {self.group}>"

# Declare variable <name> of type <type_modifier> <primary_type> and assign <value> to it
class VariableDeclaration:
    def __init__(self, type_modifier, primary_type, name, value):
        self.type_modifier = type_modifier
        self.primary_type = primary_type
        self.name = name
        self.value = value

    def __repr__(self):
        return f"<VariableDeclaration: {self.type_modifier}, {self.primary_type}, {self.name}, {self.value}>"

# Declare array <name> of size <size> and type <type_modifier> <primary_type> and assign <content> to it
class ArrayDeclaration:
    def __init__(self, type_modifier, primary_type, name, size, content):
        self.type_modifier = type_modifier
        self.primary_type = primary_type
        self.name = name
        self.size = size
        self.content = content

    def __repr__(self):
        return f"<ArrayDeclaration: {self.type_modifier}, {self.primary_type}, {self.name}, {self.size}, {self.content}>"

# {statement_list}
class CodeBlock:
    def __init__(self, statement_list):
        self.statement_list = statement_list

    def __repr__(self):
        return f"<CodeBlock: {self.statement_list}>"

# Execute <if_branch> if <condition> is true, else execute <else_branch>
class Condition:
    def __init__(self, condition, if_branch, else_branch):
        self.condition = condition
        self.if_branch = if_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"<Condition: {self.condition}, {self.if_branch}, {self.else_branch}>"

# Repeat forever the <statement_list> block
class LoopUnconditionnal:
    def __init__(self, statement_list):
        self.statement_list = statement_list

    def __repr__(self):
        return f"<LoopUnconditionnal: {self.statement_list}>"

# Repeat the <branch> block using the <looptype> loop if <condition> is true
class LoopConditionnal:
    def __init__(self, looptype, condition, branch):
        self.looptype = looptype
        self.condition = condition
        self.branch = branch

    def __repr__(self):
        return f"<LoopConditionnal: {self.looptype}, {self.condition}, {self.branch}>"

# statement [value]
class FlowControl:
    def __init__(self, statement, value):
        self.statement = statement
        self.value = value

    def __repr__(self):
        return f"<FlowControl: {self.statement}, {self.value}>"

# Define function <name> of type <datatype> with parameters <parameters> and body <body>
class FunctionDefinition:
    def __init__(self, datatype, name, parameters, body):
        self.datatype = datatype
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"<FunctionDefinition: {self.datatype}, {self.name}, {self.parameters}, {self.body}>"

# Define structure <name> with fields <fields>
class StructureDefinition:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

    def __repr__(self):
        return f"<StrcutureDefinition: {self.name}, {self.fields}>"

# Use inline C code: <code>
class InlineC:
    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return f"<InlineC: {self.code}>"