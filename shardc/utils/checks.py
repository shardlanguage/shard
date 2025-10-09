import os

from shardc.utils.errors.fs import ShardError_FileNotFound, ShardError_IsADirectory

def check_path(path: str) -> None:
    if not os.path.exists(path):
        ShardError_FileNotFound(path).display()
    if os.path.isdir(path):
        ShardError_IsADirectory(path).display()