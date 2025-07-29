# The Shard programming language

## What is Shard?
*Shard* is a compiled programming language in active development.

## Features
- sizeof and & (for address) operators
- Inline C
- Preprocessor (@include)
- Strings
- Structures
- Functions and procedures (main function required)
- Static arrays (a[size] = [e1, e2, e3, e4])
- Unsigned types (ubyte, uword, udword, uqword)
- Comments (#)
- Constants
- Flow control statements
- Loops (forever, while, until, for)
- Better errors
- Booleans, bit-boolean, assignment, bit-shifting and comparison operators
- If/else conditions
- Complete CLI
- Static and strongly-typed variables (byte, word, dword, qword, float, double, unsafe_str...)
- Division by zero handling
- Floating numbers support
- Arithmetic expressions (modulo included)
- Operators precedences
- Statement lists

## Install
---
### Linux
The shardc binary is provided in the releases but you can install from sources:
```bash
git clone https://github.com/shardlanguage/shard
cd shard
chmod +x install.sh
su
./install.sh
```

The binary named `shardc` should have been moved in `/usr/bin/`.
Try it out using:

```bash
shardc -h
```

### Windows
*WARNING: the Windows installation script has not been tried yet because I don't have a machine with Windows installed. If you have, you can run the script on your machine and open an issue to tell us if it works or not. Thanks!*

```powershell
git clone https://github.com/shardlanguage/shard.git
cd shard
# As administrator
.\install.ps1
```

## Contributing
If you want to contribute, please read [the contributing guide](CONTRIBUTING.md).

## Using the shardc CLI
***IMPORTANT: Shard requires GCC to compile***

```bash
shardc -h                               # Display a help message
shardc -c example.shd                   # Compile a Shard file into a C file
shardc -o example.shd                   # Compile a C file into an object file
shardc -x example.shd                   # Compile an object file into an executable file
shard -cox example.shd                  # All-in one -c -o and -x options
shard -cox --keep-all example.shd       # Don't remove the generated files (.c and .o)
shard option --dbg-err example.shd      # Show errors traceback directly to the compiler code.
                                        # Only used for shardc features development
```

## Program example
You can try to compile and run the program below:
```shd
# My first Shard program
# NOTE: as you can see, the last statement of a program or a code block does
# not require a ;
# But if you are making a module that will be included in another file using
# @include, ; is required at the end of your module

# Define a function to add 2 numbers and return the result
# NOTE: dword handles 32-bit signed values
func dword add_pos(dword a, dword b)
{
    return a + b
};

# Main function
func dword main()
{
    # Define a structure to represent a point with a xy position
    struct Point
    {
        unsafe_str name,
        dword x,
        dword y
    };

    # Declare an instance of this point
    struct Point p;
    # Give the point a name
    p.name = "A";

    # Add the x position and the y position of the point and store
    # the result in the pos variable
    dword pos = add(p.x, p.y);

    return 0
}
```