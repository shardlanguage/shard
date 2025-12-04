#!/bin/bash

set -e

mkdir -p examples/output/

shardc -to-x examples/hello_libc/hello_libc.sd -o examples/output/hello_libc
shardc -to-x examples/points/main.sd -o examples/output/points
shardc -nostd --no-main -tflags "-ffreestanding -nostdlib" -to-x examples/kernel/kernel.sd -o examples/output/kernel
shardc --keep-all -to-x examples/fibonacci/fib.sd -o examples/output/fibonacci