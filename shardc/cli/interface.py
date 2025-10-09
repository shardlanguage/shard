import argparse

from shardc.cli.execute import execute_args

def cli():
    parser = argparse.ArgumentParser(description="The shardc command-line interface")

    parser.add_argument("-l", "--lex", type=str, help="Display tokens")

    args = parser.parse_args()
    execute_args(args)