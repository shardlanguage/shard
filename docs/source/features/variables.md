# Variables
---

## Summary
---
- [What is a variable?](#what-is-a-variable)
- [Declaration and definition](#declaration-and-definition)
- [Inside expressions](#inside-expressions)
- [Assignment operators](#assignment-operators)
- [Constants](#constants)
- [Extern variables](#extern-variables)

## What is a variable?
---
In programming, a variable could be defined like this: **a memory space associated with an identifier, allocated statically or dynamically, whose lifetime depends on the programming language used.**

## Declaration and definition
---
In Shard, variables (and other type of symbols) must be **declared** before being used. If a symbol is used but not declared, it does not exist from the point of view of the compiler. In Shard, the syntax used to declare a variable is the following:
```sd
// Declare
prefix name: type;

// Declare and define
prefix name: type = value;
```
***Note**: a variable declared without a value contains empty memory, not zeros. Using it could lead to an undefined behaviour (UB). Make sure to define all your variables.*

For example:
```sd
var x: i32 = 42;
```
This line declares a variable named `x` of type `i32` with a value of 42.

## Inside expressions
---
Identifiers can be used inside **expressions**. For example, you can try the following code, which adds two variables together (`x` and `y`) and store the result in `z`.
```sd
var x: i32 = 5;
var y: i32 = 4;
var z: i32 = x + y;
```
Now, `z` should have a value of 9 (5 + 4).

## Assignment operators
---
The value of a variable can be **modified** using **assignment operators**. The most common is `=`, which replaces the value of a variable by another, but there are other operators, which are mostly shortcuts:
```sd
x += 5;
// instead of
x = x + 5;
```
Here are all the assignment operators that can be used in Shard:
| Operator      | Effect |
| --------      | ------ |
| `=`           | Sets x to y |
| `+=`          | Sets x to x + y |
| `-=`          | Sets x to x - y |
| `*=`          | Sets x to x * y |
| `/=`          | Sets x to x / y |
| `%=`          | Sets x to x % y |
| `&=`          | Sets x to x & y |
| `\|=`         | Sets x to x \| y |
| `^=`          | Sets x to x ^ y |
| `~=`          | Sets x to ~y |
| `<<=`         | Sets x to x << y |
| `>>=`         | Sets x to x >> y |

## Constants
---
If you do not want your variable to be modified, you can declare it as a constant, by using prefix `const` instead of `var`. Constants are **read-only**, so their value cannot be modified. This also means that **assignment operators** cannot be used on them.
```sd
const c: i32 = 5;
c *= 2;             // wrong
```

## Extern variables
The `extern` keyword preceding a declaration or a function definitioncan be used to declare an extern symbol. You can use it like this:
```sd
// for a variable
extern var name: i32;
// for a function
extern func name(params) -> i32 {};
```
***Note**: DO NOT write in the body of extern functions or you will get an error from the C compiler.*