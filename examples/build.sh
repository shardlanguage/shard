#!/bin/bash

mkdir -p examples/output/

shardc -to-x examples/hello_libc/hello_libc.sd -o examples/output/hello_libc
shardc -to-x examples/points/main.sd -o examples/output/points
shardc -tflags "-ffreestanding -nostdlib" -nostd --no-main -to-x examples/kernel/kernel.sd -o examples/output/kernel