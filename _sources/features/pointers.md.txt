# Pointers and references
---

## Summary
---
- [What is a pointer?](#what-is-a-pointer)
- [Declaring pointers](#declaring-pointers)

## What is a pointer?
---
A pointer is **a variable that stores a memory address**. You can get the memory address of a variable using the `&` unary operator.

## Declaring pointers
---
To declare a pointer, you need to use a [**pointer type**](types.md#pointer-types).
```sd
var x: i32 = 42;
var p: *i32 = &x;       // p is a pointer to x
var pp: **i32 = &p;     // pp is a pointer to p
```