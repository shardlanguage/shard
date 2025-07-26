# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains the C code generation functions.
# =====================================================================

# Import modules
from utils.symbols import *

# Generate a value
def generate_value(value):
    return f"{value}"

# Generate an access to a variable
def generate_id(name):
    return f"{name}"

# Generate an access to an array index
def generate_array_access(name, index):
    return f"{name}[{index}]"

# Generate a call to a function
def generate_function_call(name, parameters):
    return f"{name}({', '.join(parameters)})"

# Generate an unary operation
def generate_unary_op(operator, right):
    return f"{operator}{right}"

# Generate a binary operation
def generate_binary_op(left, operator, right):
    return f"{left} {operator} {right}"

# Generate an assignment to a variable
def generate_assignment(name, operator, value):
    return f"{name} {operator} {value}"

# Generate an assignment to an array index
def generate_array_assignment(name, index, operator, value):
    return f"{name}[{index}] {operator} {value}"

# Generate a groupped expression
def generate_group(group):
    return f"({group})"

# Generate a variable declaration
def generate_variable_declaration(symbol_table, type_modifier, primary_type, name, value):
    prefix = "const " if type_modifier == "const" else ""
    
    if primary_type == 'byte':
        c_type = "int8_t"
    elif primary_type == 'word':
        c_type = "int16_t"
    elif primary_type == 'dword':
        c_type = "int32_t"
    elif primary_type == 'qword':
        c_type = "int64_t"
    elif primary_type == 'float':
        c_type = "float"
    elif primary_type == 'double':
        c_type = "double"
    elif primary_type == 'ubyte':
        c_type = "uint8_t"
    elif primary_type == 'uword':
        c_type = "uint16_t"
    elif primary_type == 'udword':
        c_type = "uint32_t"
    elif primary_type == 'uqword':
        c_type = "uint64_t"
    else:
        raise ValueError(f"Unknown primary type: {primary_type}")

    return f"{prefix}{c_type} {name} = {value}"

# Generate an array declaration
def generate_array_declaration(symbol_table, type_modifier, primary_type, name, size, content):
    prefix = "const " if type_modifier == "const" else ""
    content_str = '{' + ', '.join(content) + '}'
    
    if primary_type == 'byte':
        c_type = "int8_t"
    elif primary_type == 'word':
        c_type = "int16_t"
    elif primary_type == 'dword':
        c_type = "int32_t"
    elif primary_type == 'qword':
        c_type = "int64_t"
    elif primary_type == 'float':
        c_type = "float"
    elif primary_type == 'double':
        c_type = "double"
    elif primary_type == 'ubyte':
        c_type = "uint8_t"
    elif primary_type == 'uword':
        c_type = "uint16_t"
    elif primary_type == 'udword':
        c_type = "uint32_t"
    elif primary_type == 'uqword':
        c_type = "uint64_t"
    else:
        raise ValueError(f"Unknown primary type: {primary_type}")
    
    return f"{prefix}{c_type} {name}[{size}] = {content_str}"

# Generate a code block
def generate_codeblock(statement_list):
    statements = [f"    {stmt};\n" for stmt in statement_list]
    return '{\n' + ''.join(statements) + '}'

# Generate a condition structure
def generate_condition(condition, if_branch, else_branch):
    stmt_if = [f"   {stmt};\n" for stmt in if_branch]
    stmt_else = [f"    {stmt};\n" for stmt in else_branch]

    return (
        f"if ({condition}) " +
        '{\n' + ''.join(stmt_if) + '}\n' +
        "else {\n" + ''.join(stmt_else) + '}'
    )

# Generate an unconditionnal loop structure
def generate_loop_unconditionnal(statement_list):
    stmt_list = [f"   {stmt};\n" for stmt in statement_list]
    return "while (1) {\n" + ''.join(stmt_list) + '}'

# Generate a conditionnal loop structure
def generate_loop_conditionnal(looptype, condition, statement_list):
    stmt_list = [f"   {stmt};\n" for stmt in statement_list]

    if looptype == 'while':
        return f"while ({condition}) " + "{\n" + ''.join(stmt_list) + "}"
    elif looptype == 'until':
        return f"while (!({condition})) " + "{\n" + ''.join(stmt_list) + "}"
    else:
        raise ValueError(f"Unknown loop type: {looptype}")

# Generate flow control statements
def generate_flow_control(statement, value):
    if statement == 'break':
        return "break"
    elif statement == 'continue':
        return "continue"
    elif statement == 'return':
        if value is not None:
            return f"return {value}"
        else:
            return "return"
    else:
        raise ValueError(f"Unknow flow control statement: {statement}")

# Generate a function definition
def generate_function_definition(datatype, name, parameters, body):
    body_content = [f"    {stmt};\n" for stmt in body]

    type_map = {
        'byte': 'int8_t', 'ubyte': 'uint8_t',
        'word': 'int16_t', 'uword': 'uint16_t',
        'dword': 'int32_t', 'udword': 'uint32_t',
        'qword': 'int64_t', 'uqword': 'uint64_t',
        'float': 'float', 'double': 'double',
        'void': 'void'
    }

    modifier, primary_type = datatype

    type_str = ''
    if modifier == 'const':
        type_str += 'const '

    if primary_type not in type_map:
        raise ValueError(f"Invalid type: {primary_type}")

    type_str += type_map[primary_type]
    params_str = ', '.join(parameters) if parameters else ''

    return f"{type_str} {name}({params_str}) " + '{\n' + ''.join(body_content) + '}\n'

# Generate any unary operation
def generate_UnOp(operator, right):
    op_map = {
        '+': '+',
        '-': '-',
        'not': '!',
        '~': '~'
    }
    if operator not in op_map:
        raise ValueError(f"Unknown unary operator: {operator}")
    return generate_unary_op(op_map[operator], right)

# Generate any binary operation
def generate_BinOp(left, operator, right):
    op_map = {
        '+': '+', '-': '-', '*': '*', '/': '/', '<<=': '<<=', '>>=': '>>=',
        'and': '&&', 'or': '||',
        '&': '&', '|': '|', '^': '^',
        '==': '==', '!=': '!=',
        '<': '<', '>': '>', '<=': '<=', '>=': '>='
    }
    if operator not in op_map:
        raise ValueError(f"Unknown binary operator: {operator}")
    return generate_binary_op(left, op_map[operator], right)

# Generate any assignment operation
def generate_AssignOp(symbol_table, name, operator, value):
    op_map = {
        '=': '=', '+=': '+=', '-=': '-=', '*=': '*=', '/=': '/=',
        '&=': '&=', '|=': '|=', '^=': '^=', '~=': '~=',
        '<<=': '<<=', '>>=': '>>='
    }

    var = symbol_table.get_variable(name)

    if operator not in op_map:
        raise ValueError(f"Unknow assignment operator: {operator}")
    return generate_assignment(name, op_map[operator], value)

# Generate any array index assignment operation
def generate_ArrayAssignOp(symbol_table, name, index, operator, value):
    op_map = {
        '=': '=', '+=': '+=', '-=': '-=', '*=': '*=', '/=': '/=',
        '&=': '&=', '|=': '|=', '^=': '^=', '~=': '~=',
        '<<=': '<<=', '>>=': '>>='
    }

    var = symbol_table.get_variable(name)

    if operator not in op_map:
        raise ValueError(f"Unknow assignment operator: {operator}")
    return generate_array_assignment(name, index, op_map[operator], value)

# Generate any conditionnal loop structure
def generate_LoopCondition(looptype, condition, branch):
    return generate_loop_conditionnal(looptype, condition, branch)