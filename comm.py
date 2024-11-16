#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  16-11-2024
Last update: 16-11-2024
Version: 1.0
Description: The comm command from GNU coreutils in Python3  
Example of use: python3 comm.py file1.txt file2.txt
'''

import sys

def read_file(file_path, zero_terminated=False):
    """Lit un fichier et retourne une liste de lignes, gérant le délimiteur."""
    delimiter = "\0" if zero_terminated else "\n"
    if file_path == "-":
        return sys.stdin.read().split(delimiter)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().split(delimiter)

def compare_files(file1_lines, file2_lines, suppress_columns, delimiter, zero_terminated):
    """Compare deux listes de lignes et affiche les résultats."""
    delimiter = delimiter if delimiter else ("\0" if zero_terminated else "\t")
    output = []

    file1_only = sorted(set(file1_lines) - set(file2_lines))
    file2_only = sorted(set(file2_lines) - set(file1_lines))
    common = sorted(set(file1_lines) & set(file2_lines))

    if 1 not in suppress_columns:
        output.extend([f"{line}{delimiter}" for line in file1_only])
    if 2 not in suppress_columns:
        output.extend([f"{delimiter}{line}" for line in file2_only])
    if 3 not in suppress_columns:
        output.extend([f"{delimiter}{delimiter}{line}" for line in common])

    return "".join(output)

def main():
    suppress_columns = set()
    check_order = True
    output_delimiter = None
    zero_terminated = False
    file1 = None
    file2 = None

    # Parsing des arguments
    args = iter(sys.argv[1:])
    for arg in args:
        if arg == "-1":
            suppress_columns.add(1)
        elif arg == "-2":
            suppress_columns.add(2)
        elif arg == "-3":
            suppress_columns.add(3)
        elif arg == "--check-order":
            check_order = True
        elif arg == "--nocheck-order":
            check_order = False
        elif arg.startswith("--output-delimiter="):
            output_delimiter = arg.split("=", 1)[1]
        elif arg in ("-z", "--zero-terminated"):
            zero_terminated = True
        elif arg == "--help":
            print("Usage: comm [OPTION]... FILE1 FILE2\nCompare two sorted files line by line.")
            return
        elif arg == "--version":
            print("comm 1.0")
            return
        elif file1 is None:
            file1 = arg
        elif file2 is None:
            file2 = arg
        else:
            print(f"Unexpected argument: {arg}", file=sys.stderr)
            sys.exit(1)

    if not file1 or not file2:
        print("Error: Two input files are required.", file=sys.stderr)
        sys.exit(1)

    # Lire les fichiers
    file1_lines = read_file(file1, zero_terminated)
    file2_lines = read_file(file2, zero_terminated)

    # Comparaison
    output = compare_files(file1_lines, file2_lines, suppress_columns, output_delimiter, zero_terminated)
    sys.stdout.write(output)

if __name__ == "__main__":
    main()

