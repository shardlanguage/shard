# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains the C code generation functions.
# =====================================================================

# Import modules
from utils.symbols import *
from utils.conversion import *

# Generate a value
def generate_value(value):
    return f"{value}"

def generate_string(string):
    return f"\"{string}\""

# Generate an access to a variable
def generate_id(name):
    return f"{name}"

# Generate an access to an array index
def generate_array_access(name, index):
    return f"{name}[{index}]"

# Generate an access to a structure instance field
def generate_struct_instance_field_access(instance, field):
    return f"{instance}.{field}"

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

# Generate an assignment to a structure instance field
def generate_struct_instance_field_assignment(instance, field, operator, value):
    return f"{instance}.{field} {operator} {value}"

# Generate a groupped expression
def generate_group(group):
    return f"({group})"

# Generate a variable declaration
def generate_variable_declaration(type_modifier, primary_type, name, value):
    prefix = "const " if type_modifier == "const" else ""

    c_type = shard_type_to_c(primary_type)

    if c_type.startswith("struct"):
        return f"{prefix}{c_type} {name} = " + '{' + '0' + '}'
    return f"{prefix}{c_type} {name} = {value}"

# Generate an array declaration
def generate_array_declaration(type_modifier, primary_type, name, size, content):
    prefix = "const " if type_modifier == "const" else ""
    content_str = '{' + ', '.join(content) + '}'
    
    c_type = shard_type_to_c(primary_type)
    if c_type.startswith("struct"):
        raise TypeError("A structure instance cannot be declarated as an array")
    
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
    global type_map

    body_content = [f"    {stmt};\n" for stmt in body]

    modifier, primary_type = datatype

    type_str = ''
    if modifier == 'const':
        type_str += 'const '

    if primary_type not in type_map:
        raise ValueError(f"Invalid type: {primary_type}")

    type_str += type_map[primary_type]
    if type_str.startswith("struct"):
        raise TypeError("A function cannot be a structure instance")

    params_str = ', '.join(parameters) if parameters else ''

    return f"{type_str} {name}({params_str}) " + '{\n' + ''.join(body_content) + '}\n'

# Generate a structure definition
def generate_struct_definition(name, fields):
    lines = []
    for datatype, var_name, *rest in fields:
        size = rest[0] if rest else None

        if size is not None:
            lines.append(f"{datatype} {var_name}[{size}];")
        else:
            lines.append(f"{datatype} {var_name};")

    fields_str = '\n\t'.join(lines) if lines else ''

    return f"struct {name} {{\n\t{fields_str}\n}}"

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
        '&=': '&=', '|=': '|=', '^=': '^=', '~=': '= ~',
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
        '&=': '&=', '|=': '|=', '^=': '^=', '~=': '= ~',
        '<<=': '<<=', '>>=': '>>='
    }

    var = symbol_table.get_variable(name)

    if operator not in op_map:
        raise ValueError(f"Unknow assignment operator: {operator}")
    return generate_array_assignment(name, index, op_map[operator], value)

# Generate any structure instance field assignment operation
def generate_StructInstanceFieldAssignOp(symbol_table, instance, field, operator, value):
    op_map = {
        '=': '=', '+=': '+=', '-=': '-=', '*=': '*=', '/=': '/=',
        '&=': '&=', '|=': '|=', '^=': '^=', '~=': '= ~',
        '<<=': '<<=', '>>=': '>>='
    }

    var = symbol_table.get_variable(instance)

    if operator not in op_map:
        raise ValueError(f"Unknow assignment operator: {operator}")
    return generate_struct_instance_field_assignment(instance, field, operator, value)

# Generate any conditionnal loop structure
def generate_LoopCondition(looptype, condition, branch):
    return generate_loop_conditionnal(looptype, condition, branch)