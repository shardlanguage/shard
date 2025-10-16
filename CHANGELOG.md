## Version 0.0.4
- Added comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Added single-line and multi-line comments: `//`, `/**/`

## Version 0.0.3
- Added unsigned data types: `u8`, `u16`, `u32`, `u64`
- Signed / unsigned operations are now handled
- Fixed assembly generation for NodeVariableDecl
- Added combined assignment operators: `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `&=`, `|=`, `^=`, `~=`

## Version 0.0.2
- Added variable declarations: `var x: T = y;`
- Added variable assignments using `=`
- Added a symbol table, a type table and a symbol resolver
- Cleaned up the code
- Added signed data types: `i8`, `i16`, `i32`, `i64`

## Version 0.0.1
- Added arithmetic operator: `%`
- Added bitwise operators: `&`, `|`, `^`, `~`
- Added logical operators: `<<`, `>>`
- `shardc/backend/visitor.py` now uses dictionnaries instead of conditions in visit methods
- Added `-o` `--output` flag to define the name of the output file
- Default name of the output file is now `output.[ext]`

## Version 0.0.0
- First release:
    - Lexer
    - Parser
    - AST
    - Multi-architecture support
    - NASM backend
    - CLI
    - Expressions