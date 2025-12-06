# Expressions
---

## Summary
---
- [Values](#values)
- [Unary operators](#unary-operators)
- [Binary operators](#binary-operators)
- [Assignment operators](#assignment-operators)

## Values
---
In an expression, you can use the following values:
- Decimal number (`1234`)
- Float number (`12.34`)
- Binary number (`0b10`)
- Octal number (`0o1234`)
- Hexadecimal number (`0x1234ABCD`)
- Characters (`'c'`)
- String (limited) (`"str"`)
- Identifier (`x`)
- Function call (`x()`)
- Reference (`&x`)
- Array value (`x[y]`)
- Expressions (`a+b`, `a/b*(c-d)`, ...)

## Unary operators
---
**Unary operators** can be applied on only **one expression**.
| Operator  | Operation type    |
| --------  | --------------    |
| `+`       | Positive          |
| `-`       | Negative          |
| `~`       | Bitwise not       |
| `not`     | Logical not       |
| `&`       | Reference         |
| `sizeof()`| Size in bytes     |

## Binary operators
---
**Binary operators** can be applied on **two expressions**.
| Operator  | Operation type    |
| --------  | --------------    |
| `+`       | Addition          |
| `-`       | Subtraction       |
| `*`       | Multiplication    |
| `/`       | Division          |
| `%`       | Modulo            |
| `<<`      | Bit shift to the left |
| `>>`      | Bit shift to the right |
| `&`       | Bitwise and       |
| `\|`      | Bitwise or        |
| `^`       | Bitwise xor       |
| `and`     | Logical and       |
| `or`      | Logical or        |
| `==`      | Is equal          |
| `!=`      | Is not equal      |
| `<`       | Is lesser than    |
| `>`       | Is greater than   |
| `<=`      | Is lesser than or equal |
| `>=`      | Is greater than or equal |

## Assignment operators
The list of all the assignment operators can be found [here](variables.md#assignment-operators).