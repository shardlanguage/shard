# Arrays
---

## Summary
---
- [What is an array?](#what-is-an-array)
- [Declaring arrays](#declaring-arrays)
- [Accessing values](#accessing-values)

## What is an array?
---
A **static array** is a **statically allocated memory buffer** containing values that can be accessed using **indexes**. Indexes are translated into **offsets** in the buffer using the following formula: `offset = index * element_size`.

## Declaring arrays
---
In Shard, you can declare **static arrays** using the following syntax:
```sd
var array: [10]i32;         // empty array
var array2: [10]i32 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9;
```
As you can see, we are using an [array type](types.md#array-types) to create an array of type `i32` (each element in the array must have this type) and of length 10.

Separate values with a comma (`,`) to initialize an array.

## Accessing values
---
To get a value at a specific position in an array, you need to access it using its **index** (position) in the array. For example:
```sd
const val1: i32 = array[5];
```
***Note**: the first index is 0, not 1.*