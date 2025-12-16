# The Shard PreProcessor (SPP)
---

## Summary
---
- [The role of a preprocessor](#the-role-of-a-preprocessor)
- [Instructions](#instructions)
- [Constants](#constants)
- [Macros](#macros)
- [Includes](#includes)

## The role of a preprocessor
---
A **textual preprocessor** transforms the content of a program before it is analyzed by the compiler. This type of preprocessor does not have any knowledge about what is a function, a variable, Shard syntax, ... It just operates on the content of the file.

Textual preprocessors are still used in languages like C and C++ but more languages decide to use **imports**, which manage namespaces and such things automatically.

However, Shard uses a preprocessor: **SPP**.

## Instructions
---
A SPP instruction always starts with `@`. For example:
```sd
@instruction parameters
```

## Constants
---
A **preprocessor constant** is a symbol which corresponds to a constant text pattern. The preprocessor will replace every occurance of a constant by the text it corresponds to.

Constants are defined using the `@const` instruction.
```sd
@const PI 3.14
```
All occurences of `PI` in the program after this definition will be replaced by `3.14`.

You can remove a constant using the `@undef` instruction.
```sd
@undef PI
```

## Macros
---
A **preprocessor macro** is a symbol which corresponds to a text pattern. The SPP macros are **very powerful** because they work with **regex patterns**. They are defined using the `@macro` keyword. The macro parameters start with a `$`.
```sd
@macro ADD "add $x with $y" "$x + $y"
```
Now, all occurences of `add ... with ...` (for example: `add 3 with 4`) will be replaced by `... + ...` (`3 + 4`).

## Includes
---
The Shard PreProcessor provides the `@include` instruction, which is used to copy the content of a Shard file inside another Shard file. You do not need to specify the extension of the file you want to include, because SPP automatically adds ".sd" at the end of the filename.

To include a library, you need to type `lib:` before the name of your file. SPP will search for `/usr/local/lib/shard/your_lib/your_lib/your-file.sd`.

You **must** create at least one file named `__root__.sd` in your project directory for SPP to know from where to include files.

This instruction automatically generates the `##` token, which resets the line counter.

## Messages
---
You can display messages during preprocessing with the `@message` instruction. Type the text you want to display next to it.