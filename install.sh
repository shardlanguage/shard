#!/bin/bash

TARGET=shardc

pyinstaller --onefile --collect-submodules shardc shardc.py --name $TARGET

install -m 755 dist/$TARGET /usr/bin/shardc