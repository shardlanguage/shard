# Shard documentation
---

## Summary
---
- [What is Shard?](#what-is-shard)
- [Features](#features)
- [Installation](#installation)
- [Learn Shard](#learn-shard)
- [Contributing](#contributing)

## What is Shard?
---
**Shard** is a **programming language** that combines **low-level** control, suitable for **operating systems**, with the flexibility to develop **high-level** applications

## Features
---
- **C++/Rust-like syntax**, designed to be clean and modern
- **Strong typing**: supports built-in and user-defined types
- **Pointers** like in C
- **Structures and arrays** easy to declare, initialize and access
- **Powerful preprocessor** with pattern-based macros
- **Cross-platform backend**: compiles to C code and supports freestanding, configurable target compiler
- **Extensible compiler**: adding backends is easy
- **Namespaces** organize your code into logical units

## Installation
**Step 1**: clone the repository
```bash
git clone https://github.com/shardlanguage/shard
```
**Step 2**: make sure that you have Python3 installed on your system
```bash
python3 --version
```
**Step 3**: run the installation script as root
```bash
cd shard
chmod +x install.sh
su
./install.sh
```
**Step 4**: test the installation
```bash
shardc --version
```

## Learn Shard
---
If you want to learn Shard, then you are in the right place! This documentation provides **examples** and **explanations** about **every feature** of the language.

- [Variables](features/variables.md)
- [Types](features/types.md)
- [Expressions](features/expressions.md)
- [Arrays](features/array.md)
- [Pointers and memory addresses](features/pointers.md)
- [Functions](features/functions.md)
- [Comments](features/comments.md)
- [Structures](features/structures.md)
- [Conditions and loops](features/condloops.md)
- [Namespaces](features/namespaces.md)
- [Preprocessor](features/preprocessor.md)
- [Inline C](features/inline.md)
- [Compiler flags](features/flags.md)

## Contributing
---
The contributing guide can be found [here](contributing.md).