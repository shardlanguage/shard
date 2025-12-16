# Conditions and loops
---

## Summary
---
- [Conditional structures](#conditional-structures)
    - [The IF condition](#the-if-condition)
    - [The ELSE condition](#the-else-condition)
    - [The ELIF condition](#the-elif-condition)
- [Loops](#loops)
    - [The FOREVER loop](#the-forever-loop)
    - [The WHILE loop](#the-while-loop)
    - [The UNTIL loop](#the-until-loop)
    - [The FOR loop](#the-for-loop)
    - [How to exit a loop](#how-to-exit-a-loop)
    - [How to return to the beginning of a loop](#how-to-return-at-the-beginning-of-a-loop)

## Conditional structures
---

### The IF condition
---
The first condition is **"if"**. It evaluates a **boolean expression** and executes the code if this condition is **true**. The code is skipped if the condition is false.
```sd
if 3+3 == 6 {
    // your code goes here
}
```

### The ELSE condition
---
The second condition is **"else"**. It can only be used after `if` or `elif` and marks the end of a conditional structure. It executes the code only if the expression evaluated by the previous condition was **false**.
```sd
if 3+3 == 7 {
    // your code goes here
} else {
    // your code goes here
}
```

### The ELIF condition
---
The third condition is **"elif"**, which is a contraction of **"else if"**. It is a combination of both conditions. It can only be used after `if` or another `elif`, but a conditional structure cannot start with `elif`.
```sd
var x: i32 = 3 + 3;
if x == 5 {
    // ...
} elif x == 6 {
    // ...
} else {
    // ...
}
```
is the equivalent of
```sd
var x: i32 = 3 + 3;
if x == 5 {
    // ...
} else {
    if x == 6 {
        // ...
    }
    else {
        // ...
    }
}
```

## Loops
---

### The FOREVER loop
---
The first loop is `forever`. It keeps executing the same code block forever and never stops unless if you force it to.
```sd
forever {
    // ...
}
```

### The WHILE loop
---
The second loop is `while`. It keeps executing the same code block while a condition is true and stops when it becomes false.
```sd
var x: i32 = 0;
var y: i32 = 5;

while x <= y {
    x += 1;
}
```

### The UNTIL loop
---
The third loop is `until`. It is the opposite of `while`, because it keeps executing the same code block while a condition is false and stops when it becomes true.
```sd
var x: i32 = 0;
var y: i32 = 0;

until x == y {
    x += 1;
}
```
***Note**: in Shard, we prefer using this loop but we also provide `while` if you want.*

### The FOR loop
---
The last loop is `for`. It first declares a variable, which is **local** (it cannot be used outside of the loop) then checks a condition and does something at the end.
```sd
for var i: i32 = 0; i <= 5; i += 1 {
    // ...
}
```
is equivalent to
```sd
{
    var i: i32 = 0;
    while i <= 5 {
        i += 1;
    }
}
```

### How to exit a loop
---
To exit a loop, just use the `break` keyword.

### How to return at the beginning of a loop
---
To return at the beginning of a loop and skip what comes next in the loop, use the `continue` keyword.