import os

from shardc.utils.errors.fs import ShardError_FileNotFound, ShardError_IsADirectory

def check_file(file: str):
    if not os.path.exists(file):
        ShardError_FileNotFound(file).display()
    if os.path.isdir(file):
        ShardError_IsADirectory(file).display()