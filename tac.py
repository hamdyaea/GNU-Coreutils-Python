#!/usr/bin/env python3
'''
Name:  Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2204
Version: 1.0
Description: The tac command from GNU coreutils in Python3  
Example of use:  python3 tac.py file.txt
'''
import argparse
import sys
import re

def tac(file, separator="\n", before=False, regex=False):
    """Imprime le contenu du fichier en inversant les lignes."""
    if file == "-":
        file = "/dev/stdin"
    try:
        with open(file, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"tac: {file}: No such file or directory", file=sys.stderr)
        return
    except Exception as e:
        print(f"tac: {file}: {e}", file=sys.stderr)
        return

    if regex:
        parts = re.split(separator, content)
    else:
        parts = content.split(separator)

    if before:
        output = separator.join(reversed(parts))
    else:
        output = separator.join(reversed(parts)) + separator

    sys.stdout.write(output)

def main():
    parser = argparse.ArgumentParser(description="Concatenate and print files in reverse.")
    parser.add_argument("files", nargs="*", default=["-"], help="Files to process (default: standard input).")
    parser.add_argument("-b", "--before", action="store_true", help="Attach the separator before instead of after.")
    parser.add_argument("-r", "--regex", action="store_true", help="Interpret the separator as a regular expression.")
    parser.add_argument("-s", "--separator", default="\n", help="Use STRING as the separator instead of newline.")
    parser.add_argument("--version", action="version", version="tac.py 1.0")

    args = parser.parse_args()

    for file in args.files:
        tac(file, separator=args.separator, before=args.before, regex=args.regex)

if __name__ == "__main__":
    main()

