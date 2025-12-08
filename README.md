# The Shard programming language

## What is Shard?
**Shard** is a **programming language** that combines **low-level** control, suitable for **operating systems**, with the flexibility to develop **high-level** applications.

## Features
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

**Makefile and make.bat are used to build the docs locally!**

## Learn Shard
If you want to learn Shard, you can read the [full documentation here](https://shardlanguage.github.io/shard).

## Contributing
The contributing guide can be found [here](CONTRIBUTING.md).