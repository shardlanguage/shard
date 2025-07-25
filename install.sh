#!/bin/bash

set -e

cd "$(dirname "$0")"

mkdir -p parser_out

command -v pyinstaller >/dev/null 2>&1 || { echo >&2 "pyinstaller is required but not installed."; exit 1; }
command -v install >/dev/null 2>&1 || { echo >&2 "install command not found."; exit 1; }

pyinstaller --onefile src/shardc.py
install dist/shardc /usr/bin/shardc

rm -r build
rm -r shardc.spec
rm -r dist