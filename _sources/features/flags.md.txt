# Compiler flags
---

## Summary
---
- [Flag list](#flag-list)

## Flag list
---
| Short name    | Long name | Effect |
| ----------    | --------- | ------ |
| `-v`          | `--version` | Display the current version of `shardc` |
| `-l`          | `--lex`   | Lex the source code of a file and display the tokens |
| `-p`          | `--parse` | Parse the source code of a file to check eventual syntax errors |
| `-t`          | `--tree`  | Get the AST of the source code of a file |
| `-P`          | `--preprocess` | Only execute the preprocessor |
| `-c`          | `--compile` | Only generate the intermediate code |
| `-to-o`       | `--to-object` | Compile to object file |
| `-to-x`       | `--to-executable` | Compile to executable file |
| `-o`          | `--output`  | Name of the output file (without the extension) |
| `-b`          | `--backend` | Change compiler backend (default is "c") |
| `-T`          | `--target`  | Change target compiler (default is clang) |
| `-tflags`     | `--target-flags`| Pass flags to the target compiler |
|               | `--keep-all`| Do not remove intermediate files |
|               | `--no-main` | Disable obligation to define main function |
| `-nostd`      |             | Disable dependencies to the standard library |

***Note**: `-nostd` is useless because there is no standard library yet.*