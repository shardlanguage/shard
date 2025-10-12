import argparse

from shardc.cli.execute import execute_args

def cli():
    parser = argparse.ArgumentParser(description="The shardc command-line interface")

    parser.add_argument("-l", "--lex", type=str, help="Display tokens")
    parser.add_argument("-p", "--parse", type=str, help="Parse source code")
    parser.add_argument("-t", "--tree", type=str, help="Print AST")
    parser.add_argument("-s", "--assembly", type=str, help="Generate assembly code")

    args = parser.parse_args()
    execute_args(args)