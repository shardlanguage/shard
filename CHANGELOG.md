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