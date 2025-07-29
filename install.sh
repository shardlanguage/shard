#!/bin/bash

# Stop if an error happen
set -e

# The program needs root permissions
if [ "$(id -u)" -ne 0 ]; then
    echo "This program must be executed as root."
    exit 1
fi

# Go to the script directory
cd "$(dirname "$0")"

# This directory is required for the parser
mkdir -p parser_out

# Check if the dependencies are installed
command -v pyinstaller >/dev/null 2>&1 || { echo >&2 "pyinstaller is required but not installed."; exit 1; }
command -v install >/dev/null 2>&1 || { echo >&2 "install command not found."; exit 1; }
command -v gcc >/dev/null 2>&1 || { echo >&2 "GCC not found."; exit 1; }

# Make the executable
pyinstaller --onefile --strip --clean --name shardc --exclude-module tkinter --add-data "parser_out:parser_out" src/shardc.py

# Install shardc
install dist/shardc /usr/bin/shardc

# Clean build files
rm -r build
rm -r shardc.spec
rm -r dist