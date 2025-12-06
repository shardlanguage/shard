# Functions
---

## Summary
---
- [Functions and procedures](#functions-and-procedures)
- [How to define a function](#how-to-define-a-function)
- [Returning a value](#returning-a-value)
- [Local symbols](#local-symbols)
- [Calling a function](#calling-a-function)
- [Nested functions](#nested-functions)
- [The main function](#the-main-function)

## Functions and procedures
---
In programming, a **procedure** (or a function) is like a program inside another program. The difference between both is that a function **returns a value**, unlike the procedure which does not.

In several programming languages (such as C and C++), procedures are functions of type `void`. In Shard, this type does not exist as `void` but as `C_void`. It is very rare for the programmer to have to use it since the compiler generates it automatically.

## How to define a function
---
Shard functions are designed using the following example:
```sd
// function
func f(p) -> T {}
// procedure
func f(p) {}
```
In this example, `f` is the **name** of the function, `p` is the required **parameters**, and, when it is not a procedure, `T` is the **type of the value(s) the function will return**. The function **body** is between `{` and `}`.

Let's define the function `foo`:
```sd
func proc(var x: i32) -> i32 {
    return x;
}
```

## Local symbols
---
When you declare a variable, a structure or any other symbol inside a function, it will not be accessible in **the global scope** (outside of the function). That is because when you enter a function body, the compiler creates a new scope, called **local scope**, which is **destroyed** at the end of the function body.

However, symbols which are defined **outside of the functions** (in the global scope) are accessible inside all the functions.

Let's take an example:
```sd
var x: i32 = 5;
func f() -> i32 {
    return x + 2;       // valid, because x is defined BEFORE and OUTSIDE the function
}

func g() {
    var y: i32 = 10;
}
y *= 2;                 // not valid, because y is a LOCAL variable
```

## Returning a value
---
A function returns a value using the `return` keyword. It can take a value or nothing. If it takes nothing, then the function is a procedure.

```sd
// procedure
func proc() {
    return;
}

// function
func f() -> u8 {
    return 12;
}
```

## Calling a function
---
You can call a function `f` like this: `f(p)`, where `p` is the **values** assigned to the function parameters. For example, let's write a simple function that adds two numbers and returns the result:
```sd
func add(var a: f32, var b: f32) -> f32 {
    return a + b;
}

var result: f32 = add(3, 4);
```

## Nested functions
---
Nested functions are **not supported** in Shard. A nested function is a function defined inside another.

## The main function
---
Every program must have a main function. This function is called `main`, and can only take two parameters: `var argc: C_int`, which stores the count of arguments in the command-line, and `var argv: **C_char`, which stores the arguments in the command-line.

***Note:** to avoid the obligation of defining `main()`, you can use the --no-main flag when compiling your code, but you need to provide an entry point to your linker.*