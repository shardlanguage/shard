---
name: Bug report
about: Report a bug in Shard
title: "[BUG] "
labels: bug
assignees: ''
---

**Bug description**
Describe your problem clearly and concisely.
- **Bad**: *I found a bug, my code doesn't compile.*
- **Good**: "I think I found a bug in the compiler source code. The built-in function `foo` makes the compiler crash when you pass a string containing more than 5 characters to it.*

**Steps to reproduce**
Describe **in order** the steps people need to follow to reproduce the bug.
1. Include `lib:foo/foo` in your program
2. Call the function `foo` with the following parameter: `"aaaaaa"`
3. Compile the program using the `-to-x` option

**Expected behaviour**
The function should have returned 42.

**Screenshots/logs**

**Other information**