# Types
---

## Summary
---
- [Static typing or dynamic typing](#static-typing-or-dynamic-typing)
- [Strong typing or weak typing](#strong-typing-or-weak-typing)
- [Different data types](#different-data-types)
- [Casting types](#casting-types)
- [Array types](#array-types)
- [Pointer types](#pointer-types)
- [Type aliases](#type-aliases)
- [Creating new types](#creating-new-types)

## Static typing or dynamic typing
---
Shard is a **statically typed** programming language. This means that types are resolved at **compile-time**, unlike **dynamically typed** languages, which resolve their types at **run-time**. Here is an example of how both systems work:
```sd
// static typing
var x: i32 = 5;
x = 89;
// dynamic typing
var y: i32 = 5;
y = 8.9;
```
In the example below, only the first two lines will produce executable code, because `x` is of type `i32`, so it expects a **32-bit integer** value. On the second line, we set it to 5, which is an integer lesser than 2<sup>32</sup>, so the example is valid.
On the other hand, we have the two last lines, which suppose that dynamic typing is implemented in Shard (it is not). So we have another variable of type `i32` (`y`), but we assign it a **floating value** on the fourth line. In a language like Python, this will work, but not in languages such as Shard, C or Rust, because you cannot change the type of a variable.

## Strong typing or weak typing
---
Shard is a **strongly typed** programming language. This means that operations can only be applied on values **of the same type**. For example, if I add a `f64` with an `u64`, the C compiler will raise a warning (because Shard doesn't have type checking yet).

## Different data types
---
Here are all the data types that can be used in Shard. The types prefixed by "C_" are used for compatibility with the C programming language.
| Type name | Accepted values |
| --------- | --------------- |
| `i8`      | Signed 8-bit integer |
| `i16`     | Signed 16-bit integer |
| `i32`     | Signed 32-bit integer |
| `i64`     | Signed 64-bit integer |
| `u8`      | Unsigned 8-bit integer |
| `u16`     | Unsigned 16-bit integer |
| `u32`     | Unsigned 32-bit integer |
| `u64`     | Unsigned 64-bit integer |
| `bool`    | Boolean value (0 or 1) |
| `f32`     | 32-bit float |
| `f64`     | 64-bit float |
| `voidptr` | Void pointer (for generic typing) |
| `C_char`  | C type `char` |
| `C_short`  | C type `short` |
| `C_int`  | C type `int` |
| `C_long`  | C type `long` |
| `C_uchar`  | C type `unsigned char` |
| `C_ushort`  | C type `unsigned short` |
| `C_uint`  | C type `unsigned int` |
| `C_ulong`  | C type `unsigned long` |
| `C_void`  | C type `void` |
| `C_size`  | C type `size_t` |
| `C_usize`  | C type `unsigned size_t` |

## Casting types
---
To avoid strong typing restrictions, Shard allow the developer to **cast types**, using the `as` operator, which tells the compiler to interpret a type as another type. Let's make an example:
```sd
var x: u8 = 15;
var y: u16 = x as u16;
```
The type of `x` **will not** be turned into `u16`, but **interpreted** as `u16` only in the operation where `as` is used. This is like a temporary type conversion.

## Array types
---
When declaring arrays, you need to use **array types**. They tell the compiler about the **type** of the array and its **size** (in elements). Here is how to use one:
```sd
[size]type
// for example
[10]i32
```
This tells the compiler that our array is of type **`i32`** and length **10**.

## Pointer types
---
When declaring pointers, you need to use **pointer types**. They are prefixed by a theorically unlimited count of `*`. Here is how to use one:
```sd
var p: *i32;            // a pointer of type i32
var pp: **i32;          // a pointer of pointer of type i32
var ppp: ***i32;        // a pointer of pointer of pointer of type i32
var pppppppp: **************************i32;        // help
```

## Type aliases
---
A **type alias** is what we can call a *fake type*. When you type the name of an alias, the compiler will replace it by the name of the aliased type. Type aliases are defined using the `type` keyword.
```sd
type int = C_int;
// now, "int" will be interpreted as "C_int"
var x: int = 42;
var x: C_int = 42;          // same
```
You can also define aliases of aliases:
```sd
type int = C_int;
type in = int;
type i = in;
type _ = i;
// ...
```

## Creating new types
---
Shard allows the developer to create **new types**. They are not aliases, but real types, which correspond to a real **C type**. They are defined using the `newtype` keyword. For example, let's imagine that you are writing a Shard binding for `stdio.h`:
```sd
newtype stdio_file = "FILE";
```
The compiler will now compile every use of `stdio_file` into `FILE`.