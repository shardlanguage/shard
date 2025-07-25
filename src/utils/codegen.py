from utils.symbols import *

def generate_value(value):
    return f"({value})"

def generate_id(name):
    return f"({name})"

def generate_unary_op(operator, right):
    return f"({operator}({right}))"

def generate_binary_op(left, operator, right):
    return f"(({left}) {operator} ({right}))"

def generate_assignment(name, operator, value):
    return f"({name} {operator} ({value}))"

def generate_group(group):
    return f"({group})"

def generate_variable_declaration(symbol_table, type_modifier, primary_type, name, value):
    prefix = "const " if type_modifier == "const" else ""
    if primary_type == 'byte':
        return f"{prefix}int8_t {name} = {value}"
    elif primary_type == 'word':
        return f"{prefix}int16_t {name} = {value}"
    elif primary_type == 'dword':
        return f"{prefix}int32_t {name} = {value}"
    elif primary_type == 'qword':
        return f"{prefix}int64_t {name} = {value}"
    else:
        raise ValueError(f"Unknown primary type: {primary_type}")

def generate_codeblock(statement_list):
    statements = [f"    {stmt};\n" for stmt in statement_list]
    return '{\n' + ''.join(statements) + '}'

def generate_condition(condition, if_branch, else_branch):
    stmt_if = [f"   {stmt};\n" for stmt in if_branch]
    stmt_else = [f"    {stmt};\n" for stmt in else_branch]

    return (
        f"if ({condition}) " +
        '{\n' + ''.join(stmt_if) + '}\n' +
        "else {\n" + ''.join(stmt_else) + '}'
    )

def generate_loop_unconditionnal(statement_list):
    stmt_list = [f"   {stmt};\n" for stmt in statement_list]
    return "while (1) {\n" + ''.join(stmt_list) + '}'

def generate_loop_conditionnal(looptype, condition, statement_list):
    stmt_list = [f"   {stmt};\n" for stmt in statement_list]

    if looptype == 'while':
        return f"while ({condition}) " + "{\n" + ''.join(stmt_list) + "}"
    elif looptype == 'until':
        return f"while (!({condition})) " + "{\n" + ''.join(stmt_list) + "}"
    else:
        raise ValueError(f"Unknown loop type: {looptype}")

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

def generate_AssignOp(symbol_table, name, operator, value):
    op_map = {
        '=': '=', '+=': '+=', '-=': '-=', '*=': '*=', '/=': '/=',
        '&=': '&=', '|=': '|=', '^=': '^=', '~=': '~=',
        '<<=': '<<=', '>>=': '>>='
    }

    var = symbol_table.get_variable(name)

    if operator not in op_map:
        raise ValueError(f"Unknow assignment operation: {operator}")
    return generate_assignment(name, op_map[operator], value)

def generate_LoopCondition(looptype, condition, branch):
    return generate_loop_conditionnal(looptype, condition, branch)