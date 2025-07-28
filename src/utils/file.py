# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains functions related to the code compilation.
# =====================================================================

# Import modules
import os
import subprocess
import platform
import shutil
import sys

from parser import parser
from environment import Environment

# Function to replace a file extension with another extension
def replace_extension(filename, new_ext=None):
    if '.' in filename:
        base, _ = filename.rsplit('.', 1)
    else:
        base = filename

    if new_ext:
        return f"{base}.{new_ext}"
    else:
        return base

# Function to compile Shard code to C from a file and write the generated C code
# into a new file
def compile_to_c(inputf):
    if os.path.exists(inputf):
        with open(inputf, "r") as f:
            content = f.read()

        if content:
            #try:
            env = Environment()
            ast = parser.parse(content)
            result = env.compile_ast(ast)
            #except Exception as e:
            #    print(f"ERROR: {e}")
            #    sys.exit(1)

            outputf = replace_extension(inputf, "c")

            with open(outputf, 'w') as f:
                if result:
                    for res in result:
                        f.write(res)
            return outputf
    else:
        raise FileNotFoundError(f"File \"{inputf}\" not found.")

# Function that uses GCC to compile a C file to an object file
def compile_c_to_object(c_file):
    if shutil.which("gcc") is None:
        raise EnvironmentError("gcc is not installed or not in PATH.")

    obj_file = replace_extension(c_file, "o")
    cmd = ["gcc", "-c", c_file, "-o", obj_file]
    subprocess.run(cmd, check=True)
    return obj_file

# Function that uses GCC to link an object file to an executable file
def link_object_to_executable(obj_file):
    if shutil.which("gcc") is None:
        raise EnvironmentError("gcc is not installed or not in PATH.")

    system = platform.system()
    if system in ["Linux", "Darwin"]:
        exe_file = replace_extension(obj_file, "")
    elif system == "Windows":
        exe_file = replace_extension(obj_file, "exe")
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

    cmd = ["gcc", obj_file, "-o", exe_file]
    subprocess.run(cmd, check=True)
    return exe_file