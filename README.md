# The Shard programming language

## What is Shard?
*Shard* is a compiled programming language in active development.

## Features
- Structures
- Functions and procedures (main function required)
- Static arrays (a[size] = [e1, e2, e3, e4])
- Unsigned types (ubte, uword, udword, uqword)
- Comments (#)
- Constants
- Flow control statements
- Loops (forever, while, until)
- Better errors
- Booleans, bit-boolean, assignment, bit-shifting and comparison operators
- If/else conditions
- Complete CLI
- Static and strongly typed variables (byte, word, dword, qword, float, double)
- Division by zero handling
- Floating numbers support
- Arithmetic expressions
- Operators precedences
- Statement lists

## Install
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
```

## Program example
You can try to compile and run the program below:
```shd
# My first Shard program
# NOTE: as you can see, the last statement of a program or a code block does
# not require a ;

# Define a function to add 2 numbers and return the result
# NOTE: dword handles 32-bit signed values
func dword add(dword a, dword b)
{
    return a + b
};

# Main function
func dword main()
{
    # Define a structure to represent a point with a xy position
    struct Point
    {
        dword x,
        dword y
    };

    # Declare an instance of this point
    struct Point p;

    # Add the x position and the y position of the point and store
    # the result in the pos variable
    dword pos = add(p.x, p.y);

    return 0
}
```