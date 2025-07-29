# =====================================================================
# The Shard programming language - shardc compiler
#
# Released under MIT License
#
# This file contains functions related to text manipulation, like find
# ing rows or columns.
# =====================================================================

def find_column(input_, token):
    last_cr = input_.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return token.lexpos - last_cr